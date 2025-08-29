from src.whispers.metrics import MetricsBuffer
from src.whispers.snapshots import Snapshot, take_snapshot, restore_snapshot


def test_metrics_buffer_empty_finalize_structure():
    m = MetricsBuffer()
    final = m.finalize()
    assert isinstance(final, dict)
    assert "daily" in final and isinstance(final["daily"], list)
    assert "summary" in final and isinstance(final["summary"], dict)


def test_snapshot_dataclass_and_roundtrip_identity():
    state = {"x": 1, "nested": {"y": 2}}
    snap = take_snapshot(state)
    assert isinstance(snap, Snapshot)
    restored = restore_snapshot(snap)
    assert restored == state


