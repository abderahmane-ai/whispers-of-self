"""
Re-export personality agents from their split modules for backward compatibility.
"""

from .personalities.altruist import Altruist
from .personalities.egoist import Egoist
from .personalities.pragmatist import Pragmatist

__all__ = ["Altruist", "Egoist", "Pragmatist"]
