"""Baseline FIFO packing algorithm placeholder."""

from __future__ import annotations

from strategies.write_packer.algorithms.base import PackingAlgorithm


class BaselineFIFOAlgorithm(PackingAlgorithm):
    """Baseline policy: single-region FIFO packing across platter layers."""

    def __init__(self) -> None:
        self.name = "baseline_fifo"

    def process_incoming_request(self, write_packer, request_id, object_id, size, user_tag):
        """Queue object in FIFO order and trigger flush policy."""
        pass

    def force_flush(self, write_packer):
        """Force flush buffered objects to media."""
        pass
