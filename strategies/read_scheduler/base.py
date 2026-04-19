"""Abstract read scheduler strategy interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from config import DECODE_THROUGHPUT_LIMIT, XY_STAGE_ACCELERATION, XY_STAGE_MAX_VELOCITY, Z_SCAN_DELAY_PER_LAYER


class BaseReadScheduler(ABC):
    """Strategy interface for read-queue ordering decisions."""

    def __init__(self, env, read_drive, l2p_table) -> None:
        self.env = env
        self.read_drive = read_drive
        self.l2p_table = l2p_table
        self.read_queue = []

        self.xy_stage_max_velocity = XY_STAGE_MAX_VELOCITY
        self.xy_stage_acceleration = XY_STAGE_ACCELERATION
        self.z_scan_delay_per_layer = Z_SCAN_DELAY_PER_LAYER
        self.decode_throughput_limit = DECODE_THROUGHPUT_LIMIT

    @abstractmethod
    def add_request(self, object_id):
        """Add object to read queue and resolve physical mapping."""
        pass

    @abstractmethod
    def get_next_target_track(self):
        """Select next physical target based on scheduling policy."""
        pass
