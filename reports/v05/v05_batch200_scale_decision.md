# V0.5 Batch200 Scale Decision

Date: 2026-06-01  
Context: 5.1-A — batch200 scale decision  

## Recommendation: Option B — Apply corrections first, then scale to batch500

**Why not Option A (straight to 500):** The svc:task gap (14.3pp) exceeds the 5-8pp target. The auto-generated template cases (0072-0100, 29 cases) need replacement with hand-crafted cases that follow the label policy more closely.

**Corrections needed before batch500:**
1. Replace 29 auto-gen cases (0072-0100) with hand-crafted cases balancing svc:task
2. Target post-correction ratio within 5-8pp

**After corrections, proceed to batch500 generation with strict label policy.**
