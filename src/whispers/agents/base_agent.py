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
    reputation: float = 0.5
    harvest_history: List[int] = field(default_factory=list)
    cooperation_history: List[bool] = field(default_factory=list)
    
    # Survival and reproduction economy
    resources_reserve: int = 0
    daily_need: int = 3
    reproduction_reserve: int = 8
    reproduction_cost: int = 8

    # Spatial exploration (discrete grid coordinates)
    position_x: int = 0
    position_y: int = 0
    
    # Strategy parameters
    request_multiplier: float = 1.0
    negotiation_demand: float = 0.5
    acceptance_threshold: float = 0.3
    greed_index: float = 0.5
    
    # Reproduction tracking
    newborn: bool = False


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
    
    def receive_resources(self, amount: int) -> None:
        """Receive resources (from environment/negotiation) and log harvest history."""
        if amount <= 0:
            # Still record zero for history consistency
            self.state.harvest_history.append(0)
        else:
            self.state.resources_reserve += amount
            self.state.harvest_history.append(amount)
            
    def add_resources(self, amount: int) -> None:
        """Backward-compatible alias to receive resources into reserve."""
        self.receive_resources(amount)

        
        # Keep only last 10 harvests for memory
        if len(self.state.harvest_history) > 10:
            self.state.harvest_history.pop(0)
    
    def consume_resources(self, amount: int) -> bool:
        """Consume resources from reserve; return True if fully satisfied."""
        if amount <= 0:
            return True
        if self.state.resources_reserve >= amount:
            self.state.resources_reserve -= amount
            return True
        # Not enough to cover amount
        self.state.resources_reserve = 0
        return False

    def perform_daily_upkeep(self) -> None:
        """Ensure today's collected resources meet daily need; die if insufficient.

        Note: No reserves are carried across days. This method only verifies that
        the agent has collected at least `daily_need` today. Any surplus does not
        roll over and should be reset by `start_new_day`.
        """
        if self.state.resources_reserve < self.state.daily_need:
            self.die()
    
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
        
    def reproduce(self, mutation_rate: float = 0.05) -> Optional['BaseAgent']:
        """
        Create an offspring agent with potential mutations.
        
        Args:
            mutation_rate: Probability of mutation in offspring
            
        Returns:
            New agent instance or None if reproduction fails
        """
        # Gate reproduction on today's collected resources; subclasses should call this method first
        if not self.can_reproduce():
            return None
        # Subclasses create the actual offspring; after success, charge cost
        return None

    def can_reproduce(self) -> bool:
        """Check whether the agent has enough collected today to reproduce."""
        return self.state.alive and self.state.resources_reserve >= self.state.reproduction_reserve

    def charge_reproduction_cost(self) -> None:
        """Deduct reproduction cost from today's collected resources after reproduction."""
        self.consume_resources(self.state.reproduction_cost)

    def start_new_day(self) -> None:
        """Reset per-day resource counters (no reserves carried over)."""
        self.state.resources_reserve = 0
    
    def to_dict(self) -> Dict:
        """Convert agent state to dictionary for serialization."""
        return {
            'id': self.state.id,
            'agent_type': self.state.agent_type,
            'age': self.state.age,
            'alive': self.state.alive,
            'reputation': self.state.reputation,
            'resources_reserve': self.state.resources_reserve,
            'resource_reserve': self.state.resources_reserve,  # alias for compatibility
            'daily_need': self.state.daily_need,
            'request_multiplier': self.state.request_multiplier,
            'negotiation_demand': self.state.negotiation_demand,
            'acceptance_threshold': self.state.acceptance_threshold,
            'greed_index': self.state.greed_index,
            'reproduction_reserve': self.state.reproduction_reserve,
            'reproduction_cost': self.state.reproduction_cost,
        }
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.agent_type}(id={self.id[:8]}, age={self.age}, alive={self.alive})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return (f"{self.__class__.__name__}(id={self.id[:8]}, type={self.agent_type}, "
                f"age={self.age}, alive={self.alive}, reputation={self.reputation:.2f})")

    # --- Exploration and goals ---
    def set_position(self, x: int, y: int) -> None:
        """Set the agent's grid position."""
        self.state.position_x = x
        self.state.position_y = y

    def get_position(self) -> tuple[int, int]:
        """Get the agent's grid position."""
        return (self.state.position_x, self.state.position_y)

    def desired_intake_today(self) -> int:
        """How much the agent strives to collect today based on traits."""
        return max(self.state.daily_need, int(round(self.state.daily_need * self.state.request_multiplier)))