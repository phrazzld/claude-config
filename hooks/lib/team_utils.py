"""Shared utilities for agent team detection."""
import time
from pathlib import Path


def is_in_active_team() -> bool:
    """Check if an agent team is active (teammates implement directly).

    Looks for fresh (<24h) config files in ~/.claude/teams/.
    Freshness prevents stale configs from permanently disabling enforcement.
    """
    teams_dir = Path.home() / ".claude/teams"
    if not teams_dir.exists():
        return False
    for team_dir in teams_dir.iterdir():
        if not team_dir.is_dir():
            continue
        config = team_dir / "config.json"
        if config.exists() and time.time() - config.stat().st_mtime < 86400:
            return True
    return False
