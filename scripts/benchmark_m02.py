"""Measure a cold deterministic analysis on a reproducible local workload."""

import argparse
import io
import json
import platform
import sys
from csv import writer
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

from risklens.application.contracts import AnalysisRequest, canonical, sha256
from risklens.application.service import AnalysisService
from risklens.infrastructure.parser import HEADER
from risklens.infrastructure.sample import sample_bundle
from risklens.infrastructure.state import LocalState


def benchmark_bundle(rows: int) -> tuple[bytes, bytes]:
    if rows == 2:
        return sample_bundle()
    buffer = io.StringIO(newline="")
    csv = writer(buffer, lineterminator="\n")
    csv.writerow(HEADER)
    csv.writerows(
        (
            f"loan-{i:05d}",
            f"borrower-{i // 2:05d}",
            "1000.00",
            f"{100 + i % 900}.00",
            i % 11,
            "open",
            "2026-01-01",
            f"segment-{i % 20:02d}",
        )
        for i in range(rows)
    )
    csv_bytes = buffer.getvalue().encode("utf-8")
    return canonical(
        {
            "schema_version": "1.0",
            "snapshot_id": f"benchmark-{rows}",
            "portfolio_id": "benchmark-m02",
            "portfolio_name": "Synthetic M02 benchmark",
            "as_of": "2026-10-15",
            "currency": "USD",
            "synthetic": True,
            "generator_version": "benchmark-m02-v1",
            "seed": 0,
            "source_sha256": sha256(csv_bytes),
        }
    ), csv_bytes


def peak_resident_bytes() -> int:
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        class MemoryCounters(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        handle = ctypes.WinDLL("kernel32").GetCurrentProcess
        handle.restype = wintypes.HANDLE
        measure = ctypes.WinDLL("psapi", use_last_error=True).GetProcessMemoryInfo
        measure.argtypes = [wintypes.HANDLE, ctypes.POINTER(MemoryCounters), wintypes.DWORD]
        measure.restype = wintypes.BOOL
        counters = MemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        if not measure(handle(), ctypes.byref(counters), counters.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        return int(counters.PeakWorkingSetSize)

    import resource

    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(peak if sys.platform == "darwin" else peak * 1024)


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--rows", type=int, choices=[2, 10_000, 50_000], required=True)
    rows: int = cli.parse_args().rows
    manifest, csv = benchmark_bundle(rows)
    with TemporaryDirectory(prefix="risklens-benchmark-") as directory:
        workspace = Path(directory)
        start = perf_counter()
        service = AnalysisService(LocalState(workspace))
        bundle_ref = service.register_bundle(manifest, csv)
        result = service.execute(
            AnalysisRequest(
                bundle_ref=bundle_ref,
                import_idempotency_key="benchmark-import",
                analysis_idempotency_key="benchmark-analysis",
                mode="deterministic_m02",
                requested_stages=("validate_portfolio", "calculate_metrics"),
                configuration=service.configuration,
                parent_run_id=None,
            )
        )
        reopen = AnalysisService(LocalState(workspace)).get_run(result.run.run_id)
        elapsed = perf_counter() - start
        if reopen.metrics is None or reopen.metrics.loan_count != rows:
            raise RuntimeError("The benchmark did not produce verified complete metrics")
        print(
            json.dumps(
                {
                    "rows": rows,
                    "bundle_bytes": len(manifest) + len(csv),
                    "input_sha256": result.run.input_hash,
                    "metrics_sha256": result.metrics_hash,
                    "elapsed_seconds": round(elapsed, 4),
                    "peak_resident_mib": round(peak_resident_bytes() / 1024**2, 2),
                    "platform": platform.platform(),
                    "python": platform.python_version(),
                    "code_revision": result.run.code_revision,
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
