#!/usr/bin/env python3
"""
Fast feedback after every file edit.

PostToolUse hook that runs type checking and linting immediately after Edit/Write/MultiEdit.
Detects project type and runs appropriate fast checks (~2-5s).
Exit 0 always (inform, don't block) - Claude sees errors and self-corrects.
"""
import subprocess
import sys
import os
import json

def parse_hook_input():
    """Parse hook input JSON, extracting cwd and edited file path."""
    try:
        hook_input = json.loads(sys.stdin.read())
        cwd = hook_input.get("cwd", os.getcwd())
        # Extract file_path from tool_input (Edit/Write/MultiEdit)
        tool_input = hook_input.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        return cwd, file_path
    except Exception:
        return os.getcwd(), ""

def detect_project(cwd):
    """Detect project type based on config files."""
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
        return None
    except subprocess.TimeoutExpired:
        return None

def run_eslint_on_file(file_path, cwd):
    """Run ESLint on a single file (~1-2s vs 10-30s for full project)."""
    if not file_path or not file_path.endswith((".ts", ".tsx", ".js", ".jsx")):
        return None

    # Require eslint config in project
    has_config = any(
        os.path.exists(os.path.join(cwd, f))
        for f in ("eslint.config.js", "eslint.config.mjs", "eslint.config.ts",
                   ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml")
    )
    if not has_config:
        return None

    abs_path = file_path if os.path.isabs(file_path) else os.path.join(cwd, file_path)
    if not os.path.exists(abs_path):
        return None

    try:
        result = subprocess.run(
            ["npx", "eslint", "--no-warn-ignored", "--format", "compact", abs_path],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=cwd
        )
        return result
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

def run_astgrep_on_file(file_path, cwd):
    """Run ast-grep scan on a single file if guardrails/sgconfig.yml exists."""
    if not file_path:
        return None

    sgconfig = os.path.join(cwd, "guardrails", "sgconfig.yml")
    if not os.path.exists(sgconfig):
        return None

    abs_path = file_path if os.path.isabs(file_path) else os.path.join(cwd, file_path)
    if not os.path.exists(abs_path):
        return None

    try:
        result = subprocess.run(
            ["sg", "scan", "--config", sgconfig, abs_path],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=cwd
        )
        return result
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

def main():
    cwd, file_path = parse_hook_input()
    project_type = detect_project(cwd)

    if not project_type:
        sys.exit(0)

    messages = []

    # 1. Type check (existing behavior)
    result = run_check(project_type, cwd)
    if result and result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        if output:
            messages.append(f"[fast-feedback] {project_type} issues:\n{output}")

    # 2. Per-file ESLint (TS/JS only, ~1-2s)
    if project_type == "typescript" and file_path:
        lint_result = run_eslint_on_file(file_path, cwd)
        if lint_result and lint_result.returncode != 0:
            output = (lint_result.stdout + lint_result.stderr).strip()
            if output:
                messages.append(f"[fast-feedback] eslint:\n{output}")

    # 3. Per-file ast-grep (any language, if guardrails configured)
    if file_path:
        sg_result = run_astgrep_on_file(file_path, cwd)
        if sg_result and sg_result.returncode != 0:
            output = (sg_result.stdout + sg_result.stderr).strip()
            if output:
                messages.append(f"[fast-feedback] guardrails:\n{output}")

    if messages:
        print("\n".join(messages))

    sys.exit(0)

if __name__ == "__main__":
    main()
