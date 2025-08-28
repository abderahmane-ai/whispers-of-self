"""
Concrete agent classes with different personality types.

This module implements the three main personality archetypes:
- Altruist: Cooperative, fair, low demands
- Egoist: Selfish, high demands, low cooperation
- Pragmatist: Adaptive, moderate demands, context-sensitive
"""

import random
from typing import Optional
from .base_agent import BaseAgent


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
        # Set default values if not provided
        kwargs.setdefault('agent_type', 'altruist')
        kwargs.setdefault('request_multiplier', 0.7)  # Request less than average
        kwargs.setdefault('negotiation_demand', 0.5)  # Fair 50/50 split
        kwargs.setdefault('acceptance_threshold', 0.3)  # Accept down to 30%
        kwargs.setdefault('greed_index', 0.2)  # Low greed
        
        super().__init__(**kwargs)
    
    def calculate_request(self, total_resources: int, population_size: int) -> int:
        """
        Calculate resource request - altruists request less than their fair share.
        
        Args:
            total_resources: Total resources available today
            population_size: Current population size
            
        Returns:
            Number of resources to request
        """
        fair_share = total_resources / max(population_size, 1)
        base_request = int(fair_share * self.state.request_multiplier)
        
        # Add small random variation
        variation = random.randint(-1, 1)
        return max(1, base_request + variation)
    
    def negotiate_demand(self, partner_reputation: float) -> float:
        """
        Negotiate demand - altruists are fair regardless of partner.
        
        Args:
            partner_reputation: Partner's reputation (not used by altruists)
            
        Returns:
            Demand as a fraction (0.0 to 1.0)
        """
        # Altruists maintain fair demands regardless of partner
        base_demand = self.state.negotiation_demand
        
        # Small adjustment based on partner reputation
        if partner_reputation > 0.8:
            # Be slightly more generous with highly reputable partners
            adjustment = random.uniform(-0.05, 0.0)
        else:
            # Standard fair demand
            adjustment = random.uniform(-0.02, 0.02)
        
        return max(0.3, min(0.7, base_demand + adjustment))
    
    def will_accept_offer(self, partner_demand: float, partner_reputation: float) -> bool:
        """
        Accept offers - altruists are more accepting.
        
        Args:
            partner_demand: Partner's demand as a fraction
            partner_reputation: Partner's reputation
            
        Returns:
            True if the agent accepts the offer
        """
        my_share = 1.0 - partner_demand
        
        # Altruists accept if they get at least their acceptance threshold
        if my_share >= self.state.acceptance_threshold:
            return True
        
        # Sometimes accept even unfair offers if partner has good reputation
        if partner_reputation > 0.7 and my_share >= self.state.acceptance_threshold * 0.8:
            return random.random() < 0.3  # 30% chance to accept
        
        return False
    
    def reproduce(self, mutation_rate: float = 0.05) -> Optional['Altruist']:
        """
        Create an altruistic offspring with potential mutations.
        
        Args:
            mutation_rate: Probability of mutation in offspring
            
        Returns:
            New Altruist instance or None if reproduction fails
        """
        if random.random() < mutation_rate:
            # Mutate to a different type
            if random.random() < 0.5:
                return Pragmatist()
            else:
                return Egoist()
        else:
            # Create offspring with slight parameter variations
            return Altruist(
                request_multiplier=self.state.request_multiplier + random.uniform(-0.1, 0.1),
                negotiation_demand=self.state.negotiation_demand + random.uniform(-0.05, 0.05),
                acceptance_threshold=self.state.acceptance_threshold + random.uniform(-0.05, 0.05),
                greed_index=self.state.greed_index + random.uniform(-0.1, 0.1)
            )


