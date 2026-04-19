"""Baseline FIFO write packer implementation placeholder."""

from __future__ import annotations

from strategies.write_packer.base import BaseWritePacker


class BaselineFIFOWritePacker(BaseWritePacker):
    """Baseline policy: single-region FIFO packing across platter layers."""

    def __init__(self, env, buffer, l2p_table, glass_media) -> None:
        super().__init__(env, buffer, l2p_table, glass_media)
        self.mode = "baseline"

    def receive_object(self, request_id, object_id, size, user_tag):
        """Compatibility API for incoming write requests."""
        return self.process_incoming_request(request_id, object_id, size, user_tag)

    def process_incoming_request(self, request_id, object_id, size, user_tag):
        """Queue object in FIFO order and trigger flush policy."""
        pass

    def force_flush(self):
        """Force flush buffered objects to media."""
        pass
