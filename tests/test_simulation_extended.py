import pytest
from src.whispers.simulation.simulation import Simulation, SimulationConfig
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


def test_simulation_with_many_agents():
    """Test simulation with many agents."""
    agents = [Altruist() for _ in range(50)] + [Egoist() for _ in range(30)] + [Pragmatist() for _ in range(20)]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=5))
    
    assert len(sim.agents) == 100
    
    # Run simulation
    sim.run()
    assert sim.day == 5


def test_simulation_agent_lifecycle():
    """Test simulation with agent lifecycle events."""
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=3))
    
    # All agents should start alive
    assert all(agent.alive for agent in sim.agents)
    
    # Kill one agent
    agents[0].die()
    assert not agents[0].alive
    assert agents[1].alive
    assert agents[2].alive
    
    # Run simulation
    sim.run()
    assert sim.day == 3


def test_simulation_resource_management():
    """Test simulation with resource management."""
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=2))
    
    # Give agents some resources
    for agent in agents:
        agent.receive_resources(10)
    
    # Verify resources are received
    for agent in agents:
        assert agent.state.resources_reserve == 10
    
    # Run simulation
    sim.run()
    assert sim.day == 2


def test_simulation_agent_aging():
    """Test simulation with agent aging."""
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=5))
    
    # All agents should start at age 0
    assert all(agent.age == 0 for agent in agents)
    
    # Age agents manually
    for agent in agents:
        agent.age_step()
    
    # Verify aging
    assert all(agent.age == 1 for agent in agents)
    
    # Run simulation
    sim.run()
    assert sim.day == 5


def test_simulation_reputation_tracking():
    """Test simulation with reputation tracking."""
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=3))
    
    # Update reputations
    for agent in agents:
        agent.update_reputation(True)
        agent.update_reputation(False)
        agent.update_reputation(True)
    
    # Verify reputation updates
    for agent in agents:
        assert 0.0 <= agent.reputation <= 1.0
        assert len(agent.state.cooperation_history) == 3
    
    # Run simulation
    sim.run()
    assert sim.day == 3


def test_simulation_agent_positions():
    """Test simulation with agent position tracking."""
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=2))
    
    # Set agent positions
    positions = [(1, 1), (5, 5), (10, 10)]
    for agent, pos in zip(agents, positions):
        agent.set_position(*pos)
    
    # Verify positions
    for agent, expected_pos in zip(agents, positions):
        assert agent.get_position() == expected_pos
    
    # Run simulation
    sim.run()
    assert sim.day == 2


def test_simulation_daily_upkeep():
    """Test simulation with daily upkeep mechanics."""
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=2))
    
    # Give some agents insufficient resources
    agents[0].receive_resources(2)  # Less than daily_need (3)
    agents[1].receive_resources(3)  # Equal to daily_need
    agents[2].receive_resources(5)  # More than daily_need
    
    # Perform daily upkeep
    for agent in agents:
        agent.perform_daily_upkeep()
    
    # Verify survival based on resources
    assert not agents[0].alive  # Insufficient resources
    assert agents[1].alive      # Sufficient resources
    assert agents[2].alive      # Sufficient resources
    
    # Run simulation
    sim.run()
    assert sim.day == 2


def test_simulation_reproduction_logic():
    """Test simulation with reproduction mechanics."""
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=2))
    
    # Give agents enough resources for reproduction
    for agent in agents:
        agent.receive_resources(15)  # More than reproduction_reserve (8)
    
    # Test reproduction capability
    for agent in agents:
        assert agent.can_reproduce()
    
    # Test reproduction cost charging
    for agent in agents:
        initial_resources = agent.state.resources_reserve
        assert agent.state.resources_reserve == initial_resources - agent.state.reproduction_cost
    
    # Run simulation
    sim.run()
    assert sim.day == 2


