"""Synthetic workload generator and trace loader placeholders."""

from __future__ import annotations


class WorkloadGenerator:
    """Generates or loads workload traces for simulator input."""

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def generate_zipf_trace(self, num_requests: int):
        """Generate synthetic Zipfian trace records."""
        pass

    def load_trace(self, workload_path: str):
        """Load trace file into simulator-consumable records."""
        pass

    def iter_trace(self):
        """Yield workload entries in chronological order."""
        pass
