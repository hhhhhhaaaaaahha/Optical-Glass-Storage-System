"""Metrics collection placeholders for simulation experiment outputs."""

from __future__ import annotations


class MetricsCollector:
    """Collects and exports runtime metrics for evaluation."""

    def __init__(self) -> None:
        self.max_buffer_usage_mb = 0.0
        self.space_utilization_percent = 0.0
        self.avg_object_completion_time_ms = 0.0
        self.p99_object_completion_time_ms = 0.0
        self.total_xy_seek_distance_mm = 0.0

    def record_buffer_usage(self, usage_mb: float) -> None:
        """Record current staging buffer usage."""
        pass

    def record_space_utilization(self, utilization_percent: float) -> None:
        """Record current media space utilization."""
        pass

    def record_object_completion_time(self, completion_time_ms: float) -> None:
        """Record read completion latency for one object."""
        pass

    def record_seek_distance(self, seek_distance_mm: float) -> None:
        """Record incremental XY seek distance."""
        pass

    def export_json(self, output_path: str) -> None:
        """Export collected metrics to JSON."""
        pass

    def export_csv(self, output_path: str) -> None:
        """Export collected metrics to CSV."""
        pass
