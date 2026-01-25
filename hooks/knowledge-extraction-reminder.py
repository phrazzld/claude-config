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
        # Note: No threshold - default codify philosophy means any pattern is worth considering
        error_count = count_pattern(r"try\s*{|catch\s*\(|\.catch\(", changed_files)
        if error_count > 0:
            hints.append(f"Error handling patterns detected ({error_count})")

        type_count = count_pattern(r"type\s+\w+\s*=|interface\s+\w+", changed_files)
        if type_count > 0:
            hints.append(f"Type definitions added ({type_count})")

        test_count = count_pattern(r"it\(|test\(|describe\(", changed_files)
        if test_count > 0:
            hints.append(f"Tests added ({test_count})")

    # Build the evaluation prompt (Claudeception-style)
    hint_text = ""
    if hints:
        hint_text = f"\n\nDetected patterns that may be worth codifying:\n- " + "\n- ".join(hints)

    prompt = f"""<knowledge-extraction-check>
BEFORE ending this session, evaluate what should be codified:

Review the session for:
- Problems solved (how to prevent them?)
- Feedback received (how to catch earlier?)
- Patterns discovered (how to enforce?)
- Workflows improved (how to encode?)

**Default: Codify.** The question is not "is this worth codifying?" but "what's the best codification target?"

Targets (in order of determinism):
1. Hook - guaranteed enforcement
2. Agent - specialized review
3. Skill - reusable workflow
4. CLAUDE.md - philosophy/convention

For each learning, either:
- Codify it (invoke /codify-learning)
- Justify not codifying (cite existing codification or explain why not generalizable)

"First occurrence" is NOT a valid reason to skip - cross-session memory doesn't exist.{hint_text}
</knowledge-extraction-check>"""

    # Output the prompt for Claude to evaluate
    print(json.dumps({
        "result": "continue",
        "message": prompt
    }))

if __name__ == "__main__":
    main()
