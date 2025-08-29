import math
import pytest

from src.whispers.agents.base_agent import BaseAgent
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


class DummyAgent(BaseAgent):
    """Concrete minimal agent to exercise BaseAgent behavior."""

    def __init__(self, **kwargs):
        kwargs.setdefault("agent_type", "dummy")
        super().__init__(**kwargs)


def test_base_agent_state_and_resources():
    agent = DummyAgent()

    # Age and alive flags
    assert agent.age == 0 and agent.alive is True
    agent.age_step()
    assert agent.age == 1
    agent.die()
    assert agent.alive is False

    # Resources accounting and harvest history window (last 10 kept)
    total_added = 0
    for i in range(15):
        agent.receive_resources(1)
        total_added += 1
    assert agent.state.resources_reserve == total_added
    assert len(agent.state.harvest_history) == 10
    assert all(x == 1 for x in agent.state.harvest_history)

    # Consumption
    assert agent.consume_resources(5) is True
    assert agent.state.resources_reserve == total_added - 5
    assert agent.consume_resources(10**9) is False


def test_base_agent_reputation_and_average_harvest():
    agent = DummyAgent()

    # Reputation updates as moving average with smoothing
    start_rep = agent.reputation
    for outcome in [True, True, False, True, False, False, True]:
        agent.update_reputation(outcome)
    assert 0.0 <= agent.reputation <= 1.0
    assert agent.reputation != start_rep

    # Average harvest with no history defaults sensibly
    empty_agent = DummyAgent()
    assert empty_agent.get_average_harvest() == 0.0

    # Average harvest over window
    for v in [1, 3, 5, 7, 9]:
        empty_agent.receive_resources(v)
    avg5 = empty_agent.get_average_harvest(days=5)
    assert isinstance(avg5, float)
    assert math.isclose(avg5, (1 + 3 + 5 + 7 + 9) / 5)


def test_base_agent_position_and_movement():
    agent = DummyAgent()
    
    # Test position setting and getting
    agent.set_position(5, 10)
    assert agent.get_position() == (5, 10)
    
    # Test position updates
    agent.set_position(15, 20)
    assert agent.get_position() == (15, 20)


def test_base_agent_daily_upkeep_and_survival():
    agent = DummyAgent()
    
    # Agent should die if resources < daily_need
    agent.receive_resources(2)  # Less than daily_need (3)
    agent.perform_daily_upkeep()
    assert not agent.alive
    
    # Agent should survive if resources >= daily_need
    agent2 = DummyAgent()
    agent2.receive_resources(3)  # Equal to daily_need
    agent2.perform_daily_upkeep()
    assert agent2.alive
    
    agent3 = DummyAgent()
    agent3.receive_resources(5)  # More than daily_need
    agent3.perform_daily_upkeep()
    assert agent3.alive


def test_base_agent_reproduction_logic():
    agent = DummyAgent()
    
    # Can't reproduce without enough resources
    assert not agent.can_reproduce()
    
    # Can reproduce with enough resources
    agent.receive_resources(15)  # More than reproduction_reserve (8)
    assert agent.can_reproduce()
    
    # Reproduction cost is charged
    initial_resources = agent.state.resources_reserve
    agent.charge_reproduction_cost()
    assert agent.state.resources_reserve == initial_resources - agent.state.reproduction_cost


def test_base_agent_new_day_reset():
    agent = DummyAgent()
    agent.receive_resources(10)
    assert agent.state.resources_reserve == 10
    
    agent.start_new_day()
    assert agent.state.resources_reserve == 0


@pytest.mark.parametrize("agent_cls", [Altruist, Egoist, Pragmatist])
def test_personality_agents_desired_intake_at_least_daily_need(agent_cls):
    agent = agent_cls()
    desired = agent.desired_intake_today()
    assert isinstance(desired, int)
    assert desired >= agent.state.daily_need


def test_personality_agents_initialization():
    altruist = Altruist()
    egoist = Egoist()
    pragmatist = Pragmatist()
    
    # Check that each has the correct agent type
    assert altruist.agent_type == "altruist"
    assert egoist.agent_type == "egoist"
    assert pragmatist.agent_type == "pragmatist"
    
    # Check that they have different characteristics
    assert altruist.state.greed_index < egoist.state.greed_index
    assert altruist.state.request_multiplier < egoist.state.request_multiplier


def test_to_dict_contains_key_fields():
    agent = Altruist()
    data = agent.to_dict()
    for key in [
        "id",
        "agent_type",
        "age",
        "alive",
        "resources_reserve",
        "reputation",
        "request_multiplier",
        "negotiation_demand",
        "acceptance_threshold",
        "greed_index",
        "reproduction_reserve",
        "reproduction_cost",
    ]:
        assert key in data


def test_agent_string_representations():
    agent = DummyAgent()
    
    # Test __str__
    str_repr = str(agent)
    assert "dummy" in str_repr
    assert agent.id[:8] in str_repr
    
    # Test __repr__
    repr_str = repr(agent)
    assert "DummyAgent" in repr_str
    assert agent.id[:8] in repr_str
    assert "dummy" in repr_str


