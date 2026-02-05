#!/usr/bin/env python3
"""
Delegation guard - graduated enforcement for delegation.

PreToolUse hook with tiered responses:
- Silent: excluded repos, trivial edits
- Warn: approaching thresholds (shows message, allows)
- Ask: exceeds soft limits (prompts user confirmation)
- Block: exceeds hard limits (denies with MCP suggestion)

Config: ~/.claude/config/delegation-enforcement.json
Session state: /tmp/claude-delegation-{PPID}.json
"""
import fnmatch
import json
import os
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".claude/config/delegation-enforcement.json"

DEFAULT_CONFIG = {
    "enabled": True,
    "mode": "graduated",
    "exclusions": {
        "repositories": [],
        "patterns": []
    },
    "thresholds": {
        "silent": {"maxLines": 20, "maxFiles": 1, "maxNewFiles": 0},
        "warn": {"maxLines": 50, "maxFiles": 2, "maxNewFiles": 1},
        "ask": {"maxLines": 100, "maxFiles": 4, "maxNewFiles": 3}
    },
    "alwaysSilent": ["**/.env*", "**/package.json", "**/*.lock", "**/CLAUDE.md"]
}


def load_config() -> dict:
    """Load config with fallback to defaults."""
    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text())
            # Merge with defaults for missing keys
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_CONFIG


def get_state_file() -> Path:
    """Get session state file path based on parent PID."""
    ppid = os.getppid()
    return Path(f"/tmp/claude-delegation-{ppid}.json")


def load_state() -> dict:
    """Load session state, creating fresh if missing."""
    state_file = get_state_file()
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "files_touched": [],
        "new_files_created": 0,
        "total_lines_added": 0,
        "directories_touched": [],
    }


def save_state(state: dict) -> None:
    """Save session state."""
    get_state_file().write_text(json.dumps(state, indent=2))


def is_excluded_repo(cwd: str, config: dict) -> bool:
    """Check if current working directory is in excluded repos."""
    exclusions = config.get("exclusions", {})

    # Check exact repo paths
    for repo_path in exclusions.get("repositories", []):
        if cwd.startswith(repo_path):
            return True

    # Check glob patterns
    for pattern in exclusions.get("patterns", []):
        if fnmatch.fnmatch(cwd, pattern):
            return True

    return False


def is_always_silent(file_path: str, config: dict) -> bool:
    """Check if file matches always-silent patterns."""
    for pattern in config.get("alwaysSilent", []):
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def get_directory(file_path: str) -> str:
    """Extract directory from file path."""
    return str(Path(file_path).parent)


def count_lines(tool_input: dict) -> int:
    """Estimate lines being added/changed."""
    new_string = tool_input.get("new_string", "")
    content = tool_input.get("content", "")
    text = new_string or content
    if not text:
        return 0
    return len(text.strip().split("\n"))


def calculate_tier(state: dict, config: dict) -> str:
    """
    Determine enforcement tier based on session metrics.

    Returns: "silent", "warn", "ask", or "block"
    """
    thresholds = config.get("thresholds", DEFAULT_CONFIG["thresholds"])

    num_files = len(state["files_touched"])
    total_lines = state["total_lines_added"]
    new_files = state["new_files_created"]

    # Check thresholds from lowest to highest
    silent = thresholds.get("silent", {})
    warn_t = thresholds.get("warn", {})
    ask_t = thresholds.get("ask", {})

    # Silent tier: within all silent thresholds
    if (total_lines <= silent.get("maxLines", 20) and
        num_files <= silent.get("maxFiles", 1) and
        new_files <= silent.get("maxNewFiles", 0)):
        return "silent"

    # Warn tier: within warn thresholds
    if (total_lines <= warn_t.get("maxLines", 50) and
        num_files <= warn_t.get("maxFiles", 2) and
        new_files <= warn_t.get("maxNewFiles", 1)):
        return "warn"

    # Ask tier: within ask thresholds
    if (total_lines <= ask_t.get("maxLines", 100) and
        num_files <= ask_t.get("maxFiles", 4) and
        new_files <= ask_t.get("maxNewFiles", 3)):
        return "ask"

    # Block tier: exceeds ask thresholds
    return "block"


def format_session_summary(state: dict) -> str:
    """Format session metrics for display."""
    num_files = len(state["files_touched"])
    total_lines = state["total_lines_added"]
    new_files = state["new_files_created"]

    summary = f"Session: {num_files} files, {total_lines} lines"
    if new_files > 0:
        summary += f", {new_files} new"
    return summary


def output_silent() -> None:
    """Silent exit - no output."""
    sys.exit(0)


def output_warn(message: str) -> None:
    """Warn but allow the edit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "message": message
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def output_ask(reason: str) -> None:
    """Prompt user for confirmation."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def output_block(reason: str) -> None:
    """Block the action."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    config = load_config()

    # Check if enforcement is disabled
    if not config.get("enabled", True):
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    cwd = data.get("cwd", os.getcwd())

    if tool_name not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Check repo exclusion - both CWD and file path
    # This allows editing ~/.claude files even when CWD is another project
    if is_excluded_repo(cwd, config):
        output_silent()

    for repo_path in config.get("exclusions", {}).get("repositories", []):
        if file_path.startswith(repo_path):
            output_silent()

    # Check always-silent patterns
    if is_always_silent(file_path, config):
        output_silent()

    # Load and update state
    state = load_state()
    lines = count_lines(tool_input)
    directory = get_directory(file_path)
    is_new_file = tool_name == "Write"

    if file_path not in state["files_touched"]:
        state["files_touched"].append(file_path)
    if directory not in state["directories_touched"]:
        state["directories_touched"].append(directory)
    if is_new_file:
        state["new_files_created"] += 1
    state["total_lines_added"] += lines

    save_state(state)

    # Calculate enforcement tier
    tier = calculate_tier(state, config)
    summary = format_session_summary(state)

    if tier == "silent":
        output_silent()

    elif tier == "warn":
        output_warn(
            f"⚠️  DELEGATION ENCOURAGED\n\n"
            f"{summary}\n\n"
            f"Consider delegating via Moonbridge:\n"
            f"  spawn_agent(prompt=\"[task]\", adapter=\"codex|kimi\")"
        )

    elif tier == "ask":
        output_ask(
            f"📋 DELEGATION RECOMMENDED\n\n"
            f"{summary}\n\n"
            f"Delegate via Moonbridge:\n"
            f"  spawn_agent(prompt=\"[task]\", adapter=\"codex|kimi\")\n\n"
            f"Continue with direct edit?"
        )

    else:  # block
        output_block(
            f"🛑 DELEGATION REQUIRED\n\n"
            f"{summary}\n\n"
            f"Delegate via MCP:\n"
            f"  spawn_agent(\"[task description]\")\n\n"
            f"Or add repo to exclusions in:\n"
            f"  ~/.claude/config/delegation-enforcement.json"
        )


if __name__ == "__main__":
    main()
