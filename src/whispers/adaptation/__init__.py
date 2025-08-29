"""Minimal adaptation stubs for tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class EvolutionConfig:
    mutation_rate: float = 0.05
    max_offspring_per_day: int = 0


class Evolution:
    def __init__(self, config: EvolutionConfig | None = None) -> None:
        self.config = config or EvolutionConfig()

    def reproduce(self, agents: Sequence[object]) -> List[object]:
        # No reproduction in baseline; return empty list
        return []


@dataclass
class ImitationConfig:
    copy_interval_days: int = 0


class Imitation:
    def __init__(self, config: ImitationConfig | None = None) -> None:
        self.config = config or ImitationConfig()

    def maybe_copy(self, day_index: int, agents: Iterable[object]) -> None:
        # Baseline no-op
        return None

__all__ = [
    "EvolutionConfig",
    "Evolution",
    "ImitationConfig",
    "Imitation",
]


