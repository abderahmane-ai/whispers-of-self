#!/usr/bin/env python3
"""
Test script for Rich CLI visualization in Whispers of Self simulation.

This script demonstrates the new Rich-based visualization capabilities
that replace the previous Solara web-based visualization.
"""

from src.whispers.simulation.simulation import Simulation, SimulationConfig
from src.whispers.agents.base_agent import BaseAgent
from rich.console import Console
from rich.panel import Panel

def create_test_agents(num_agents: int = 5) -> list[BaseAgent]:
    """Create test agents for demonstration."""
    agents = []
    for i in range(num_agents):
        agent = BaseAgent(f"test_agent_{i}")
        agent.agent_type = f"Type_{i % 3}"  # Different types for variety
        agent.age = i + 1
        # Set some resources
        if hasattr(agent, 'state'):
            agent.state.resources_reserve = (i + 1) * 10
        agents.append(agent)
    return agents

def main():
    """Main demonstration function."""
    console = Console()
    
    console.print(Panel("[bold green]Whispers of Self - Rich CLI Visualization Demo[/bold green]", style="green"))
    console.print("\nThis demo shows the new Rich-based CLI visualization capabilities.")
    console.print("The simulation will run with live progress bars, status tables, and dynamic updates.\n")
    
    # Create test agents
    agents = create_test_agents(8)
    console.print(f"Created {len(agents)} test agents for demonstration.\n")
    
    # Configure simulation
    config = SimulationConfig(
        num_days=15,
        daily_resource_budget=100,
        enable_visualization=True,
        update_interval=0.2  # Slower updates for demo
    )
    
    # Create and run simulation
    simulation = Simulation(agents, config)
    
    console.print("Starting simulation with Rich CLI visualization...\n")
    
    # Run the simulation
    simulation.run()
    
    console.print("\n" + "="*60)
    console.print("Demo completed! The Rich CLI visualization provides:")
    console.print("• Live progress bars with spinners and time tracking")
    console.print("• Dynamic status tables showing agent statistics")
    console.print("• Real-time updates during simulation execution")
    console.print("• Beautiful final summary with agent breakdowns")
    console.print("• Interactive mode for step-by-step execution")
    console.print("="*60)

if __name__ == "__main__":
    main()
