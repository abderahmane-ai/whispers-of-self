"""
Metrics tracking baseline.

Provides a minimal structure for collecting time-series and summary stats.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MetricsBuffer:
    """In-memory accumulator for metrics."""
    daily: List[Dict] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)

    def log_day(self, data: Dict) -> None:
        self.daily.append(dict(data))

    def finalize(self) -> Dict:
        return {"daily": self.daily, "summary": self.summary}


