#!/usr/bin/env python3
"""Block direct git push to master/main from within Claude Code.

Exit 0 + JSON with permissionDecision: "deny" = block the command
Exit 0 + no output = allow the command
"""
import json
import re
import subprocess
import sys


def deny(reason: str) -> None:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"BLOCKED: {reason}\n\n"
                "Create a feature branch and open a PR instead."
            ),
        }
    }
    print(json.dumps(output))
    sys.exit(0)


data = json.load(sys.stdin)
if data.get("tool_name") != "Bash":
    sys.exit(0)

cmd = data.get("tool_input", {}).get("command", "")
if not re.search(r"\bgit\s+push\b", cmd):
    sys.exit(0)

# Explicit destination: git push origin master / git push origin main
if re.search(r"\bgit\s+push\b.*\b(master|main)\b", cmd):
    deny("Direct push to master/main is prohibited.")

# Ambiguous destination (git push / git push origin / git push origin HEAD):
# resolve via current branch
try:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()
    if branch in ("master", "main"):
        deny(f"Current branch is '{branch}' — direct push to master/main is prohibited.")
except Exception:
    pass

sys.exit(0)
