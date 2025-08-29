import pytest

from src.whispers.simulation import Simulation, SimulationConfig
from src.whispers.agents.personality_agents import Altruist


def test_simulation_config_defaults_and_run_zero_days():
    cfg = SimulationConfig()
    assert cfg.num_days >= 0
    sim = Simulation(config=SimulationConfig(num_days=0))
    sim.run()
    assert sim.day == 0


def test_simulation_add_agents_idempotent_and_accessor():
    a1, a2 = Altruist(), Altruist()
    sim = Simulation()
    sim.add_agents([a1])
    sim.add_agents([a2])
    assert len(sim.agents) == 2
    # tuple immutability of accessor
    with pytest.raises(AttributeError):
        sim.agents.append(a1)  # type: ignore[attr-defined]


def test_simulation_multiple_steps_increase_day_correctly():
    sim = Simulation(config=SimulationConfig(num_days=3))
    for _ in range(5):
        sim.step()
    assert sim.day == 5


