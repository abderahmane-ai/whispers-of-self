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
        agent.add_resources(1)
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
        empty_agent.add_resources(v)
    avg5 = empty_agent.get_average_harvest(days=5)
    assert isinstance(avg5, float)
    assert math.isclose(avg5, (1 + 3 + 5 + 7 + 9) / 5)


@pytest.mark.parametrize("agent_cls", [Altruist, Egoist, Pragmatist])
def test_personality_agents_desired_intake_at_least_daily_need(agent_cls):
    agent = agent_cls()
    desired = agent.desired_intake_today()
    assert isinstance(desired, int)
    assert desired >= agent.state.daily_need


def test_no_negotiation_interfaces_present():
    agent = Altruist()
    assert not hasattr(agent, "calculate_request")
    assert not hasattr(agent, "negotiate_demand")
    assert not hasattr(agent, "will_accept_offer")


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
    ]:
        assert key in data