class Egoist(BaseAgent):
    """
    Egoistic agent that prioritizes self-interest.
    
    Characteristics:
    - High resource requests
    - High negotiation demands (≥60%)
    - Low acceptance threshold for cooperation
    - High greed index
    """
    
    def __init__(self, **kwargs):
        """Initialize an egoistic agent."""
        # Set default values if not provided
        kwargs.setdefault('agent_type', 'egoist')
        kwargs.setdefault('request_multiplier', 1.5)  # Request more than average
        kwargs.setdefault('negotiation_demand', 0.7)  # High demand for 70%
        kwargs.setdefault('acceptance_threshold', 0.4)  # Only accept if they get at least 40%
        kwargs.setdefault('greed_index', 0.8)  # High greed
        
        super().__init__(**kwargs)
    
    def calculate_request(self, total_resources: int, population_size: int) -> int:
        """
        Calculate resource request - egoists request more than their fair share.
        
        Args:
            total_resources: Total resources available today
            population_size: Current population size
            
        Returns:
            Number of resources to request
        """
        fair_share = total_resources / max(population_size, 1)
        base_request = int(fair_share * self.state.request_multiplier)
        
        # Add random variation
        variation = random.randint(-2, 3)
        return max(1, base_request + variation)
    
    def negotiate_demand(self, partner_reputation: float) -> float:
        """
        Negotiate demand - egoists demand more, especially from low-reputation partners.
        
        Args:
            partner_reputation: Partner's reputation
            
        Returns:
            Demand as a fraction (0.0 to 1.0)
        """
        base_demand = self.state.negotiation_demand
        
        # Adjust based on partner reputation
        if partner_reputation < 0.4:
            # Demand more from low-reputation partners
            adjustment = random.uniform(0.05, 0.15)
        elif partner_reputation > 0.8:
            # Slightly reduce demand from high-reputation partners
            adjustment = random.uniform(-0.05, 0.05)
        else:
            # Standard high demand
            adjustment = random.uniform(-0.02, 0.08)
        
        return max(0.5, min(0.9, base_demand + adjustment))
    
    def will_accept_offer(self, partner_demand: float, partner_reputation: float) -> bool:
        """
        Accept offers - egoists are less accepting.
        
        Args:
            partner_demand: Partner's demand as a fraction
            partner_reputation: Partner's reputation
            
        Returns:
            True if the agent accepts the offer
        """
        my_share = 1.0 - partner_demand
        
        # Egoists have higher acceptance threshold
        if my_share >= self.state.acceptance_threshold:
            return True
        
        # Rarely accept unfair offers, even from high-reputation partners
        if partner_reputation > 0.9 and my_share >= self.state.acceptance_threshold * 0.9:
            return random.random() < 0.1  # 10% chance to accept
        
        return False
    
    def reproduce(self, mutation_rate: float = 0.05) -> Optional['Egoist']:
        """
        Create an egoistic offspring with potential mutations.
        
        Args:
            mutation_rate: Probability of mutation in offspring
            
        Returns:
            New Egoist instance or None if reproduction fails
        """
        if random.random() < mutation_rate:
            # Mutate to a different type
            if random.random() < 0.5:
                return Pragmatist()
            else:
                return Altruist()
        else:
            # Create offspring with slight parameter variations
            return Egoist(
                request_multiplier=self.state.request_multiplier + random.uniform(-0.1, 0.1),
                negotiation_demand=self.state.negotiation_demand + random.uniform(-0.05, 0.05),
                acceptance_threshold=self.state.acceptance_threshold + random.uniform(-0.05, 0.05),
                greed_index=self.state.greed_index + random.uniform(-0.1, 0.1)
            )


