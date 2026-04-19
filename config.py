"""Global configuration constants for the Glass Storage Simulator."""

# 1.1 Glass Platter (Media)
PLATTER_SIZE_X = 120.0  # mm
PLATTER_SIZE_Y = 120.0  # mm
Z_LAYERS = 200
VOXEL_DENSITY = 100  # KB per sector/layer-track

# 1.2 Hardware Kinematics (Read/Write Drives)
XY_STAGE_MAX_VELOCITY = 100.0  # mm/s
XY_STAGE_ACCELERATION = 500.0  # mm/s^2
Z_SCAN_DELAY_PER_LAYER = 0.05  # ms
DECODE_THROUGHPUT_LIMIT = 500  # MB/s
LASER_WRITE_SPEED = 50  # MB/s

# 1.3 Buffer & OGB Parameters
STAGING_BUFFER_MAX_SIZE = 16384  # MB
OGB_GAP_SIZE = 1.0  # mm
REGION_SIZE = 10.0  # mm


class SimulatorConfig:
    """Container object exposing all physical constants as instance attributes."""

    def __init__(self) -> None:
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
