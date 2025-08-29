import pytest
from src.whispers.metrics import MetricsBuffer
from src.whispers.snapshots.snapshot import Snapshot, take_snapshot, restore_snapshot


def test_metrics_buffer_large_dataset():
    """Test metrics buffer with large dataset."""
    buffer = MetricsBuffer()
    
    # Log many days of data
    for day in range(100):
        record = {
            "day": day,
            "agents_alive": max(0, 50 - day),
            "resources_collected": day * 10,
            "reproduction_events": day // 5,
            "cooperation_rate": 0.5 + (day % 10) / 20
        }
        buffer.log_day(record)
    
    assert len(buffer.daily) == 100
    
    # Verify finalization works with large dataset
    result = buffer.finalize()
    assert len(result["daily"]) == 100
    assert result["daily"][99]["day"] == 99


def test_metrics_buffer_complex_data_types():
    """Test metrics buffer with complex data types."""
    buffer = MetricsBuffer()
    
    complex_record = {
        "day": 1,
        "agent_positions": [(1, 1), (2, 3), (5, 5)],
        "resource_locations": [(0, 0), (1, 1)],
        "nested_data": {
            "altruists": {"count": 5, "avg_reputation": 0.8},
            "egoists": {"count": 3, "avg_reputation": 0.4}
        },
        "boolean_flags": [True, False, True]
    }
    
    buffer.log_day(complex_record)
    
    assert len(buffer.daily) == 1
    logged_record = buffer.daily[0]
    
    # Verify complex data is preserved
    assert logged_record["agent_positions"] == [(1, 1), (2, 3), (5, 5)]
    assert logged_record["nested_data"]["altruists"]["count"] == 5
    assert logged_record["boolean_flags"] == [True, False, True]


def test_snapshot_complex_state():
    """Test snapshot with complex state data."""
    complex_state = {
        "simulation_day": 15,
        "environment": {
            "width": 20,
            "height": 20,
            "resources": [{"x": 1, "y": 1, "value": 5}]
        },
        "agents": [
            {"id": "agent1", "type": "altruist", "position": (5, 5)},
            {"id": "agent2", "type": "egoist", "position": (10, 10)}
        ],
        "metrics": {
            "total_resources_collected": 150,
            "cooperation_events": 25,
            "reproduction_events": 3
        }
    }
    
    snapshot = take_snapshot(complex_state)
    restored_state = restore_snapshot(snapshot)
    
    # Verify complex state is preserved
    assert restored_state["simulation_day"] == 15
    assert restored_state["environment"]["width"] == 20
    assert len(restored_state["agents"]) == 2
    assert restored_state["agents"][0]["id"] == "agent1"
    assert restored_state["metrics"]["total_resources_collected"] == 150


def test_snapshot_nested_structures():
    """Test snapshot with deeply nested structures."""
    nested_state = {
        "level1": {
            "level2": {
                "level3": {
                    "data": [1, 2, 3],
                    "nested_dict": {"key": "value"}
                }
            }
        },
        "arrays": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    }
    
    snapshot = take_snapshot(nested_state)
    restored_state = restore_snapshot(snapshot)
    
    # Verify deep nesting is preserved
    assert restored_state["level1"]["level2"]["level3"]["data"] == [1, 2, 3]
    assert restored_state["level1"]["level2"]["level3"]["nested_dict"]["key"] == "value"
    assert restored_state["arrays"][0] == [1, 2, 3]
    assert restored_state["arrays"][1] == [4, 5, 6]


def test_metrics_buffer_edge_cases():
    """Test metrics buffer with edge case data."""
    buffer = MetricsBuffer()
    
    # Test with empty record
    buffer.log_day({})
    assert len(buffer.daily) == 1
    assert buffer.daily[0] == {}
    
    # Test with None values
    buffer.log_day({"day": None, "data": None})
    assert buffer.daily[1]["day"] is None
    assert buffer.daily[1]["data"] is None
    
    # Test with zero values
    buffer.log_day({"count": 0, "rate": 0.0})
    assert buffer.daily[2]["count"] == 0
    assert buffer.daily[2]["rate"] == 0.0


def test_snapshot_edge_cases():
    """Test snapshot with edge case data."""
    # Test with empty state
    empty_state = {}
    snapshot = take_snapshot(empty_state)
    restored = restore_snapshot(snapshot)
    assert restored == {}
    
    # Test with None values
    none_state = {"key": None, "data": None}
    snapshot = take_snapshot(none_state)
    restored = restore_snapshot(snapshot)
    assert restored["key"] is None
    assert restored["data"] is None
    
    # Test with zero values
    zero_state = {"count": 0, "rate": 0.0}
    snapshot = take_snapshot(zero_state)
    restored = restore_snapshot(snapshot)
    assert restored["count"] == 0
    assert restored["rate"] == 0.0


