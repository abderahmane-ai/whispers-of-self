"""
Imitation (social copying) baseline.

Provides an interface to update agent strategies by copying others.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from src.whispers.agents.base_agent import BaseAgent


@dataclass
class ImitationConfig:
    copy_interval_days: int = 5
    k_window: int = 5  # performance window length
    kappa: float = 1.0  # selection strength


class Imitation:
    def __init__(self, config: ImitationConfig | None = None) -> None:
        self._config: ImitationConfig = config or ImitationConfig()
        self._last_copy_day: int = -1

    def maybe_copy(self, day_index: int, agents: Sequence[BaseAgent]) -> None:
        """Hook to perform copying on a schedule. Implement logic later."""
        return None


