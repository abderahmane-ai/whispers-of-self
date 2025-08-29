"""Minimal metrics buffer for tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MetricsBuffer:
    """Collects per-day metrics and summarizes at the end."""
    daily: List[Dict[str, Any]] = field(default_factory=list)

    def log_day(self, record: Dict[str, Any]) -> None:
        self.daily.append(dict(record))

    def finalize(self) -> Dict[str, Any]:
        return {
            "daily": list(self.daily),
            "summary": {},
        }

__all__ = ["MetricsBuffer"]


