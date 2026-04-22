"""Entry point for the Glass-Native Object Store discrete-event simulator."""

from __future__ import annotations

import argparse

from config import STAGING_BUFFER_MAX_SIZE
from core.env_manager import EnvironmentManager
from core.l2p_table import L2PTable
from core.simpy_compat import simpy
from hardware.glass_media import GlassMedia
from hardware.read_drive import ReadDrive
from hardware.write_drive import WriteDrive
from strategies.read_scheduler.baseline_smtf import BaselineSMTFReadScheduler
from strategies.read_scheduler.proposed_occs import ProposedOCCSReadScheduler
from strategies.write_packer.algorithms.proposed_sa_bfd import ProposedSABFDAlgorithm
from strategies.write_packer.write_packer import WritePacker
from utils.metrics import MetricsCollector
from workload.generator import WorkloadGenerator


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for simulation setup."""
    parser = argparse.ArgumentParser(description="Glass Storage Simulator")
    parser.add_argument(
        "--mode",
        choices=["baseline", "proposed"],
        default="baseline",
        help="Select baseline or proposed architecture.",
    )
    parser.add_argument(
        "--workload",
        default=None,
        help="Optional path to workload trace file.",
    )
    parser.add_argument(
        "--until-ms",
        type=float,
        default=1.0,
        help="Simulation time horizon in milliseconds.",
    )
    return parser.parse_args()


def build_simulation(mode: str) -> dict[str, object]:
    """Build all simulator components and wire strategy objects."""
    env_manager = EnvironmentManager()
    env = env_manager.env

    staging_buffer = simpy.Container(env, capacity=STAGING_BUFFER_MAX_SIZE, init=0)
    l2p_table = L2PTable()
    glass_media = GlassMedia(mode=mode)
    read_drive = ReadDrive(env)
    write_drive = WriteDrive(env)

    if mode == "baseline":
        packing_algorithm = None
        read_scheduler = BaselineSMTFReadScheduler(env, read_drive, l2p_table)
    else:
        packing_algorithm = ProposedSABFDAlgorithm()
        read_scheduler = ProposedOCCSReadScheduler(env, read_drive, l2p_table)

    write_packer = WritePacker(
        env,
        staging_buffer,
        l2p_table,
        glass_media,
        packing_algorithm=packing_algorithm,
    )

    metrics = MetricsCollector()
    workload_generator = WorkloadGenerator()

    return {
        "env_manager": env_manager,
        "staging_buffer": staging_buffer,
        "l2p_table": l2p_table,
        "glass_media": glass_media,
        "read_drive": read_drive,
        "write_drive": write_drive,
        "write_packer": write_packer,
        "read_scheduler": read_scheduler,
        "metrics": metrics,
        "workload_generator": workload_generator,
    }


def main() -> None:
    """Initialize and run the simulation skeleton."""
    args = parse_args()
    simulation = build_simulation(args.mode)
    env_manager = simulation["env_manager"]

    if isinstance(env_manager, EnvironmentManager):
        env_manager.run(until=args.until_ms)

    print(
        f"Simulator initialized successfully (mode={args.mode}, until_ms={args.until_ms}, "
        f"workload={args.workload})."
    )


if __name__ == "__main__":
    main()
