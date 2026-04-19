"""Compatibility layer for SimPy imports used in the skeleton phase."""

from __future__ import annotations

from types import SimpleNamespace

try:
    import simpy as _simpy
except ModuleNotFoundError:
    class _FallbackEnvironment:
        """Minimal SimPy-like environment used when SimPy is unavailable."""

        def __init__(self) -> None:
            self.now = 0.0

        def process(self, generator):
            """Register a process placeholder."""
            return generator

        def run(self, until=None) -> None:
            """Advance simulated time to the target horizon."""
            if until is not None:
                self.now = float(until)

    class _FallbackContainer:
        """Minimal SimPy-like container for bootstrap wiring only."""

        def __init__(self, env, capacity: float, init: float = 0) -> None:
            self.env = env
            self.capacity = capacity
            self.level = init

        def put(self, amount: float) -> None:
            """Increase container level without event semantics."""
            self.level = min(self.capacity, self.level + amount)

        def get(self, amount: float) -> None:
            """Decrease container level without event semantics."""
            self.level = max(0.0, self.level - amount)

    simpy = SimpleNamespace(Environment=_FallbackEnvironment, Container=_FallbackContainer)
else:
    simpy = _simpy

