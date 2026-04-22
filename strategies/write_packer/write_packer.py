"""Single write packer implementation with pluggable packing algorithms."""

from __future__ import annotations

from config import OGB_GAP_SIZE, REGION_SIZE, STAGING_BUFFER_MAX_SIZE
from strategies.write_packer.algorithms.base import PackingAlgorithm
from strategies.write_packer.algorithms.baseline_fifo import BaselineFIFOAlgorithm


class WritePacker:
    """Coordinates staging buffer and delegates packing behavior to an algorithm."""

    def __init__(
        self,
        env,
        buffer,
        l2p_table,
        glass_media,
        packing_algorithm: PackingAlgorithm | None = None,
    ) -> None:
        self.env = env
        self.buffer = buffer
        self.l2p_table = l2p_table
        self.glass_media = glass_media
        self.packing_algorithm = packing_algorithm or BaselineFIFOAlgorithm()

        self.staging_buffer_max_size = STAGING_BUFFER_MAX_SIZE
        self.ogb_gap_size = OGB_GAP_SIZE
        self.region_size = REGION_SIZE

    @property
    def algorithm_name(self) -> str:
        """Return configured packing algorithm name."""
        return getattr(self.packing_algorithm, "name", self.packing_algorithm.__class__.__name__)

    def receive_object(self, request_id, object_id, size, user_tag):
        """Compatibility API for incoming write requests."""
        return self.process_incoming_request(request_id, object_id, size, user_tag)

    def process_incoming_request(self, request_id, object_id, size, user_tag):
        """Handle incoming object and delegate packing behavior."""
        return self.packing_algorithm.process_incoming_request(
            self,
            request_id,
            object_id,
            size,
            user_tag,
        )

    def manage_region_dependency(self, region_id):
        """Delegate region dependency logic when the algorithm supports it."""
        return self.packing_algorithm.manage_region_dependency(self, region_id)

    def force_flush(self):
        """Force flush buffered payload using current algorithm behavior."""
        return self.packing_algorithm.force_flush(self)
