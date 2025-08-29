from src.whispers.environment import BigResourceEnvironment, BigResourceConfig
from src.whispers.agents.personality_agents import Altruist, Egoist


def test_big_resource_always_appears_when_prob_one():
    env = BigResourceEnvironment(BigResourceConfig(probability_big=1.0))
    assert env.big_appears(day_index=0) is True


def test_select_pair_returns_first_two():
    env = BigResourceEnvironment()
    a1, a2 = Altruist(), Egoist()
    pair = env.select_pair([a1, a2])
    assert pair == (a1, a2)


