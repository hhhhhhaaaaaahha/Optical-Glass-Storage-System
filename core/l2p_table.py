"""Logical-to-Physical mapping table and metadata placeholders."""

from __future__ import annotations

from config import OGB_GAP_SIZE, REGION_SIZE, VOXEL_DENSITY, Z_LAYERS


class L2PTable:
    """Stores logical object IDs and their physical placement metadata."""

    def __init__(self) -> None:
        self.mapping = {}
        self.voxel_density = VOXEL_DENSITY
        self.z_layers = Z_LAYERS
        self.region_size = REGION_SIZE
        self.ogb_gap_size = OGB_GAP_SIZE

    def register_mapping(self, object_id: str, physical_layout: dict) -> None:
        """Register logical-to-physical mapping for an object."""
        pass

    def lookup_mapping(self, object_id: str) -> dict | None:
        """Lookup physical coordinates for a logical object."""
        pass

    def mark_padding_layer(self, object_id: str, layer_index: int) -> None:
        """Mark a layer as padding for logical filtering."""
        pass

    def filter_padding_layers(self, object_id: str) -> list:
        """Return only valid layers for read-side decode path."""
        pass
