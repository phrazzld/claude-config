#!/usr/bin/env python3
"""
Hearthstone design system guard for Claude Code.

Blocks code that violates Hearthstone design system rules in the Heartbeat project:
1. Hardcoded colors outside CSS definitions
2. Banned fonts (Inter, Roboto, Space Grotesk, Noto Serif JP, Manrope)
3. Old animation classes (animate-km-*, animate-zen-*)
4. Non-Hearthstone design tokens

Only applies to /Users/phaedrus/Development/heartbeat project.

PreToolUse hook - runs before Edit/Write/MultiEdit commands.
"""
import json
import os
import re
import sys

# Project scope - only enforce in Heartbeat
HEARTBEAT_PATH = "/Users/phaedrus/Development/heartbeat"

# Banned fonts - these are from other design systems
BANNED_FONTS = [
    "Inter",
    "Roboto",
    "Space Grotesk",
    "Noto Serif JP",
    "Noto Serif",
    "Manrope",
]

# Old animation patterns that should be replaced
OLD_ANIMATIONS = [
    r'animate-km-',
    r'animate-zen-',
]

# Allowed file patterns for CSS variable definitions
CSS_DEFINITION_FILES = [
    r'globals\.css$',
    r'tokens\.css$',
    r'\.css$',  # Any CSS file can define tokens
]

# Hardcoded color patterns (hex, rgb, hsl)
# Only block in non-CSS files, and only for specific color-like patterns
HARDCODED_COLOR_PATTERNS = [
    # 6-digit hex colors (but allow common ones like #000, #fff, white, black)
    (r'["\']#[0-9a-fA-F]{6}["\']', "hardcoded hex color"),
    (r'bg-\[#[0-9a-fA-F]{6}\]', "hardcoded Tailwind hex"),
    (r'text-\[#[0-9a-fA-F]{6}\]', "hardcoded Tailwind hex"),
    (r'border-\[#[0-9a-fA-F]{6}\]', "hardcoded Tailwind hex"),
    # rgb/rgba in inline styles
    (r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)', "hardcoded rgb color"),
]

# Exceptions - these patterns are allowed even with hardcoded colors
COLOR_EXCEPTIONS = [
    r'--color-',  # CSS variable definitions
    r'var\(--',   # CSS variable usage
    r'\.svg',     # SVG files
    r'\.md',      # Markdown files
    r'currentColor',
    r'transparent',
    r'inherit',
]

# Files where hardcoded colors are allowed (theme previews, etc)
COLOR_ALLOWED_FILES = [
    r'lib/themes\.ts$',  # Theme preview colors for UI
    r'\.css$',           # CSS files
]


def is_heartbeat_project(file_path: str) -> bool:
    """Check if the file is in the Heartbeat project."""
    if not file_path:
        return False
    return file_path.startswith(HEARTBEAT_PATH)


def is_css_file(file_path: str) -> bool:
    """Check if file is a CSS file where token definitions are allowed."""
    if not file_path:
        return False
    basename = os.path.basename(file_path)
    for pattern in CSS_DEFINITION_FILES:
        if re.search(pattern, basename):
            return True
    return False


def check_banned_fonts(content: str, file_path: str) -> tuple[bool, str]:
    """Check for banned fonts in the content."""
    if not content:
        return False, ""

    for font in BANNED_FONTS:
        # Look for font-family declarations or font imports
        patterns = [
            rf'font-family:\s*["\']?{font}',
            rf'@import.*{font}',
            rf'from\s+["\']next/font.*{font}',
            rf'{font}\s*\(',  # next/font import
        ]
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True, (
                    f"🔥 HEARTHSTONE DESIGN GUARD: Banned font '{font}' detected\n\n"
                    f"File: {file_path}\n\n"
                    "Hearthstone uses Lora (display) + Nunito (body) typography.\n"
                    "Replace with:\n"
                    "  - Display: Lora\n"
                    "  - Body: Nunito\n"
                    "  - Mono: IBM Plex Mono"
                )
    return False, ""


def check_old_animations(content: str, file_path: str) -> tuple[bool, str]:
    """Check for old Kyoto Moss animation classes."""
    if not content:
        return False, ""

    for pattern in OLD_ANIMATIONS:
        match = re.search(pattern, content)
        if match:
            old_class = match.group(0)
            return True, (
                f"🔥 HEARTHSTONE DESIGN GUARD: Old animation class detected\n\n"
                f"File: {file_path}\n"
                f"Found: {old_class}...\n\n"
                "Hearthstone uses hs-* animations instead of km-*/zen-*.\n"
                "Replace with:\n"
                "  - animate-km-breathe → animate-hs-ember-pulse\n"
                "  - animate-km-breathe-subtle → animate-hs-ember-flicker\n"
                "  - animate-km-fade-in → animate-hs-fade-in\n"
                "  - animate-zen-* → animate-hs-*"
            )
    return False, ""


def is_color_allowed_file(file_path: str) -> bool:
    """Check if file is allowed to have hardcoded colors."""
    if not file_path:
        return False
    for pattern in COLOR_ALLOWED_FILES:
        if re.search(pattern, file_path):
            return True
    return False


def check_hardcoded_colors(content: str, file_path: str) -> tuple[bool, str]:
    """Check for hardcoded colors outside CSS files."""
    if not content:
        return False, ""

    # Allow in CSS files and theme preview files
    if is_css_file(file_path) or is_color_allowed_file(file_path):
        return False, ""

    # Check each color pattern
    for pattern, desc in HARDCODED_COLOR_PATTERNS:
        matches = re.findall(pattern, content)
        for match in matches:
            # Check if it's in an exception context
            line_context = content[max(0, content.find(match) - 50):content.find(match) + 50]

            is_exception = any(
                re.search(exc, line_context) for exc in COLOR_EXCEPTIONS
            )

            if not is_exception:
                return True, (
                    f"🔥 HEARTHSTONE DESIGN GUARD: Hardcoded color detected\n\n"
                    f"File: {file_path}\n"
                    f"Found: {match} ({desc})\n\n"
                    "Hearthstone uses CSS variables for all colors.\n"
                    "Use design tokens instead:\n"
                    "  - bg-[var(--color-bg-primary)]\n"
                    "  - text-[var(--color-text-primary)]\n"
                    "  - border-[var(--color-border-default)]\n\n"
                    "Or status colors:\n"
                    "  - bg-up / text-up\n"
                    "  - bg-degraded / text-degraded\n"
                    "  - bg-down / text-down"
                )
    return False, ""


def block(reason: str) -> None:
    """Block the command."""
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

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}

    # Only check Edit/Write/MultiEdit
    if tool_name not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")

    # Only enforce in Heartbeat project
    if not is_heartbeat_project(file_path):
        sys.exit(0)

    # Get content to check
    content = tool_input.get("content", "") or tool_input.get("new_string", "")

    if not content:
        sys.exit(0)

    # Run checks
    checks = [
        check_banned_fonts,
        check_old_animations,
        check_hardcoded_colors,
    ]

    for check_fn in checks:
        should_block, reason = check_fn(content, file_path)
        if should_block:
            block(reason)

    sys.exit(0)


if __name__ == "__main__":
    main()
