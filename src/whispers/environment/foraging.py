"""
Foraging phase environment baseline.

Responsibilities (to be implemented later):
- Spawn daily small resources
- Collect agent requests and allocate according to a chosen rule
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from src.whispers.agents.base_agent import BaseAgent


@dataclass
class ForagingConfig:
    """Configuration for foraging dynamics."""
    lambda_supply: int = 20  # mean or fixed daily small-resource units
    allocation_mode: str = "proportional"  # or "sequential"


class ForagingEnvironment:
    """Baseline scaffold for Phase A (foraging)."""

    def __init__(self, config: ForagingConfig | None = None) -> None:
        self._config: ForagingConfig = config or ForagingConfig()

    def spawn_resources(self, day_index: int) -> int:
        """
        Determine daily small-resource availability.
        Replace with stochastic draw if needed (e.g., Poisson).
        """
        return int(self._config.lambda_supply)

    def allocate(self, agents: Sequence[BaseAgent], supply: int) -> None:
        """
        Allocate resources to agents based on their requests.
        Implement chosen rule (proportional / sequential) later.
        This should call `agent.add_resources(amount)` per agent.
        """
        return None


