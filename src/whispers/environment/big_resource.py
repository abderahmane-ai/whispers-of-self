"""
Big-resource phase environment baseline.

Responsibilities (to be implemented later):
- Decide if a big resource appears
- Select a candidate pair
- Delegate negotiation and apply outcomes
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from src.whispers.agents.base_agent import BaseAgent


@dataclass
class BigResourceConfig:
    """Configuration for big-resource dynamics."""
    probability_big: float = 1.0  # daily chance a big resource appears
    big_size: int = 50


class BigResourceEnvironment:
    """Baseline scaffold for Phase B (big-resource)."""

    def __init__(self, config: Optional[BigResourceConfig] = None) -> None:
        self._config: BigResourceConfig = config or BigResourceConfig()

    def big_appears(self, day_index: int) -> bool:
        """Decide if a big resource is available today."""
        return self._config.probability_big >= 1.0

    def select_pair(self, agents: Sequence[BaseAgent]) -> Optional[Tuple[BaseAgent, BaseAgent]]:
        """
        Select two agents to negotiate. Replace with sampling / partner choice later.
        """
        if len(agents) < 2:
            return None
        return agents[0], agents[1]


