"""
Evolutionary adaptation baseline.

Provides a minimal interface to produce offspring and mutate parameters later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from src.whispers.agents.base_agent import BaseAgent


@dataclass
class EvolutionConfig:
    mutation_rate: float = 0.05
    max_offspring_per_day: int = 2


class Evolution:
    def __init__(self, config: EvolutionConfig | None = None) -> None:
        self._config: EvolutionConfig = config or EvolutionConfig()

    def reproduce(self, agents: Sequence[BaseAgent]) -> Sequence[BaseAgent]:
        """Return new offspring. Implement divisible rule and mutation later."""
        return []


