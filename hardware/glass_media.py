"""Glass platter abstraction for baseline and OGB-based placement modes."""

from __future__ import annotations

from config import OGB_GAP_SIZE, PLATTER_SIZE_X, PLATTER_SIZE_Y, REGION_SIZE, VOXEL_DENSITY, Z_LAYERS


class GlassMedia:
    """Represents physical media geometry and region allocation behavior."""

    def __init__(self, mode: str = "baseline") -> None:
        self.mode = mode

        self.platter_size_x = PLATTER_SIZE_X
        self.platter_size_y = PLATTER_SIZE_Y
        self.z_layers = Z_LAYERS
        self.voxel_density = VOXEL_DENSITY

        self.ogb_gap_size = OGB_GAP_SIZE
        self.region_size = REGION_SIZE

    def receive_object(self, object_id: str, size_kb: int, user_tag: str) -> None:
        """Receive an incoming object before media placement."""
        pass

    def allocate_region(self, object_id: str, size_kb: int, user_tag: str) -> dict:
        """Allocate region coordinates according to current mode."""
        pass

    def manage_region_dependency(self, region_id: str) -> None:
        """Manage inter-region write dependencies for proposed mode."""
        pass

    def calculate_space_utilization(self) -> float:
        """Calculate valid data utilization over total occupied media space."""
        pass
