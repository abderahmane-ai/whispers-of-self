import pytest
from src.whispers.environment.environment import Environment, Resource


def test_environment_zero_dimensions():
    """Test environment with zero dimensions."""
    env = Environment(width=0, height=0)
    assert env.width == 0
    assert env.height == 0
    
    # Spawning resources should handle zero dimensions gracefully
    env.spawn_resources()
    assert len(env.resources) == 0


def test_environment_single_cell():
    """Test environment with single cell."""
    env = Environment(width=1, height=1)
    env.spawn_resources()
    
    # All resources should be at (0, 0)
    for resource in env.resources:
        assert resource.x == 0
        assert resource.y == 0


def test_environment_very_large():
    """Test environment with very large dimensions."""
    env = Environment(width=1000, height=1000)
    assert env.width == 1000
    assert env.height == 1000
    
    # Should handle large dimensions without issues
    env.spawn_resources()
    assert len(env.resources) >= 0


def test_environment_zero_spawn_rate():
    """Test environment with zero spawn rate."""
    env = Environment(resource_spawn_rate=0.0)
    env.spawn_resources()
    
    # Should spawn no resources
    assert len(env.resources) == 0


def test_environment_very_high_spawn_rate():
    """Test environment with very high spawn rate."""
    env = Environment(width=5, height=5, resource_spawn_rate=1000.0)
    env.spawn_resources()
    
    # Should handle high spawn rates gracefully
    assert len(env.resources) >= 0


def test_closest_resource_edge_cases():
    """Test edge cases for finding closest resource."""
    env = Environment(width=5, height=5)
    
    # No resources
    closest = env.get_closest_resource(2, 2)
    assert closest is None
    
    # Single resource
    env.resources = [Resource(1, 1, 1)]
    closest = env.get_closest_resource(2, 2)
    assert closest is not None
    assert closest.x == 1 and closest.y == 1
    
    # All resources collected
    env.resources[0].collected = True
    closest = env.get_closest_resource(2, 2)
    assert closest is None


def test_resource_collection_edge_cases():
    """Test edge cases for resource collection."""
    env = Environment()
    
    # Collect already collected resource
    resource = Resource(1, 1, 5)
    resource.collected = True
    value = env.collect_resource(resource)
    assert value == 5  # Should still return value
    assert resource.collected  # Should remain collected
    
    # Collect resource with zero value
    resource2 = Resource(2, 2, 0)
    value = env.collect_resource(resource2)
    assert value == 0
    assert resource2.collected


