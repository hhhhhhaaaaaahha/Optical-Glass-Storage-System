"""Abstract packing algorithm contract for write packer strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod


class PackingAlgorithm(ABC):
    """Common interface for pluggable write-packing algorithms."""

    name = "packing_algorithm"

    @abstractmethod
    def process_incoming_request(self, write_packer, request_id, object_id, size, user_tag):
        """Handle one incoming object request through the selected policy."""
        pass

    @abstractmethod
    def force_flush(self, write_packer):
        """Flush pending payloads according to the selected policy."""
        pass

    def manage_region_dependency(self, write_packer, region_id):
        """Optional hook for algorithms that implement region dependencies."""
        return None

