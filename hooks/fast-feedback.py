#!/usr/bin/env python3
"""
Fast feedback after every file edit.

PostToolUse hook that runs type checking immediately after Edit/Write/MultiEdit.
Detects project type and runs appropriate fast check (~2-5s).
Exit 0 always (inform, don't block) - Claude sees errors and self-corrects.
"""
import subprocess
import sys
import os
import json

def get_cwd():
    """Get working directory from hook input or fallback to env."""
    try:
        hook_input = json.loads(sys.stdin.read())
        return hook_input.get("cwd", os.getcwd())
    except:
        return os.getcwd()

def detect_project(cwd):
    """Detect project type based on config files."""
    # TypeScript: require tsconfig.json, not just package.json
    if os.path.exists(os.path.join(cwd, "tsconfig.json")):
        return "typescript"
    if os.path.exists(os.path.join(cwd, "pyproject.toml")) or \
       os.path.exists(os.path.join(cwd, "setup.py")):
        return "python"
    if os.path.exists(os.path.join(cwd, "Cargo.toml")):
        return "rust"
    if os.path.exists(os.path.join(cwd, "go.mod")):
        return "go"
    if os.path.exists(os.path.join(cwd, "Package.swift")):
        return "swift"
    return None

def run_check(project_type, cwd):
    """Run fast type check for detected project type."""
    commands = {
        "typescript": ["npx", "tsc", "--noEmit", "--pretty"],
        "python": ["ruff", "check", "."],
        "rust": ["cargo", "check", "--message-format=short"],
        "go": ["go", "vet", "./..."],
        "swift": ["swift", "build", "--build-tests"],
    }

    timeouts = {
        "typescript": 30,
        "python": 15,
        "rust": 60,
        "go": 30,
        "swift": 60,
    }

    cmd = commands.get(project_type)
    timeout = timeouts.get(project_type, 30)

    if not cmd:
        return None

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        return result
    except FileNotFoundError:
        return None  # Command not installed, skip
    except subprocess.TimeoutExpired:
        return None  # Took too long, skip

def main():
    cwd = get_cwd()
    project_type = detect_project(cwd)

    if not project_type:
        sys.exit(0)  # Not a recognized project, skip silently

    result = run_check(project_type, cwd)

    if result and result.returncode != 0:
        # Output errors for Claude to see and self-correct
        output = result.stdout + result.stderr
        if output.strip():
            print(f"[fast-feedback] {project_type} issues:\n{output.strip()}")

    # Always exit 0 - inform but don't block mid-edit
    sys.exit(0)

if __name__ == "__main__":
    main()
