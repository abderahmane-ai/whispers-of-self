"""
Minimal simulation baseline built around agent interfaces.

This class provides a clean starting point to orchestrate agents, days, and
basic lifecycle events. Extend incrementally by adding environment dynamics,
resource generation, interactions, logging, and metrics as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

from src.whispers.agents.base_agent import BaseAgent


@dataclass
class SimulationConfig:
    """Configuration settings for a simulation run."""
    num_days: int = 30
    daily_resource_budget: int = 0


class Simulation:
    """
    Orchestrates the simulation loop.

    Responsibilities:
    - Hold references to agents
    - Advance discrete time steps (days)
    """

    def __init__(self, agents: Optional[Sequence[BaseAgent]] = None, config: Optional[SimulationConfig] = None) -> None:
        self._agents: List[BaseAgent] = list(agents) if agents is not None else []
        self._config: SimulationConfig = config or SimulationConfig()
        self._day_index: int = 0


    @property
    def day(self) -> int:
        return self._day_index

    @property
    def agents(self) -> Sequence[BaseAgent]:
        return tuple(self._agents)

    def add_agents(self, new_agents: Iterable[BaseAgent]) -> None:
        for agent in new_agents:
            self._agents.append(agent)

    def run(self) -> None:
        """
        Run the simulation for the configured number of days.
        """
        for _ in range(self._config.num_days):
            self.step()

    def step(self) -> None:
        """
        Advance the simulation by one day.

        Default behavior:
        - Age all agents
        - Call hooks for resource distribution and interactions (no-op by default)
        - Cull dead agents (if any external logic marks them dead)
        """
        self._day_index += 1