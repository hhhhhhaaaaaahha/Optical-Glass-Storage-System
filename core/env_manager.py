"""SimPy environment wrapper for simulator lifecycle management."""

from __future__ import annotations

from config import (
    DECODE_THROUGHPUT_LIMIT,
    LASER_WRITE_SPEED,
    OGB_GAP_SIZE,
    PLATTER_SIZE_X,
    PLATTER_SIZE_Y,
    REGION_SIZE,
    STAGING_BUFFER_MAX_SIZE,
    VOXEL_DENSITY,
    XY_STAGE_ACCELERATION,
    XY_STAGE_MAX_VELOCITY,
    Z_LAYERS,
    Z_SCAN_DELAY_PER_LAYER,
)
from core.simpy_compat import simpy


class EnvironmentManager:
    """Owns the SimPy environment and global simulation-scoped parameters."""

    def __init__(self) -> None:
        self.env = simpy.Environment()

        self.platter_size_x = PLATTER_SIZE_X
        self.platter_size_y = PLATTER_SIZE_Y
        self.z_layers = Z_LAYERS
        self.voxel_density = VOXEL_DENSITY

        self.xy_stage_max_velocity = XY_STAGE_MAX_VELOCITY
        self.xy_stage_acceleration = XY_STAGE_ACCELERATION
        self.z_scan_delay_per_layer = Z_SCAN_DELAY_PER_LAYER
        self.decode_throughput_limit = DECODE_THROUGHPUT_LIMIT
        self.laser_write_speed = LASER_WRITE_SPEED

        self.staging_buffer_max_size = STAGING_BUFFER_MAX_SIZE
        self.ogb_gap_size = OGB_GAP_SIZE
        self.region_size = REGION_SIZE

    def register_process(self, process) -> None:
        """Register a process handle for later orchestration."""
        pass

    def run(self, until: float | None = None) -> None:
        """Run the SimPy environment."""
        self.env.run(until=until)
