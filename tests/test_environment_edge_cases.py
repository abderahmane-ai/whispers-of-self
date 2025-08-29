from src.whispers.environment import ForagingEnvironment, ForagingConfig, BigResourceEnvironment, BigResourceConfig
from src.whispers.agents.personality_agents import Altruist, Egoist


def test_foraging_spawn_resources_zero_and_large():
    env_zero = ForagingEnvironment(ForagingConfig(lambda_supply=0))
    assert env_zero.spawn_resources(day_index=1) == 0

    env_large = ForagingEnvironment(ForagingConfig(lambda_supply=10_000))
    assert env_large.spawn_resources(day_index=2) == 10_000


def test_foraging_allocate_with_no_agents_is_noop():
    env = ForagingEnvironment()
    env.allocate([], supply=100)


def test_big_resource_pair_selection_with_insufficient_agents():
    env = BigResourceEnvironment(BigResourceConfig(probability_big=1.0))
    assert env.select_pair([]) is None

    a = Altruist()
    assert env.select_pair([a]) is None


def test_big_resource_appearance_prob_one_always_true():
    env = BigResourceEnvironment(BigResourceConfig(probability_big=1.0))
    assert env.big_appears(day_index=10) is True


