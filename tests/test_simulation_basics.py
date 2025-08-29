import pytest

from src.whispers.simulation import Simulation, SimulationConfig
from src.whispers.agents.personality_agents import Altruist, Egoist, Pragmatist


def test_simulation_initialization_empty():
    sim = Simulation()
    assert sim.day == 0
    assert len(sim.agents) == 0


def test_simulation_add_agents_and_run_steps():
    agents = [Altruist(), Egoist(), Pragmatist()]
    sim = Simulation(agents=agents, config=SimulationConfig(num_days=2))
    assert len(sim.agents) == 3

    sim.step()
    assert sim.day == 1

    sim.run()
    # After run() of 2 days starting from day=1, final day should be 3
    assert sim.day == 3


