import pytest
from src.whispers.adaptation import Evolution, EvolutionConfig, Imitation, ImitationConfig
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


def test_evolution_config_defaults():
    """Test EvolutionConfig default values."""
    config = EvolutionConfig()
    assert config.mutation_rate == 0.05
    assert config.max_offspring_per_day == 0


def test_evolution_config_custom():
    """Test EvolutionConfig with custom values."""
    config = EvolutionConfig(mutation_rate=0.1, max_offspring_per_day=5)
    assert config.mutation_rate == 0.1
    assert config.max_offspring_per_day == 5


def test_evolution_initialization():
    """Test Evolution class initialization."""
    config = EvolutionConfig(mutation_rate=0.1)
    evolution = Evolution(config)
    assert evolution.config.mutation_rate == 0.1
    
    # Test with default config
    evolution_default = Evolution()
    assert evolution_default.config.mutation_rate == 0.05


def test_evolution_reproduction_baseline():
    """Test that evolution returns empty list in baseline."""
    evolution = Evolution()
    agents = [Altruist(), Egoist(), Pragmatist()]
    
    offspring = evolution.reproduce(agents)
    assert isinstance(offspring, list)
    assert len(offspring) == 0


def test_imitation_config_defaults():
    """Test ImitationConfig default values."""
    config = ImitationConfig()
    assert config.copy_interval_days == 0


def test_imitation_config_custom():
    """Test ImitationConfig with custom values."""
    config = ImitationConfig(copy_interval_days=5)
    assert config.copy_interval_days == 5


def test_imitation_initialization():
    """Test Imitation class initialization."""
    config = ImitationConfig(copy_interval_days=3)
    imitation = Imitation(config)
    assert imitation.config.copy_interval_days == 3
    
    # Test with default config
    imitation_default = Imitation()
    assert imitation_default.config.copy_interval_days == 0


def test_imitation_maybe_copy_baseline():
    """Test that imitation does nothing in baseline."""
    imitation = Imitation()
    agents = [Altruist(), Egoist(), Pragmatist()]
    
    # Should return None and not modify agents
    result = imitation.maybe_copy(day_index=5, agents=agents)
    assert result is None
    assert len(agents) == 3  # Agents unchanged


def test_adaptation_with_different_agent_types():
    """Test adaptation with different agent types."""
    evolution = Evolution()
    imitation = Imitation()
    
    # Mix of different agent types
    agents = [
        Altruist(),
        Egoist(),
        Pragmatist(),
        Altruist(),
        Egoist()
    ]
    
    # Evolution should return empty list
    offspring = evolution.reproduce(agents)
    assert len(offspring) == 0
    
    # Imitation should do nothing
    result = imitation.maybe_copy(day_index=10, agents=agents)
    assert result is None


def test_adaptation_edge_cases():
    """Test adaptation with edge cases."""
    evolution = Evolution()
    imitation = Imitation()
    
    # Empty agent list
    empty_agents = []
    offspring = evolution.reproduce(empty_agents)
    assert len(offspring) == 0
    
    result = imitation.maybe_copy(day_index=0, agents=empty_agents)
    assert result is None
    
    # Single agent
    single_agent = [Altruist()]
    offspring = evolution.reproduce(single_agent)
    assert len(offspring) == 0
    
    result = imitation.maybe_copy(day_index=1, agents=single_agent)
    assert result is None


