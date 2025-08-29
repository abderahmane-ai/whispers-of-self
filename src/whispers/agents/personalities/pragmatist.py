"""
Pragmatist agent: adaptive and moderate behavior.
"""

import random
from typing import Optional

from ..base_agent import BaseAgent


class Pragmatist(BaseAgent):
    """Pragmatic agent that adapts to context and circumstances."""

    def __init__(self, **kwargs):
        kwargs.setdefault('agent_type', 'pragmatist')
        kwargs.setdefault('request_multiplier', 1.0)
        kwargs.setdefault('negotiation_demand', 0.55)
        kwargs.setdefault('acceptance_threshold', 0.35)
        kwargs.setdefault('greed_index', 0.5)
        super().__init__(**kwargs)

    def reproduce(self, mutation_rate: float = 0.05) -> Optional['Pragmatist']:
        if not self.can_reproduce():
            return None
        if random.random() < mutation_rate:
            from .altruist import Altruist
            from .egoist import Egoist
            if random.random() < 0.5:
                offspring = Altruist()
            else:
                offspring = Egoist()
        else:
            offspring = Pragmatist(
                request_multiplier=self.state.request_multiplier + random.uniform(-0.1, 0.1),
                negotiation_demand=self.state.negotiation_demand + random.uniform(-0.05, 0.05),
                acceptance_threshold=self.state.acceptance_threshold + random.uniform(-0.05, 0.05),
                greed_index=self.state.greed_index + random.uniform(-0.1, 0.1)
            )
        self.charge_reproduction_cost()
        return offspring