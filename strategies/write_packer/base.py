"""Abstract write packer strategy interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from config import OGB_GAP_SIZE, REGION_SIZE, STAGING_BUFFER_MAX_SIZE


class BaseWritePacker(ABC):
    """Strategy interface for object packing and flush decisions."""

    def __init__(self, env, buffer, l2p_table, glass_media) -> None:
        self.env = env
        self.buffer = buffer
        self.l2p_table = l2p_table
        self.glass_media = glass_media

        self.staging_buffer_max_size = STAGING_BUFFER_MAX_SIZE
        self.ogb_gap_size = OGB_GAP_SIZE
        self.region_size = REGION_SIZE

    @abstractmethod
    def process_incoming_request(self, request_id, object_id, size, user_tag):
        """Handle incoming object and decide when to flush to glass media."""
        pass

    @abstractmethod
    def force_flush(self):
        """Flush buffered payload due to timeout or pressure."""
        pass
