"""Baseline SMTF read scheduler implementation placeholder."""

from __future__ import annotations

from strategies.read_scheduler.base import BaseReadScheduler


class BaselineSMTFReadScheduler(BaseReadScheduler):
    """Shortest Mechanical Time First scheduler placeholder."""

    def __init__(self, env, read_drive, l2p_table) -> None:
        super().__init__(env, read_drive, l2p_table)
        self.mode = "baseline"

    def add_request(self, object_id):
        """Add a read request and prepare candidate track metadata."""
        pass

    def estimate_mechanical_time(self, target_track):
        """Estimate travel time to a candidate target track."""
        pass

    def get_next_target_track(self):
        """Return next target using SMTF policy."""
        pass
