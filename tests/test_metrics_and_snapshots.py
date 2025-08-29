from src.whispers.metrics import MetricsBuffer
from src.whispers.snapshots import take_snapshot, restore_snapshot


def test_metrics_buffer_log_and_finalize():
    m = MetricsBuffer()
    m.log_day({"n": 1})
    m.log_day({"n": 2})
    final = m.finalize()
    assert "daily" in final and "summary" in final
    assert final["daily"][0]["n"] == 1
    assert final["daily"][1]["n"] == 2


def test_snapshot_roundtrip():
    state = {"day": 5, "agents": []}
    snap = take_snapshot(state)
    restored = restore_snapshot(snap)
    assert restored == state


