"""
Personality agent implementations.

This package contains the concrete personality types that inherit from BaseAgent.
"""

from .altruist import Altruist
from .egoist import Egoist
from .pragmatist import Pragmatist

__all__ = ["Altruist", "Egoist", "Pragmatist"]
