import pytest

from src.whispers.simulation.simulation import Simulation, SimulationConfig
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


def test_simulation_initialization_empty():
    sim = Simulation()
    assert sim.day == 0
    assert len(sim.agents) == 0


def test_simulation_add_agents_and_run_steps():
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=2))
    assert len(sim.agents) == 3

    sim.step()
    assert sim.day == 1

    sim.run()
    # After run() of 2 days starting from day=1, final day should be 3
    assert sim.day == 3


def test_simulation_config_defaults():
    config = SimulationConfig()
    assert config.num_days == 30
    assert config.daily_resource_budget == 0


def test_simulation_config_custom():
    config = SimulationConfig(num_days=10, daily_resource_budget=100)
    assert config.num_days == 10
    assert config.daily_resource_budget == 100


def test_simulation_add_agents_dynamically():
    sim = Simulation()
    assert len(sim.agents) == 0
    
    agents = [Altruist(), Egoist()]
    sim.add_agents(agents)
    assert len(sim.agents) == 2
    
    sim.add_agents([Pragmatist()])
    assert len(sim.agents) == 3


def test_simulation_agents_property_immutable():
    sim = Simulation(agents=[Altruist()])
    agents = sim.agents
    
    # Should be a tuple (immutable)
    assert isinstance(agents, tuple)
    assert len(agents) == 1
    
    # Original list should not be modified
    original_agents = list(sim.agents)
    sim.add_agents([Egoist()])
    assert len(original_agents) == 1  # Original list unchanged
    assert len(sim.agents) == 2  # New agents added


def test_simulation_step_advances_day():
    sim = Simulation()
    initial_day = sim.day
    
    sim.step()
    assert sim.day == initial_day + 1
    
    sim.step()
    assert sim.day == initial_day + 2


