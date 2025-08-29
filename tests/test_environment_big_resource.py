import pytest
from src.whispers.environment.environment import Environment, Resource


def test_environment_many_resources():
    """Test environment with many resources."""
    env = Environment(width=10, height=10, resource_spawn_rate=100.0)
    env.spawn_resources()
    
    # Should have many resources
    assert len(env.resources) > 10
    
    # All resources should be within bounds
    for resource in env.resources:
        assert 0 <= resource.x < env.width
        assert 0 <= resource.y < env.height


def test_closest_resource_with_many_options():
    """Test finding closest resource when many are available."""
    env = Environment(width=20, height=20)
    
    # Create many resources in a grid pattern
    resources = []
    for x in range(0, 20, 2):
        for y in range(0, 20, 2):
            resources.append(Resource(x, y, 1))
    
    env.resources = resources
    
    # Test finding closest from various positions
    test_positions = [(1, 1), (5, 5), (10, 10), (15, 15)]
    
    for pos_x, pos_y in test_positions:
        closest = env.get_closest_resource(pos_x, pos_y)
        assert closest is not None
        
        # Verify it's actually the closest
        distances = [abs(r.x - pos_x) + abs(r.y - pos_y) for r in env.resources if not r.collected]
        min_distance = min(distances)
        actual_distance = abs(closest.x - pos_x) + abs(closest.y - pos_y)
        assert actual_distance == min_distance


def test_resource_collection_with_many_resources():
    """Test collecting resources when many are available."""
    env = Environment(width=10, height=10)
    
    # Create many resources
    resources = []
    for i in range(50):
        resources.append(Resource(i % 10, i // 10, i + 1))
    
    env.resources = resources
    
    # Collect all resources
    total_value = 0
    for resource in resources:
        value = env.collect_resource(resource)
        total_value += value
        assert resource.collected
    
    # Verify total value
    expected_value = sum(i + 1 for i in range(50))
    assert total_value == expected_value


def test_environment_performance_with_many_resources():
    """Test that environment handles many resources efficiently."""
    env = Environment(width=50, height=50, resource_spawn_rate=500.0)
    
    # Spawn many resources
    env.spawn_resources()
    
    # Should handle many resources without issues
    assert len(env.resources) > 0
    
    # Test finding closest resource multiple times
    for _ in range(100):
        closest = env.get_closest_resource(25, 25)
        if closest is not None:
            # Verify it's within reasonable distance
            distance = abs(closest.x - 25) + abs(closest.y - 25)
            assert distance <= 50  # Should be within grid bounds


