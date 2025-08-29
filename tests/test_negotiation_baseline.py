import pytest
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


def test_agent_negotiation_parameters():
    """Test that agents have negotiation parameters."""
    altruist = Altruist()
    egoist = Egoist()
    pragmatist = Pragmatist()
    
    # All agents should have negotiation parameters
    for agent in [altruist, egoist, pragmatist]:
        assert hasattr(agent.state, 'request_multiplier')
        assert hasattr(agent.state, 'negotiation_demand')
        assert hasattr(agent.state, 'acceptance_threshold')
        assert hasattr(agent.state, 'greed_index')
        
        # Parameters should be within reasonable bounds
        assert 0.0 <= agent.state.request_multiplier <= 2.0
        assert 0.0 <= agent.state.negotiation_demand <= 1.0
        assert 0.0 <= agent.state.acceptance_threshold <= 1.0
        assert 0.0 <= agent.state.greed_index <= 1.0


def test_agent_personality_differences():
    """Test that different agent types have different negotiation characteristics."""
    altruist = Altruist()
    egoist = Egoist()
    pragmatist = Pragmatist()
    
    # Altruists should be more cooperative than egoists
    assert altruist.state.greed_index < egoist.state.greed_index
    assert altruist.state.request_multiplier < egoist.state.request_multiplier
    
    # Egoists should be more demanding than altruists
    assert egoist.state.negotiation_demand > altruist.state.negotiation_demand
    
    # Pragmatists should be in the middle
    assert altruist.state.greed_index < pragmatist.state.greed_index < egoist.state.greed_index


def test_agent_desired_intake_calculation():
    """Test that agents calculate desired intake based on their traits."""
    altruist = Altruist()
    egoist = Egoist()
    pragmatist = Pragmatist()
    
    # All agents should have a desired intake method
    for agent in [altruist, egoist, pragmatist]:
        desired = agent.desired_intake_today()
        assert isinstance(desired, int)
        assert desired >= agent.state.daily_need
        
        # Desired intake should be influenced by request_multiplier
        expected_min = agent.state.daily_need
        expected_max = int(agent.state.daily_need * agent.state.request_multiplier)
        assert expected_min <= desired <= expected_max


def test_agent_reputation_mechanism():
    """Test that agents can update their reputation based on cooperation."""
    agent = Altruist()
    initial_reputation = agent.reputation
    
    # Test reputation updates
    agent.update_reputation(True)   # Successful cooperation
    assert agent.reputation > initial_reputation
    
    agent.update_reputation(False)  # Failed cooperation
    assert agent.reputation < agent.reputation  # Should decrease
    
    # Reputation should stay within bounds
    assert 0.0 <= agent.reputation <= 1.0


def test_agent_cooperation_history():
    """Test that agents track their cooperation history."""
    agent = Altruist()
    
    # Initially no cooperation history
    assert len(agent.state.cooperation_history) == 0
    
    # Add some cooperation events
    for i in range(25):  # More than the 20 limit
        agent.update_reputation(i % 2 == 0)  # Alternate True/False
    
    # Should keep only last 20 events
    assert len(agent.state.cooperation_history) == 20
    
    # Verify the last few events
    assert agent.state.cooperation_history[-1] is False  # Last event was False
    assert agent.state.cooperation_history[-2] is True   # Second to last was True


def test_agent_harvest_history():
    """Test that agents track their harvest history."""
    agent = Altruist()
    
    # Initially no harvest history
    assert len(agent.state.harvest_history) == 0
    
    # Add some harvests
    for i in range(15):  # More than the 10 limit
        agent.receive_resources(i + 1)
    
    # Should keep only last 10 harvests
    assert len(agent.state.harvest_history) == 10
    
    # Verify the last few harvests
    assert agent.state.harvest_history[-1] == 15  # Last harvest was 15
    assert agent.state.harvest_history[-2] == 14  # Second to last was 14


def test_agent_average_harvest_calculation():
    """Test that agents can calculate average harvest over time."""
    agent = Altruist()
    
    # No history should return 0
    assert agent.get_average_harvest() == 0.0
    
    # Add some harvests
    harvests = [1, 3, 5, 7, 9]
    for harvest in harvests:
        agent.receive_resources(harvest)
    
    # Calculate average over different periods
    avg_all = agent.get_average_harvest(days=5)
    assert avg_all == sum(harvests) / len(harvests)
    
    avg_recent = agent.get_average_harvest(days=3)
    assert avg_recent == sum(harvests[-3:]) / 3


