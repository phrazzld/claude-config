#!/usr/bin/env python3
"""
Knowledge extraction reminder hook.

Inspired by Claudeception - injects prompt for Claude to evaluate
whether current session yielded extractable knowledge.

Runs on Stop hook to evaluate entire session context.
"""

import json
import subprocess
import sys

def get_recent_changes():
    """Get files changed in recent commits (context for Claude)."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~3", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except:
        return []

def count_pattern(pattern: str, files: list[str]) -> int:
    """Count pattern occurrences across files."""
    count = 0
    for f in files:
        try:
            result = subprocess.run(
                ["rg", "-c", pattern, f],
                capture_output=True, text=True, timeout=2
            )
            if result.stdout.strip():
                count += int(result.stdout.strip())
        except:
            pass
    return count

def main():
    # Read hook context from stdin
    try:
        context = json.load(sys.stdin)
    except:
        context = {}

    # Gather bonus context about recent work
    changed_files = get_recent_changes()

    hints = []
    if changed_files:
        # Check for patterns that might indicate extractable knowledge
        error_count = count_pattern(r"try\s*{|catch\s*\(|\.catch\(", changed_files)
        if error_count >= 3:
            hints.append("Multiple error handling patterns added")

        type_count = count_pattern(r"type\s+\w+\s*=|interface\s+\w+", changed_files)
        if type_count >= 3:
            hints.append("Multiple type definitions added")

        test_count = count_pattern(r"it\(|test\(|describe\(", changed_files)
        if test_count >= 3:
            hints.append("Multiple tests added")

    # Build the evaluation prompt (Claudeception-style)
    hint_text = ""
    if hints:
        hint_text = f"\n\nDetected patterns that may be worth codifying:\n- " + "\n- ".join(hints)

    prompt = f"""<knowledge-extraction-check>
BEFORE ending this session, evaluate:

Did this session involve:
- Debugging with non-obvious solution (required investigation)?
- Discovering undocumented workaround or pattern?
- Learning project-specific convention that should persist?
- Solving a problem that would help future sessions?

If YES to any, consider: Should this become a skill?

Quality gates (ALL must be true to proceed):
1. REUSABLE - applies beyond this single instance
2. NON-TRIVIAL - required discovery, not just reading docs
3. SPECIFIC - clear trigger conditions can be defined
4. VERIFIED - solution confirmed working

If passes all gates → Invoke skill-builder skill to extract.
If fails any gate → No action needed.{hint_text}
</knowledge-extraction-check>"""

    # Output the prompt for Claude to evaluate
    print(json.dumps({
        "result": "continue",
        "message": prompt
    }))

if __name__ == "__main__":
    main()
