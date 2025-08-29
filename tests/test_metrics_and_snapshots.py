import pytest
from src.whispers.metrics import MetricsBuffer
from src.whispers.snapshots.snapshot import Snapshot, take_snapshot, restore_snapshot


def test_metrics_buffer_initialization():
    """Test MetricsBuffer initialization."""
    buffer = MetricsBuffer()
    assert len(buffer.daily) == 0


def test_metrics_buffer_log_day():
    """Test logging daily metrics."""
    buffer = MetricsBuffer()
    
    # Log some test data
    test_record = {"day": 1, "agents_alive": 5, "resources_collected": 10}
    buffer.log_day(test_record)
    
    assert len(buffer.daily) == 1
    assert buffer.daily[0]["day"] == 1
    assert buffer.daily[0]["agents_alive"] == 5
    assert buffer.daily[0]["resources_collected"] == 10


def test_metrics_buffer_multiple_days():
    """Test logging multiple days of metrics."""
    buffer = MetricsBuffer()
    
    for day in range(5):
        record = {"day": day, "agents_alive": day + 1, "resources": day * 2}
        buffer.log_day(record)
    
    assert len(buffer.daily) == 5
    
    # Verify all days are logged correctly
    for i, record in enumerate(buffer.daily):
        assert record["day"] == i
        assert record["agents_alive"] == i + 1
        assert record["resources"] == i * 2


def test_metrics_buffer_finalize():
    """Test finalizing metrics buffer."""
    buffer = MetricsBuffer()
    
    # Add some test data
    buffer.log_day({"day": 1, "test": "data"})
    buffer.log_day({"day": 2, "test": "more"})
    
    result = buffer.finalize()
    
    assert "daily" in result
    assert "summary" in result
    assert len(result["daily"]) == 2
    assert result["daily"][0]["day"] == 1
    assert result["daily"][1]["day"] == 2


def test_metrics_buffer_immutable_logging():
    """Test that logging doesn't modify the input record."""
    buffer = MetricsBuffer()
    
    original_record = {"day": 1, "data": [1, 2, 3]}
    buffer.log_day(original_record)
    
    # Modify the original record
    original_record["data"].append(4)
    
    # The logged record should not be affected
    assert len(buffer.daily[0]["data"]) == 3


def test_snapshot_creation():
    """Test creating a snapshot."""
    test_state = {"agents": 5, "day": 10, "resources": 25}
    snapshot = take_snapshot(test_state)
    
    assert isinstance(snapshot, Snapshot)
    assert snapshot.metadata == {}
    assert snapshot.state == test_state


def test_snapshot_restoration():
    """Test restoring from a snapshot."""
    original_state = {"agents": 5, "day": 10, "resources": 25}
    snapshot = take_snapshot(original_state)
    
    restored_state = restore_snapshot(snapshot)
    
    assert restored_state == original_state
    assert restored_state is not original_state  # Should be a copy


def test_snapshot_immutability():
    """Test that snapshot restoration doesn't modify the original."""
    original_state = {"data": [1, 2, 3]}
    snapshot = take_snapshot(original_state)
    
    restored_state = restore_snapshot(snapshot)
    restored_state["data"].append(4)
    
    # Original state should be unchanged
    assert len(original_state["data"]) == 3
    assert len(snapshot.state["data"]) == 3


def test_snapshot_with_metadata():
    """Test snapshot with custom metadata."""
    test_state = {"test": "data"}
    snapshot = Snapshot(metadata={"timestamp": "2024-01-01"}, state=test_state)
    
    assert snapshot.metadata["timestamp"] == "2024-01-01"
    assert snapshot.state == test_state


