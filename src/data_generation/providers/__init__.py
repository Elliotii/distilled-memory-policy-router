"""Generation provider adapters.

Only the local mock provider is implemented. Real API providers should be added behind
the same interface after the smoke-test plan is approved.
"""

from src.data_generation.providers.base import GenerationProvider
from src.data_generation.providers.mock import LocalMockProvider

__all__ = ["GenerationProvider", "LocalMockProvider"]
