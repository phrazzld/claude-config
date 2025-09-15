#!/usr/bin/env python3
"""
Claude Code PreToolUse hook to remind about using ripgrep (rg) or ast-grep
instead of regular grep for better performance and functionality.

This hook runs before Grep and Bash tool calls to provide gentle reminders
about using more efficient alternatives.
"""

import json
import sys
import re

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Initialize response
        response = {
            "continue": True,  # Don't block the tool call
            "suppressOutput": True  # Don't show raw output in transcript
        }

        # Check for Grep tool usage
        if tool_name == "Grep":
            response["systemMessage"] = (
                "🔍 Reminder: The Grep tool already uses ripgrep (rg) internally for optimal performance. "
                "For semantic code search, consider using ast-grep for structural pattern matching."
            )

        # Check for Bash commands containing grep
        elif tool_name == "Bash":
            command = tool_input.get("command", "")

            # Check if command contains grep (but not ripgrep or ast-grep)
            grep_pattern = r'\bgrep\b'
            rg_pattern = r'\brg\b|\bripgrep\b'
            ast_pattern = r'\bast-grep\b'

            if (re.search(grep_pattern, command) and
                not re.search(rg_pattern, command) and
                not re.search(ast_pattern, command)):

                # Provide context-aware suggestions
                suggestions = []

                # Basic grep usage
                if re.search(r'grep\s+["\'].*?["\']', command) or re.search(r'grep\s+-\w*\s+["\'].*?["\']', command):
                    suggestions.append("• Use 'rg <pattern>' for faster file content search")

                # Recursive grep
                if re.search(r'grep\s+-r', command):
                    suggestions.append("• Use 'rg <pattern>' (recursive by default)")

                # Case insensitive
                if re.search(r'grep\s+-i', command):
                    suggestions.append("• Use 'rg -i <pattern>' for case-insensitive search")

                # Files with matches only
                if re.search(r'grep\s+-l', command):
                    suggestions.append("• Use 'rg -l <pattern>' to list files with matches")

                # For code structure search
                if re.search(r'grep.*\b(function|class|def|impl|struct)\b', command):
                    suggestions.append("• Consider 'ast-grep' for semantic code structure search")

                # Build the message
                message = "🔍 Performance tip: Consider using ripgrep (rg) or ast-grep instead of grep:\n"

                if suggestions:
                    message += "\n".join(suggestions)
                else:
                    message += (
                        "• 'rg <pattern>' - Faster alternative to grep with better defaults\n"
                        "• 'ast-grep' - Semantic code search for structural patterns"
                    )

                message += "\n\nThese tools are pre-installed and optimized for code search."

                response["systemMessage"] = message

        # Output the response
        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        # On error, allow the tool to continue but log the issue
        error_response = {
            "continue": True,
            "systemMessage": f"Hook error (non-blocking): {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(0)

if __name__ == "__main__":
    main()