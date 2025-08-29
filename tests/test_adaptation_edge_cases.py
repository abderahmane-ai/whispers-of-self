import pytest
from src.whispers.adaptation import Evolution, EvolutionConfig, Imitation, ImitationConfig
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


def test_evolution_config_edge_cases():
    """Test EvolutionConfig with edge case values."""
    # Zero mutation rate
    config = EvolutionConfig(mutation_rate=0.0)
    assert config.mutation_rate == 0.0
    
    # Very high mutation rate
    config = EvolutionConfig(mutation_rate=1.0)
    assert config.mutation_rate == 1.0
    
    # Negative max offspring (should be allowed for config)
    config = EvolutionConfig(max_offspring_per_day=-1)
    assert config.max_offspring_per_day == -1


def test_imitation_config_edge_cases():
    """Test ImitationConfig with edge case values."""
    # Zero copy interval
    config = ImitationConfig(copy_interval_days=0)
    assert config.copy_interval_days == 0
    
    # Very large copy interval
    config = ImitationConfig(copy_interval_days=1000)
    assert config.copy_interval_days == 1000
    
    # Negative copy interval
    config = ImitationConfig(copy_interval_days=-5)
    assert config.copy_interval_days == -5


def test_evolution_with_none_config():
    """Test Evolution initialization with None config."""
    evolution = Evolution(config=None)
    assert evolution.config is not None
    assert evolution.config.mutation_rate == 0.05
    assert evolution.config.max_offspring_per_day == 0


def test_imitation_with_none_config():
    """Test Imitation initialization with None config."""
    imitation = Imitation(config=None)
    assert imitation.config is not None
    assert imitation.config.copy_interval_days == 0


def test_evolution_reproduction_with_none_agents():
    """Test evolution reproduction with None agents."""
    evolution = Evolution()
    
    # Should handle None gracefully
    offspring = evolution.reproduce(None)
    assert isinstance(offspring, list)
    assert len(offspring) == 0


def test_imitation_maybe_copy_with_none_agents():
    """Test imitation maybe_copy with None agents."""
    imitation = Imitation()
    
    # Should handle None gracefully
    result = imitation.maybe_copy(day_index=5, agents=None)
    assert result is None


def test_evolution_reproduction_with_dead_agents():
    """Test evolution reproduction with dead agents."""
    evolution = Evolution()
    
    # Create some dead agents
    dead_altruist = Altruist()
    dead_altruist.die()
    
    dead_egoist = Egoist()
    dead_egoist.die()
    
    agents = [dead_altruist, dead_egoist, Pragmatist()]  # Mix of dead and alive
    
    offspring = evolution.reproduce(agents)
    assert len(offspring) == 0  # Baseline returns empty


def test_imitation_maybe_copy_with_dead_agents():
    """Test imitation maybe_copy with dead agents."""
    imitation = Imitation()
    
    # Create some dead agents
    dead_altruist = Altruist()
    dead_altruist.die()
    
    agents = [dead_altruist, Egoist(), Pragmatist()]
    
    result = imitation.maybe_copy(day_index=10, agents=agents)
    assert result is None  # Baseline does nothing


def test_adaptation_with_very_large_agent_lists():
    """Test adaptation with very large agent lists."""
    evolution = Evolution()
    imitation = Imitation()
    
    # Create many agents
    agents = [Altruist() for _ in range(1000)]
    
    # Should handle large lists without issues
    offspring = evolution.reproduce(agents)
    assert len(offspring) == 0
    
    result = imitation.maybe_copy(day_index=50, agents=agents)
    assert result is None


def test_adaptation_with_negative_day_indices():
    """Test adaptation with negative day indices."""
    imitation = Imitation()
    agents = [Altruist(), Egoist()]
    
    # Should handle negative day indices
    result = imitation.maybe_copy(day_index=-1, agents=agents)
    assert result is None
    
    result = imitation.maybe_copy(day_index=-100, agents=agents)
    assert result is None


