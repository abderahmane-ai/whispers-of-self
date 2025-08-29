from src.whispers.environment import ForagingEnvironment, ForagingConfig


def test_foraging_spawn_resources_fixed():
    env = ForagingEnvironment(ForagingConfig(lambda_supply=25))
    supply = env.spawn_resources(day_index=0)
    assert supply == 25


def test_foraging_allocate_noop():
    env = ForagingEnvironment()
    env.allocate([], supply=10)  # should be a no-op for now


