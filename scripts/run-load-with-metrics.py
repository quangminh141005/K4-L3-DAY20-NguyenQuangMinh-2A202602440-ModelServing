#!/usr/bin/env python3
"""Overlap the required 50-user load test and Prometheus sampling."""
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
with (root / 'benchmarks/load-50.log').open('w') as load_log, (root / 'benchmarks/metrics.log').open('w') as metrics_log:
    load = subprocess.Popen(['make', 'load-50'], cwd=root, stdout=load_log, stderr=subprocess.STDOUT)
    metrics = subprocess.Popen(['make', 'metrics'], cwd=root, stdout=metrics_log, stderr=subprocess.STDOUT)
    try:
        codes = [load.wait(), metrics.wait()]
    finally:
        for proc in (load, metrics):
            if proc.poll() is None:
                proc.terminate()
                proc.wait()
if any(codes):
    raise SystemExit(f'Run failed: load/metrics exit codes {codes}; inspect benchmarks/*.log')
print('50-user load and metrics sampling completed successfully.')
