"""
Snapshotting baseline.

Provides minimal utilities to capture and restore simulation state later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Snapshot:
    """Simple container for serialized state."""
    metadata: Dict[str, Any]
    state: Dict[str, Any]


def take_snapshot(sim_state: Dict[str, Any]) -> Snapshot:
    """Capture a snapshot from a simulation-provided dict."""
    return Snapshot(metadata={}, state=dict(sim_state))


def restore_snapshot(snapshot: Snapshot) -> Dict[str, Any]:
    """Return a state dict that a simulation can use to restore later."""
    return dict(snapshot.state)


