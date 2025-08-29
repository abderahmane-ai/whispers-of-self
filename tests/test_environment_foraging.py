import pytest
from src.whispers.environment.environment import Environment, Resource


def test_environment_initialization():
    env = Environment()
    assert env.width == 20
    assert env.height == 20
    assert env.resource_spawn_rate == 25.0
    assert len(env.resources) == 0


def test_environment_custom_initialization():
    env = Environment(width=10, height=15, resource_spawn_rate=50.0)
    assert env.width == 10
    assert env.height == 15
    assert env.resource_spawn_rate == 50.0


def test_resource_creation():
    resource = Resource(x=5, y=10, value=3)
    assert resource.x == 5
    assert resource.y == 10
    assert resource.value == 3
    assert not resource.collected


def test_resource_string_representation():
    resource = Resource(x=1, y=2, value=5)
    str_repr = str(resource)
    assert "Resource(1, 2, value=5)" in str_repr


def test_environment_spawn_resources():
    env = Environment(width=5, height=5, resource_spawn_rate=10.0)
    env.spawn_resources()
    
    # Should have spawned some resources
    assert len(env.resources) > 0
    
    # All resources should be within bounds
    for resource in env.resources:
        assert 0 <= resource.x < env.width
        assert 0 <= resource.y < env.height
        assert not resource.collected


def test_environment_get_closest_resource():
    env = Environment(width=10, height=10)
    
    # Add some test resources
    env.resources = [
        Resource(1, 1, 1),
        Resource(5, 5, 1),
        Resource(9, 9, 1)
    ]
    
    # Test finding closest resource
    closest = env.get_closest_resource(3, 3)
    assert closest is not None
    assert closest.x == 1 and closest.y == 1  # Should be closest to (3,3)
    
    # Test with no available resources
    for resource in env.resources:
        resource.collected = True
    
    closest = env.get_closest_resource(3, 3)
    assert closest is None


def test_environment_collect_resource():
    env = Environment()
    resource = Resource(1, 1, 5)
    
    # Collect resource
    value = env.collect_resource(resource)
    assert value == 5
    assert resource.collected


