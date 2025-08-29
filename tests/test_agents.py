import math
import random
import pytest

from src.whispers.agents.base_agent import BaseAgent
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


class DummyAgent(BaseAgent):
    """Concrete minimal agent to exercise BaseAgent behavior."""

    def __init__(self, **kwargs):
        kwargs.setdefault("agent_type", "dummy")
        super().__init__(**kwargs)

    def calculate_request(self, total_resources: int, population_size: int) -> int:
        return 1

    def negotiate_demand(self, partner_reputation: float) -> float:
        return 0.5

    def will_accept_offer(self, partner_demand: float, partner_reputation: float) -> bool:
        return True


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
def test_personality_agents_calculate_request_and_acceptance(agent_cls):
    random.seed(0)
    agent = agent_cls()
    total_resources = 100
    population = 10

    # Request is a positive integer and at least 1
    req = agent.calculate_request(total_resources, population)
    assert isinstance(req, int)
    assert req >= 1

    # Offers meeting threshold are accepted
    my_threshold = agent.state.acceptance_threshold
    partner_demand = 1.0 - my_threshold
    assert agent.will_accept_offer(partner_demand, partner_reputation=0.5) is True


@pytest.mark.parametrize("agent_cls,low,high", [
    (Altruist, 0.3, 0.7),
    (Egoist, 0.5, 0.9),
    (Pragmatist, 0.4, 0.7),
])
def test_personality_agents_negotiate_demand_ranges(agent_cls, low, high):
    random.seed(1)
    agent = agent_cls()
    d1 = agent.negotiate_demand(partner_reputation=0.2)
    d2 = agent.negotiate_demand(partner_reputation=0.9)
    for d in (d1, d2):
        assert low <= d <= high


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


