"""
Environment class for the Whispers of Self simulation.

This module provides the spatial environment where agents interact,
resources spawn, and agents navigate to find resources.
"""

import random
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


@dataclass
class Resource:
    """Represents a resource in the environment."""
    x: int
    y: int
    value: int
    collected: bool = False
    
    def __str__(self) -> str:
        return f"Resource({self.x}, {self.y}, value={self.value})"


class Environment:
    """
    Spatial environment where agents navigate and collect resources.
    
    The environment is a discrete grid where:
    - Resources spawn randomly each day
    - Agents can move to adjacent cells
    - Agents can see all resources and navigate to the closest one
    """
    
    def __init__(self, width: int = 20, height: int = 20, resource_spawn_rate: float = 25.0):
        """
        Initialize the environment.
        
        Args:
            width: Width of the environment grid
            height: Height of the environment grid
            resource_spawn_rate: Average number of resources to spawn per day (Poisson)
        """
        self.width = width
        self.height = height
        self.resource_spawn_rate = resource_spawn_rate
        self.resources: List[Resource] = []
        self.console = Console()
        
    def spawn_resources(self) -> None:
        """Spawn new resources randomly across the environment."""
        # Clear old resources
        self.resources = []
        
        # Calculate target number of resources based on spawn rate
        target_resources = int(self.resource_spawn_rate * self.width * self.height)
        
        # Ensure minimum viable resources for survival
        min_resources = max(5, target_resources)  # At least 5 resources for basic survival
        
        # Spawn resources at random positions
        for _ in range(min_resources):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            value = 1  # All resources are worth 1
            self.resources.append(Resource(x, y, value))
        
        # Debug logging
        if hasattr(self, 'console'):
            self.console.print(f"[dim]Spawned {min_resources} resources (target: {target_resources}, rate: {self.resource_spawn_rate:.3f})[/dim]")
    
    def get_closest_resource(self, agent_x: int, agent_y: int) -> Optional[Resource]:
        """
        Find the closest uncollected resource to the agent.
        
        Args:
            agent_x: Agent's x position
            agent_y: Agent's y position
            
        Returns:
            Closest uncollected resource or None if no resources available
        """
        available_resources = [r for r in self.resources if not r.collected]
        
        if not available_resources:
            return None
        
        # Find closest resource using Manhattan distance
        closest = min(available_resources, 
                     key=lambda r: abs(r.x - agent_x) + abs(r.y - agent_y))
        return closest
    
    def collect_resource(self, resource: Resource) -> int:
        """
        Collect a resource and return its value.
        
        Args:
            resource: The resource to collect
            
        Returns:
            The value of the collected resource
        """
        if resource.collected:
            return 0
        
        resource.collected = True
        return resource.value
    
    def get_available_resources(self) -> List[Resource]:
        """Get all uncollected resources."""
        return [r for r in self.resources if not r.collected]
    
    def get_total_resources(self) -> int:
        """Get total number of resources (collected + uncollected)."""
        return len(self.resources)
    
    def get_collected_resources(self) -> int:
        """Get number of collected resources."""
        return sum(1 for r in self.resources if r.collected)
    
    def display(self, agent_positions: Dict[str, Tuple[int, int]] = None, agent_types: Dict[str, str] = None, agent_info: Dict[str, dict] = None) -> None:
        """
        Display the environment grid with resources and agents.
        
        Args:
            agent_positions: Dictionary mapping agent IDs to their positions
            agent_types: Dictionary mapping agent IDs to their types for different symbols
            agent_info: Dictionary mapping agent IDs to additional info (e.g., newborn status)
        """
        if agent_positions is None:
            agent_positions = {}
        if agent_types is None:
            agent_types = {}
        if agent_info is None:
            agent_info = {}
        
        # Create grid representation
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place resources
        for resource in self.resources:
            if not resource.collected:
                grid[resource.y][resource.x] = f'{resource.value}'
        
        # Place agents with type-specific symbols
        for agent_id, (x, y) in agent_positions.items():
            if 0 <= x < self.width and 0 <= y < self.height:
                agent_type = agent_types.get(agent_id, 'unknown')
                agent_data = agent_info.get(agent_id, {})
                newborn = agent_data.get('newborn', False)
                
                if agent_type == 'altruist':
                    grid[y][x] = 'a' if newborn else 'A'  # Lowercase for newborn altruist
                elif agent_type == 'egoist':
                    grid[y][x] = 'e' if newborn else 'E'  # Lowercase for newborn egoist
                elif agent_type == 'pragmatist':
                    grid[y][x] = 'p' if newborn else 'P'  # Lowercase for newborn pragmatist
                else:
                    grid[y][x] = 'a' if newborn else 'A'  # Default agent symbol
        
        # Create table
        table = Table(title=f"Environment (Available Resources: {len(self.get_available_resources())})")
        
        # Add columns
        for i in range(self.width):
            table.add_column(f"{i}", justify="center", style="bold")
        
        # Add rows
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = grid[y][x]
                if cell == 'A':
                    row.append(Text("A", style="bold green"))  # Altruist
                elif cell == 'a':
                    row.append(Text("a", style="bold green"))  # Newborn Altruist
                elif cell == 'E':
                    row.append(Text("E", style="bold red"))   # Egoist
                elif cell == 'e':
                    row.append(Text("e", style="bold red"))   # Newborn Egoist
                elif cell == 'P':
                    row.append(Text("P", style="bold yellow")) # Pragmatist
                elif cell == 'p':
                    row.append(Text("p", style="bold yellow")) # Newborn Pragmatist
                elif cell.isdigit():
                    row.append(Text(cell, style="bold green"))
                else:
                    row.append("·")
            table.add_row(*row)
        
        self.console.print(table)
        
        # Display legend
        legend = Table.grid()
        legend.add_column()
        legend.add_column()
        legend.add_row("A ", "Altruist Agent")
        legend.add_row("a ", "Newborn Altruist")
        legend.add_row("E ", "Egoist Agent")
        legend.add_row("e ", "Newborn Egoist")
        legend.add_row("P ", "Pragmatist Agent")
        legend.add_row("p ", "Newborn Pragmatist")
        legend.add_row("1 ", "Resource (value=1)")
        legend.add_row("· ", "Empty space")
        
        self.console.print(Panel(legend, title="Legend"))
    
    def get_display_string(self, agent_positions: Dict[str, Tuple[int, int]] = None, agent_types: Dict[str, str] = None, agent_info: Dict[str, dict] = None) -> str:
        """
        Get the environment display as a string for real-time updates.
        
        Args:
            agent_positions: Dictionary mapping agent IDs to their positions
            agent_types: Dictionary mapping agent IDs to their types for different symbols
            agent_info: Dictionary mapping agent IDs to additional info (e.g., newborn status)
            
        Returns:
            String representation of the environment display
        """
        if agent_positions is None:
            agent_positions = {}
        if agent_types is None:
            agent_types = {}
        if agent_info is None:
            agent_info = {}
        
        # Create grid representation
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place resources
        for resource in self.resources:
            if not resource.collected:
                grid[resource.y][resource.x] = f'{resource.value}'
        
        # Place agents with type-specific symbols
        for agent_id, (x, y) in agent_positions.items():
            if 0 <= x < self.width and 0 <= y < self.height:
                agent_type = agent_types.get(agent_id, 'unknown')
                agent_data = agent_info.get(agent_id, {})
                newborn = agent_data.get('newborn', False)
                
                if agent_type == 'altruist':
                    grid[y][x] = 'a' if newborn else 'A'  # Lowercase for newborn altruist
                elif agent_type == 'egoist':
                    grid[y][x] = 'e' if newborn else 'E'  # Lowercase for newborn egoist
                elif agent_type == 'pragmatist':
                    grid[y][x] = 'p' if newborn else 'P'  # Lowercase for newborn pragmatist
                else:
                    grid[y][x] = 'a' if newborn else 'A'  # Default agent symbol
        
        # Build the display string
        lines = []
        lines.append(f"Environment (Available Resources: {len(self.get_available_resources())})")
        lines.append("=" * (self.width * 3 + 10))
        
        # Add column headers
        header = "   " + " ".join(f"{i:2}" for i in range(self.width))
        lines.append(header)
        lines.append("-" * len(header))
        
        # Add rows
        for y in range(self.height):
            row = f"{y:2} |"
            for x in range(self.width):
                cell = grid[y][x]
                if cell == 'A':
                    row += " A "
                elif cell.isdigit():
                    row += f" {cell} "
                else:
                    row += " · "
            lines.append(row)
        
        # Add legend
        lines.append("")
        lines.append("Legend:")
        lines.append("A = Agent")
        lines.append("1 = Resource (value=1)")
        lines.append("· = Empty space")
        
        return "\n".join(lines)
    
    def get_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate Manhattan distance between two points."""
        return abs(x2 - x1) + abs(y2 - y1)