class Pragmatist(BaseAgent):
    """
    Pragmatic agent that adapts to context and circumstances.
    
    Characteristics:
    - Adaptive resource requests based on availability
    - Moderate negotiation demands (~50-60%)
    - Context-sensitive acceptance threshold
    - Moderate greed index
    """
    
    def __init__(self, **kwargs):
        """Initialize a pragmatic agent."""
        # Set default values if not provided
        kwargs.setdefault('agent_type', 'pragmatist')
        kwargs.setdefault('request_multiplier', 1.0)  # Average requests
        kwargs.setdefault('negotiation_demand', 0.55)  # Moderate demand for 55%
        kwargs.setdefault('acceptance_threshold', 0.35)  # Moderate acceptance threshold
        kwargs.setdefault('greed_index', 0.5)  # Moderate greed
        
        super().__init__(**kwargs)
    
    def calculate_request(self, total_resources: int, population_size: int) -> int:
        """
        Calculate resource request - pragmatists adapt to resource availability.
        
        Args:
            total_resources: Total resources available today
            population_size: Current population size
            
        Returns:
            Number of resources to request
        """
        fair_share = total_resources / max(population_size, 1)
        
        # Adapt request based on resource availability
        if total_resources > population_size * 10:
            # Abundant resources - request more
            multiplier = self.state.request_multiplier * 1.2
        elif total_resources < population_size * 3:
            # Scarce resources - request less to ensure survival
            multiplier = self.state.request_multiplier * 0.8
        else:
            # Normal conditions
            multiplier = self.state.request_multiplier
        
        base_request = int(fair_share * multiplier)
        variation = random.randint(-1, 2)
        return max(1, base_request + variation)
    
    def negotiate_demand(self, partner_reputation: float) -> float:
        """
        Negotiate demand - pragmatists adapt based on partner reputation.
        
        Args:
            partner_reputation: Partner's reputation
            
        Returns:
            Demand as a fraction (0.0 to 1.0)
        """
        base_demand = self.state.negotiation_demand
        
        # Adapt demand based on partner reputation
        if partner_reputation < 0.3:
            # Demand more from low-reputation partners
            adjustment = random.uniform(0.05, 0.1)
        elif partner_reputation > 0.7:
            # Be more cooperative with high-reputation partners
            adjustment = random.uniform(-0.05, 0.05)
        else:
            # Standard moderate demand
            adjustment = random.uniform(-0.03, 0.03)
        
        return max(0.4, min(0.7, base_demand + adjustment))
    
    def will_accept_offer(self, partner_demand: float, partner_reputation: float) -> bool:
        """
        Accept offers - pragmatists are context-sensitive.
        
        Args:
            partner_demand: Partner's demand as a fraction
            partner_reputation: Partner's reputation
            
        Returns:
            True if the agent accepts the offer
        """
        my_share = 1.0 - partner_demand
        
        # Base acceptance on threshold
        if my_share >= self.state.acceptance_threshold:
            return True
        
        # Context-sensitive acceptance
        if partner_reputation > 0.6:
            # More likely to accept from reputable partners
            if my_share >= self.state.acceptance_threshold * 0.8:
                return random.random() < 0.6  # 60% chance to accept
        elif partner_reputation < 0.3:
            # Less likely to accept from low-reputation partners
            if my_share >= self.state.acceptance_threshold * 1.2:
                return random.random() < 0.2  # 20% chance to accept
        
        return False
    
    def reproduce(self, mutation_rate: float = 0.05) -> Optional['Pragmatist']:
        """
        Create a pragmatic offspring with potential mutations.
        
        Args:
            mutation_rate: Probability of mutation in offspring
            
        Returns:
            New Pragmatist instance or None if reproduction fails
        """
        if random.random() < mutation_rate:
            # Mutate to a different type
            if random.random() < 0.5:
                return Altruist()
            else:
                return Egoist()
        else:
            # Create offspring with slight parameter variations
            return Pragmatist(
                request_multiplier=self.state.request_multiplier + random.uniform(-0.1, 0.1),
                negotiation_demand=self.state.negotiation_demand + random.uniform(-0.05, 0.05),
                acceptance_threshold=self.state.acceptance_threshold + random.uniform(-0.05, 0.05),
                greed_index=self.state.greed_index + random.uniform(-0.1, 0.1)
            )
