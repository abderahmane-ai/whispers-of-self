"""
Base agent class for the Whispers of Self simulation.

This module defines the core agent interface and common functionality
that all agent types will inherit from.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


@dataclass
class AgentState:
    """Represents the current state of an agent."""
    id: str
    agent_type: str
    age: int = 0
    alive: bool = True
    resources_reserve: int = 0
    reputation: float = 0.5
    harvest_history: List[int] = field(default_factory=list)
    cooperation_history: List[bool] = field(default_factory=list)
    
    # Strategy parameters
    request_multiplier: float = 1.0
    negotiation_demand: float = 0.5
    acceptance_threshold: float = 0.3
    greed_index: float = 0.5


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the simulation.
    
    This class defines the interface and common functionality that all
    agent types must implement.
    """
    
    def __init__(self, agent_type: str, **kwargs):
        """Initialize a new agent."""
        self.state = AgentState(
            id=str(uuid.uuid4()),
            agent_type=agent_type,
            **kwargs
        )
        
    @property
    def id(self) -> str:
        """Get the agent's unique identifier."""
        return self.state.id
    
    @property
    def agent_type(self) -> str:
        """Get the agent's type."""
        return self.state.agent_type
    
    @property
    def age(self) -> int:
        """Get the agent's age."""
        return self.state.age
    
    @property
    def alive(self) -> bool:
        """Check if the agent is alive."""
        return self.state.alive
    
    @property
    def reputation(self) -> float:
        """Get the agent's reputation score."""
        return self.state.reputation
    
    def die(self) -> None:
        """Mark the agent as dead."""
        self.state.alive = False
    
    def age_step(self) -> None:
        """Increment the agent's age by one day."""
        self.state.age += 1
    
    def add_resources(self, amount: int) -> None:
        """Add resources to the agent's reserve."""
        self.state.resources_reserve += amount
        self.state.harvest_history.append(amount)
        
        # Keep only last 10 harvests for memory
        if len(self.state.harvest_history) > 10:
            self.state.harvest_history.pop(0)
    
    def consume_resources(self, amount: int) -> bool:
        """
        Consume resources from the agent's reserve.
        
        Returns:
            True if the agent has enough resources, False otherwise.
        """
        if self.state.resources_reserve >= amount:
            self.state.resources_reserve -= amount
            return True
        return False
    
    def update_reputation(self, cooperation_success: bool) -> None:
        """
        Update the agent's reputation based on cooperation behavior.
        
        Args:
            cooperation_success: Whether the agent successfully cooperated
        """
        self.state.cooperation_history.append(cooperation_success)
        
        # Keep only last 20 cooperation events
        if len(self.state.cooperation_history) > 20:
            self.state.cooperation_history.pop(0)
        
        # Calculate reputation as moving average of cooperation
        if self.state.cooperation_history:
            cooperation_rate = sum(self.state.cooperation_history) / len(self.state.cooperation_history)
            # Smooth update with learning rate
            self.state.reputation = 0.9 * self.state.reputation + 0.1 * cooperation_rate
    
    def get_average_harvest(self, days: int = 5) -> float:
        """
        Get the average harvest over the last N days.
        
        Args:
            days: Number of recent days to average over
            
        Returns:
            Average harvest over the specified period
        """
        recent_harvests = self.state.harvest_history[-days:] if self.state.harvest_history else [0]
        return sum(recent_harvests) / len(recent_harvests)
    
    @abstractmethod
    def calculate_request(self, total_resources: int, population_size: int) -> int:
        """
        Calculate how many resources the agent will request.
        
        Args:
            total_resources: Total resources available today
            population_size: Current population size
            
        Returns:
            Number of resources to request
        """
        pass
    
    @abstractmethod
    def negotiate_demand(self, partner_reputation: float) -> float:
        """
        Calculate negotiation demand when cooperating with another agent.
        
        Args:
            partner_reputation: Reputation of the potential partner
            
        Returns:
            Demand as a fraction (0.0 to 1.0)
        """
        pass
    
    @abstractmethod
    def will_accept_offer(self, partner_demand: float, partner_reputation: float) -> bool:
        """
        Determine if the agent will accept a partner's offer.
        
        Args:
            partner_demand: Partner's demand as a fraction
            partner_reputation: Partner's reputation
            
        Returns:
            True if the agent accepts the offer
        """
        pass
    
    def reproduce(self, mutation_rate: float = 0.05) -> Optional['BaseAgent']:
        """
        Create an offspring agent with potential mutations.
        
        Args:
            mutation_rate: Probability of mutation in offspring
            
        Returns:
            New agent instance or None if reproduction fails
        """
        # This will be implemented by concrete agent classes
        return None
    
    def to_dict(self) -> Dict:
        """Convert agent state to dictionary for serialization."""
        return {
            'id': self.state.id,
            'agent_type': self.state.agent_type,
            'age': self.state.age,
            'alive': self.state.alive,
            'resources_reserve': self.state.resources_reserve,
            'reputation': self.state.reputation,
            'request_multiplier': self.state.request_multiplier,
            'negotiation_demand': self.state.negotiation_demand,
            'acceptance_threshold': self.state.acceptance_threshold,
            'greed_index': self.state.greed_index,
        }
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.agent_type}(id={self.id[:8]}, age={self.age}, alive={self.alive})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return (f"{self.__class__.__name__}(id={self.id[:8]}, type={self.agent_type}, "
                f"age={self.age}, alive={self.alive}, reputation={self.reputation:.2f})")
