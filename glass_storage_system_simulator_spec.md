# Glass Storage Simulator: System Specification

> **Version:** 1.0
**Objective:** A discrete-event simulator (using `simpy`) to evaluate the write/read performance and resource utilization of Glass-Native Object Storage.
**Architecture Support:** Dynamically switchable between Baseline (GAIA/Traditional) and Proposed (V3: OGB + SA-BFD + OCCS).
> 

---

## 1. Physical Parameters & System Constants (Configurable)

*These parameters are derived from Project Silica & GAIA literature context and should be defined in a `config.py` file.*

### 1.1 Glass Platter (Media)

- `PLATTER_SIZE_X`, `PLATTER_SIZE_Y`: 120.0 (mm)
- `Z_LAYERS`: 200 (Total layers per Z-axis track)
- `VOXEL_DENSITY`: 100 KB per Sector/Layer-Track

### 1.2 Hardware Kinematics (Read/Write Drives)

- `XY_STAGE_MAX_VELOCITY`: 100.0 (mm/s)
- `XY_STAGE_ACCELERATION`: 500.0 (mm/s^2)
- `Z_SCAN_DELAY_PER_LAYER`: 0.05 (ms)
- `DECODE_THROUGHPUT_LIMIT`: 500 (MB/s) - *Used for Baseline only; Proposed drops padding early.*
- `LASER_WRITE_SPEED`: 50 (MB/s)

### 1.3 Buffer & OGB Parameters

- `STAGING_BUFFER_MAX_SIZE`: 16384 (MB, 16GB limit)
- `OGB_GAP_SIZE`: 1.0 (mm) - *Optical Guard Band*
- `REGION_SIZE`: 10.0 (mm) - *Size of one independent write zone*

---

## 2. Directory Structure

```bash
glass_storage_sim/
├── main.py                 # Entry point, argument parser (--mode baseline/proposed)
├── config.py               # Global physical parameters
├── workload/
│   └── generator.py        # Generates synthetic Zipfian traces
├── core/
│   ├── env_manager.py      # Simpy environment wrapper
│   └── l2p_table.py        # Logical-to-Physical mapping & Metadata
├── hardware/
│   ├── glass_media.py      # Platter space math (Baseline vs OGB)
│   ├── read_drive.py       # Simulates kinematic delays (XY seek, Z-scan)
│   └── write_drive.py      # Simulates laser wavefront progression
├── strategies/               # STRATEGY PATTERN FOR DYNAMIC SWITCHING
│   ├── write_packer/
│   │   ├── base.py
│   │   ├── baseline_fifo.py
│   │   └── proposed_sa_bfd.py
│   └── read_scheduler/
│       ├── base.py
│       ├── baseline_smtf.py
│       └── proposed_occs.py
└── utils/
    └── metrics.py          # Collects and exports CSV data
```

---

## 3. Core API Interfaces (Abstract Base Classes)

*AI Agent Instruction: Implement the following abstract classes to allow dynamic injection of Baseline vs. Proposed strategies.*

### 3.1 Write Packer Strategy (`strategies/write_packer/base.py`)

```python
from abc import ABC, abstractmethod

class BaseWritePacker(ABC):
    def __init__(self, env, buffer, l2p_table, glass_media):
        self.env = env
        self.buffer = buffer
        self.l2p_table = l2p_table
        self.glass_media = glass_media

    @abstractmethod
    def process_incoming_request(self, request_id, object_id, size, user_tag):
        """Handle incoming object and decide when to flush to glass_media."""
        pass

    @abstractmethod
    def force_flush(self):
        """Triggered by timeout or buffer pressure. Must handle padding if needed."""
        pass
```

- **Baseline Implementation (`baseline_fifo.py`)**: Treats the whole platter as one region. Waits until Layer N of the *entire platter* is full before moving to Layer N+1.
- **Proposed Implementation (`proposed_sa_bfd.py`)**: Uses `REGION_SIZE` and `OGB_GAP_SIZE`. Groups objects by `user_tag`. Triggers `Dynamic Zero-Padding` if a region is stalled.

### 3.2 Read Scheduler Strategy (`strategies/read_scheduler/base.py`)

```python
from abc import ABC, abstractmethod

class BaseReadScheduler(ABC):
    def __init__(self, env, read_drive, l2p_table):
        self.env = env
        self.read_drive = read_drive
        self.l2p_table = l2p_table
        self.read_queue = []

    @abstractmethod
    def add_request(self, object_id):
        """Add object to queue and lookup L2P physical coordinates."""
        pass

    @abstractmethod
    def get_next_target_track(self):
        """Determine the next physical track to seek and read."""
        pass
```

- **Baseline Implementation (`baseline_smtf.py`)**: Implements Shortest Mechanical Time First. Calculates Euclidean XY distance. Ignores object completion state.
- **Proposed Implementation (`proposed_occs.py`)**: Implements Object-Centric Completion Scheduling.
    - `Score = (alpha / XY_Distance) + (beta * Object_Completion_Ratio)`.
    - Also integrates `L2P Logical Filtering` (drops `is_padding=True` layers from decode delay).

---

## 4. Workload & Trace Format

The `workload/generator.py` should output a pandas DataFrame or iterable with the following schema:

- `timestamp` (float): Arrival time in ms.
- `req_type` (str): 'WRITE' or 'READ'.
- `object_id` (str): Unique ID.
- `size_kb` (int): Object size.
- `user_tag` (str): Represents semantic locality (e.g., "Tenant_A_Backup_Job_1").

---

## 5. Experiment Execution & Metrics (`utils/metrics.py`)

The system must support running via CLI:

```bash
python3 main.py --mode baseline --workload trace.csv
python3 main.py --mode proposed --workload trace.csv
```

**Required Output Metrics (JSON/CSV):**

1. `max_buffer_usage_mb`: Peak memory used in the Staging Buffer.
2. `space_utilization_percent`: Ratio of valid data to (valid + gap + padding).
3. `avg_object_completion_time_ms`: Average TTFB/Completion time for READs.
4. `p99_object_completion_time_ms`: 99th percentile tail latency for READs.
5. `total_xy_seek_distance_mm`: Total mechanical wear/movement.