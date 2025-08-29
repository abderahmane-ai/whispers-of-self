"""
Altruist agent: cooperative, fair, and low greed.
"""

import random
from typing import Optional

from ..base_agent import BaseAgent


class Altruist(BaseAgent):
    """
    Altruistic agent that prioritizes cooperation and fairness.
    
    Characteristics:
    - Low resource requests
    - Fair negotiation demands (~50%)
    - High acceptance threshold for cooperation
    - Low greed index
    """
    
    def __init__(self, **kwargs):
        """Initialize an altruistic agent."""
        kwargs.setdefault('agent_type', 'altruist')
        kwargs.setdefault('request_multiplier', 0.7)
        kwargs.setdefault('negotiation_demand', 0.5)
        kwargs.setdefault('acceptance_threshold', 0.3)
        kwargs.setdefault('greed_index', 0.2)
        super().__init__(**kwargs)
        
    def reproduce(self, mutation_rate: float = 0.05) -> Optional['Altruist']:
        if not self.can_reproduce():
            return None
        if random.random() < mutation_rate:
            from .pragmatist import Pragmatist
            from .egoist import Egoist
            if random.random() < 0.5:
                offspring = Pragmatist()
            else:
                offspring = Egoist()
        else:
            offspring = Altruist(
                request_multiplier=self.state.request_multiplier + random.uniform(-0.1, 0.1),
                negotiation_demand=self.state.negotiation_demand + random.uniform(-0.05, 0.05),
                acceptance_threshold=self.state.acceptance_threshold + random.uniform(-0.05, 0.05),
                greed_index=self.state.greed_index + random.uniform(-0.1, 0.1)
            )
        self.charge_reproduction_cost()
        return offspring