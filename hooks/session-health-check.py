#!/usr/bin/env python3
"""
Session start health check - warns if system resources are constrained.
Lightweight check that runs at session start.
"""

import json
import os
import subprocess
import sys


def get_disk_percent():
    """Get disk usage percentage."""
    try:
        result = subprocess.run(
            ["df", "-h", "/System/Volumes/Data"],
            capture_output=True, text=True, timeout=5
        )
        # Parse "97%" from output
        for line in result.stdout.strip().split('\n')[1:]:
            parts = line.split()
            if len(parts) >= 5:
                return int(parts[4].rstrip('%'))
    except Exception:
        pass
    return None


def get_swap_gb():
    """Get swap usage in GB."""
    try:
        result = subprocess.run(
            ["sysctl", "vm.swapusage"],
            capture_output=True, text=True, timeout=5
        )
        # Parse "used = 7783.88M"
        output = result.stdout
        if "used = " in output:
            used_part = output.split("used = ")[1].split()[0]
            value = float(used_part.rstrip('M'))
            return value / 1024  # Convert MB to GB
    except Exception:
        pass
    return None


def main():
    warnings = []

    disk_pct = get_disk_percent()
    if disk_pct and disk_pct >= 90:
        warnings.append(f"💾 Disk at {disk_pct}% - consider running 'cache-clean'")

    swap_gb = get_swap_gb()
    if swap_gb and swap_gb >= 15:
        warnings.append(f"🔄 Swap at {swap_gb:.1f}GB - high memory pressure")

    if warnings:
        message = "[codex] ⚠️ SYSTEM HEALTH:\n" + "\n".join(warnings)
        print(json.dumps({"message": message}))
    else:
        print(json.dumps({}))


if __name__ == "__main__":
    main()
