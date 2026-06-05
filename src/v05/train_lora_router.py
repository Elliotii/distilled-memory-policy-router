"""Qwen3-4B Unit DSL QLoRA training script for v0.5.

Usage:
  PYTHONDONTWRITEBYTECODE=1 python src/v05/train_lora_router.py \
    --config configs/v05/qwen3_4b_lora_dsl_125.yaml
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_yaml(path: str) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)


def _resolve_path(raw: str) -> str:
    """Expand environment variables and ~ in a path string."""
    s = os.path.expanduser(raw)
    s = os.path.expandvars(s)
    return s


def preflight(cfg: dict[str, Any]) -> bool:
    """Run preflight checks. Return True if safe to train."""
    print("=" * 60)
    print("PREFLIGHT CHECK")
    print("=" * 60)

    ok = True

    # Paths — resolve env vars
    train_path = Path(_resolve_path(cfg["train_file"]))
    eval_path = Path(_resolve_path(cfg["eval_file"]))
    model_path = Path(_resolve_path(cfg["base_model_path"]))
    output_dir = Path(_resolve_path(cfg["output_dir"]))
    print(f"✅ Resolved model path: {model_path}")

    for label, path in [("train", train_path), ("eval", eval_path), ("model", model_path)]:
        if not path.exists():
            print(f"❌ {label} not found: {path}")
            ok = False
        else:
            print(f"✅ {label}: {path}")

    # Row counts
    with open(train_path) as f:
        train_rows = [json.loads(l) for l in f if l.strip()]
    with open(eval_path) as f:
        eval_rows = [json.loads(l) for l in f if l.strip()]
    print(f"✅ train rows: {len(train_rows)}")
    print(f"✅ eval rows: {len(eval_rows)}")

    # Validate assistant format (markdown-free, interface-agnostic)
    interface_label = cfg.get("interface", "unit_dsl")
    bad = sum(1 for r in train_rows if "```" in r["messages"][2]["content"])
    if bad:
        print(f"❌ {bad} train rows have markdown in assistant")
        ok = False
    else:
        print(f"✅ No markdown in train assistant ({interface_label})")

    bad = sum(1 for r in eval_rows if "```" in r["messages"][2]["content"])
    if bad:
        print(f"❌ {bad} eval rows have markdown in assistant")
        ok = False
    else:
        print(f"✅ No markdown in eval assistant ({interface_label})")

    # No gold in config
    cfg_text = json.dumps(cfg)
    if "gold" in cfg_text.lower():
        print("❌ 'gold' appears in config — possible gold leak")
        ok = False
    else:
        print("✅ No gold references in config")

    # CUDA
    import torch
    if not torch.cuda.is_available():
        print("❌ CUDA not available")
        ok = False
    else:
        p = torch.cuda.get_device_properties(0)
        free, total = torch.cuda.mem_get_info(0)
        quant_mode = cfg.get("quantization", "4bit")
        print(f"✅ CUDA: {p.name}, {total//1024**3}GB total, {free//1024**3}GB free")
        print(f"✅ Quantization mode: {quant_mode}")

    # Output dir
    if output_dir.exists() and list(output_dir.iterdir()):
        print(f"⚠ Output dir exists and is non-empty: {output_dir}")
        # Not a hard fail — allow overwrite with warning
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Output dir: {output_dir}")

    # Dry-run tokenizer
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True, trust_remote_code=True)
        print(f"✅ Tokenizer loaded: vocab={len(tok)}")
    except Exception as e:
        print(f"❌ Tokenizer load failed: {e}")
        ok = False

    print("=" * 60)
    if ok:
        print("✅ PREFLIGHT PASSED")
    else:
        print("❌ PREFLIGHT FAILED — aborting")
    return ok


def train(cfg: dict[str, Any]) -> bool:
    """Run LoRA/QLoRA training. Return True on success.
    
    Supports two quantization modes via config:
    - quantization: "4bit" (QLoRA — default, backward-compatible)
    - quantization: "none" (standard BF16 LoRA — no quantization)
    """
    import torch
    from transformers import (
        AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig,
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from trl import SFTTrainer
    from datasets import Dataset

    print("=" * 60)
    print("TRAINING")
    print("=" * 60)

    model_path = _resolve_path(cfg["base_model_path"])
    train_path = cfg["train_file"]
    eval_path = cfg["eval_file"]
    output_dir = Path(cfg["output_dir"])
    quant_mode = cfg.get("quantization", "4bit")  # "4bit" or "none"
    gp_checkpointing = cfg.get("gradient_checkpointing", False)

    # Load data
    with open(train_path) as f:
        train_data = [json.loads(l) for l in f if l.strip()]
    with open(eval_path) as f:
        eval_data = [json.loads(l) for l in f if l.strip()]
    print(f"Train: {len(train_data)}  |  Eval: {len(eval_data)}")
    print(f"Quantization: {quant_mode}")

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Format for SFTTrainer
    def format_sft(example):
        return tokenizer.apply_chat_template(
            example["messages"], tokenize=False, add_generation_prompt=False,
        )

    train_dataset = Dataset.from_list(train_data)
    eval_dataset = Dataset.from_list(eval_data)

    # Model loading: QLoRA vs standard BF16 LoRA
    if quant_mode == "none":
        # Standard BF16 LoRA — no quantization
        print("Loading model in BF16 (standard LoRA, no quantization)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            local_files_only=True,
            trust_remote_code=True,
        )
        # No prepare_model_for_kbit_training needed for standard LoRA
        use_kbit = False
    else:
        # QLoRA — 4-bit quantization
        bnb_compute_dtype = getattr(torch, cfg.get("bnb_4bit_compute_dtype", "bfloat16"))
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=bnb_compute_dtype,
            bnb_4bit_quant_type=cfg.get("bnb_4bit_quant_type", "nf4"),
            bnb_4bit_use_double_quant=cfg.get("bnb_4bit_use_double_quant", True),
        )
        print("Loading model with QLoRA (4-bit quantization)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=bnb_config,
            device_map="auto",
            local_files_only=True,
            trust_remote_code=True,
        )
        model = prepare_model_for_kbit_training(model)
        use_kbit = True

    lora_config = LoraConfig(
        r=cfg.get("lora_r", 8),
        lora_alpha=cfg.get("lora_alpha", 16),
        lora_dropout=cfg.get("lora_dropout", 0.05),
        target_modules=cfg.get("lora_target_modules", ["q_proj", "k_proj", "v_proj", "o_proj"]),
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Gradient checkpointing (for VRAM-constrained GPUs like RTX 4090 24GB)
    if gp_checkpointing:
        print("Enabling gradient checkpointing...")
        if hasattr(model, "config") and hasattr(model.config, "use_cache"):
            model.config.use_cache = False
            print("  model.config.use_cache = False")
        if hasattr(model, "gradient_checkpointing_enable"):
            model.gradient_checkpointing_enable()
            print("  gradient_checkpointing_enable() called")
        else:
            # Fallback for wrapped models
            try:
                model.enable_input_require_grads()
                print("  enable_input_require_grads() called (PEFT gradient checkpointing compat)")
            except Exception:
                pass
    else:
        print("Gradient checkpointing: disabled")

    # Optimizer: adamw_8bit works with QLoRA; standard LoRA needs adamw_torch
    optim = cfg.get("optim", "adamw_8bit")
    if quant_mode == "none" and optim == "adamw_8bit":
        print("⚠ Switching optimizer from adamw_8bit to adamw_torch (required for standard BF16 LoRA)")
        optim = "adamw_torch"

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=cfg.get("num_train_epochs", 3),
        per_device_train_batch_size=cfg.get("per_device_train_batch_size", 4),
        per_device_eval_batch_size=cfg.get("per_device_eval_batch_size", 4),
        gradient_accumulation_steps=cfg.get("gradient_accumulation_steps", 4),
        learning_rate=cfg.get("learning_rate", 2e-4),
        lr_scheduler_type=cfg.get("lr_scheduler_type", "cosine"),
        warmup_ratio=cfg.get("warmup_ratio", 0.1),
        optim=optim,
        weight_decay=cfg.get("weight_decay", 0.01),
        bf16=cfg.get("bf16", True),
        tf32=cfg.get("tf32", True),
        eval_strategy=cfg.get("eval_strategy", "epoch"),
        save_strategy=cfg.get("save_strategy", "epoch"),
        save_total_limit=cfg.get("save_total_limit", 3),
        load_best_model_at_end=cfg.get("load_best_model_at_end", True),
        metric_for_best_model=cfg.get("metric_for_best_model", "eval_loss"),
        logging_steps=cfg.get("logging_steps", 10),
        report_to=cfg.get("report_to", "none"),
        seed=cfg.get("seed", 42),
        data_seed=cfg.get("data_seed", 42),
        gradient_checkpointing=gp_checkpointing,
        remove_unused_columns=False,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        formatting_func=format_sft,
        processing_class=tokenizer,
    )

    t0 = time.perf_counter()
    print("Starting training...")
    trainer.train()
    elapsed = time.perf_counter() - t0
    print(f"Training completed in {elapsed:.0f}s")

    # Save adapter
    adapter_dir = output_dir / "adapter"
    trainer.model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))
    print(f"Adapter saved to {adapter_dir}")

    # Save summary
    summary = {
        "config": cfg,
        "train_rows": len(train_data),
        "eval_rows": len(eval_data),
        "training_time_s": round(elapsed, 1),
        "output_dir": str(output_dir),
        "adapter_dir": str(adapter_dir),
        "completed_utc": datetime.now(timezone.utc).isoformat(),
    }
    with open(output_dir / "training_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    del model; del trainer; gc.collect()
    torch.cuda.empty_cache()
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to YAML config")
    args = ap.parse_args()

    cfg = load_yaml(args.config)

    if not preflight(cfg):
        return 1

    try:
        ok = train(cfg)
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
