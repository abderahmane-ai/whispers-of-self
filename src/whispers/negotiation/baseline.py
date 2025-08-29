"""
Negotiation baseline (single-round, demand-threshold model).

This module provides just the interfaces needed by the environment; fill in
the decision logic later using agent methods and parameters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from src.whispers.agents.base_agent import BaseAgent


@dataclass
class NegotiationConfig:
    """Configuration for baseline negotiation rules."""
    demand_grid: Tuple[float, ...] = (0.3, 0.4, 0.5, 0.6, 0.7)


class Negotiation:
    """Minimal negotiator that can be extended later."""

    def __init__(self, config: NegotiationConfig | None = None) -> None:
        self._config: NegotiationConfig = config or NegotiationConfig()

    def negotiate(self, a: BaseAgent, b: BaseAgent, resource_size: int) -> Tuple[int, int, bool]:
        """
        Return (share_a, share_b, success). Implement selection and acceptance later.
        """
        return 0, 0, False


