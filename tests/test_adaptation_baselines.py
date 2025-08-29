from src.whispers.adaptation import Evolution, EvolutionConfig, Imitation, ImitationConfig
from src.whispers.agents.personality_agents import Altruist


def test_evolution_reproduce_empty_returns_empty():
    evo = Evolution(EvolutionConfig())
    offspring = evo.reproduce([])
    assert isinstance(offspring, list) or isinstance(offspring, tuple)
    assert len(offspring) == 0


def test_imitation_maybe_copy_noop():
    imi = Imitation(ImitationConfig())
    imi.maybe_copy(day_index=0, agents=[Altruist()])


