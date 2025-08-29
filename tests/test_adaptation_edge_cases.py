import pytest

from src.whispers.adaptation import Evolution, EvolutionConfig, Imitation, ImitationConfig
from src.whispers.agents.personality_agents import Altruist


def test_evolution_config_defaults_and_reproduce_types():
    cfg = EvolutionConfig()
    assert 0.0 <= cfg.mutation_rate <= 1.0
    assert cfg.max_offspring_per_day >= 0

    evo = Evolution(cfg)
    offspring = evo.reproduce([Altruist()])
    assert isinstance(offspring, (list, tuple))


def test_imitation_copy_schedule_noop_before_interval():
    cfg = ImitationConfig(copy_interval_days=5)
    imi = Imitation(cfg)
    # day 0 should not error and is a no-op
    imi.maybe_copy(day_index=0, agents=[Altruist()])
    # non-multiple also no-op for now
    imi.maybe_copy(day_index=3, agents=[Altruist()])


