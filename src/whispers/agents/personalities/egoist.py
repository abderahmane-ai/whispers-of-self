"""
Egoist agent: selfish and high-demanding behavior.
"""

import random
from typing import Optional

from ..base_agent import BaseAgent


class Egoist(BaseAgent):
    """Egoistic agent that prioritizes self-interest."""

    def __init__(self, **kwargs):
        kwargs.setdefault('agent_type', 'egoist')
        kwargs.setdefault('request_multiplier', 1.5)
        kwargs.setdefault('negotiation_demand', 0.7)
        kwargs.setdefault('acceptance_threshold', 0.4)
        kwargs.setdefault('greed_index', 0.8)
        super().__init__(**kwargs)

    def reproduce(self, mutation_rate: float = 0.05) -> Optional['Egoist']:
        if not self.can_reproduce():
            return None
        if random.random() < mutation_rate:
            from .pragmatist import Pragmatist
            from .altruist import Altruist
            if random.random() < 0.5:
                offspring = Pragmatist()
            else:
                offspring = Altruist()
        else:
            offspring = Egoist(
                request_multiplier=self.state.request_multiplier + random.uniform(-0.1, 0.1),
                negotiation_demand=self.state.negotiation_demand + random.uniform(-0.05, 0.05),
                acceptance_threshold=self.state.acceptance_threshold + random.uniform(-0.05, 0.05),
                greed_index=self.state.greed_index + random.uniform(-0.1, 0.1)
            )
        self.charge_reproduction_cost()
        return offspring