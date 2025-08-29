"""
Whispers of Self - Agent-based simulation package.

This package contains the core agent classes and simulation logic for studying
how micro-level interactions shape macro-level social phenomena.
"""

from .base_agent import BaseAgent
from .personalities import Altruist, Egoist, Pragmatist

__version__ = "0.1.0"
__all__ = ["BaseAgent", "Altruist", "Egoist", "Pragmatist"]
