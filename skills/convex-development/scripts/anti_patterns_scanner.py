#!/usr/bin/env python3
"""
Scan Convex code for common anti-patterns.

Usage:
    python anti_patterns_scanner.py <convex_directory>
    python anti_patterns_scanner.py ./convex

Returns JSON with detected anti-patterns and recommendations.
"""

import sys
import os
import re
import json
from pathlib import Path


def scan_file(file_path: Path) -> list:
    """Scan a single file for anti-patterns."""
    findings = []
    content = file_path.read_text()
    lines = content.split('\n')

    # Pattern 1: Unbounded .collect() without pagination
    for i, line in enumerate(lines, 1):
        if '.collect()' in line and 'paginate' not in content[:content.find(line)]:
            # Check if there's a .take() or pagination nearby
            context_start = max(0, i - 10)
            context = '\n'.join(lines[context_start:i])
            if '.take(' not in context and '.paginate(' not in context and '.first()' not in context and '.unique()' not in context:
                findings.append({
                    "file": str(file_path),
                    "line": i,
                    "pattern": "unbounded_collect",
                    "severity": "high",
                    "message": "Unbounded .collect() - consider using .paginate(), .take(n), or .first()",
                    "code": line.strip()
                })

    # Pattern 2: .filter() instead of .withIndex()
    filter_pattern = r'\.filter\s*\(\s*\(?q\)?.*q\.eq'
    for i, line in enumerate(lines, 1):
        if re.search(filter_pattern, line):
            findings.append({
                "file": str(file_path),
                "line": i,
                "pattern": "filter_instead_of_index",
                "severity": "high",
                "message": "Using .filter() with .eq() - use .withIndex() for efficient querying",
                "code": line.strip()
            })

    # Pattern 3: User-provided auth data
    auth_pattern = r'args:\s*\{[^}]*(?:userId|userEmail|userName|tokenIdentifier):\s*v\.(?:string|id)'
    if re.search(auth_pattern, content, re.MULTILINE | re.DOTALL):
        # Check if ctx.auth is also used
        if 'ctx.auth.getUserIdentity' not in content:
            for i, line in enumerate(lines, 1):
                if re.search(r'userId|userEmail|userName', line) and 'args' in line:
                    findings.append({
                        "file": str(file_path),
                        "line": i,
                        "pattern": "user_provided_auth",
                        "severity": "critical",
                        "message": "User-provided auth data in args without ctx.auth verification - security risk",
                        "code": line.strip()
                    })
                    break

    # Pattern 4: Sequential await in for loop (N+1 pattern)
    for_await_pattern = r'for\s*\([^)]*of\s+\w+\)\s*\{[^}]*await\s+ctx\.db'
    matches = list(re.finditer(for_await_pattern, content, re.DOTALL))
    for match in matches:
        line_num = content[:match.start()].count('\n') + 1
        findings.append({
            "file": str(file_path),
            "line": line_num,
            "pattern": "n_plus_one_query",
            "severity": "high",
            "message": "Sequential await in for loop - use Promise.all() for parallel queries",
            "code": match.group()[:100] + "..."
        })

    # Pattern 5: Missing argument validators
    func_pattern = r'export\s+const\s+\w+\s*=\s*(query|mutation|action)\s*\(\s*\{[^}]*handler'
    for match in re.finditer(func_pattern, content):
        func_text = content[match.start():match.end() + 200]
        if 'args:' not in func_text.split('handler')[0]:
            line_num = content[:match.start()].count('\n') + 1
            findings.append({
                "file": str(file_path),
                "line": line_num,
                "pattern": "missing_args_validator",
                "severity": "medium",
                "message": "Public function without argument validators - add args: {} or explicit validators",
                "code": func_text[:80] + "..."
            })

    # Pattern 6: Hardcoded API keys
    key_patterns = [
        r'["\']sk-[a-zA-Z0-9]{20,}["\']',
        r'["\']api[_-]?key["\']:\s*["\'][^"\']+["\']',
        r'apiKey\s*=\s*["\'][^"\']{10,}["\']'
    ]
    for pattern in key_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1
            findings.append({
                "file": str(file_path),
                "line": line_num,
                "pattern": "hardcoded_secret",
                "severity": "critical",
                "message": "Possible hardcoded API key - use environment variables via dashboard",
                "code": "[REDACTED]"
            })

    # Pattern 7: Scheduling public functions
    if 'crons.' in content or 'ctx.scheduler' in content:
        if 'api.' in content and 'internal.' not in content:
            for i, line in enumerate(lines, 1):
                if ('crons.' in line or 'scheduler' in line) and 'api.' in line:
                    findings.append({
                        "file": str(file_path),
                        "line": i,
                        "pattern": "scheduling_public_function",
                        "severity": "high",
                        "message": "Scheduling public function - use internal.* for scheduled tasks",
                        "code": line.strip()
                    })

    # Pattern 8: Mixed update frequencies in schema
    if 'schema.ts' in str(file_path):
        # Look for tables with both static and dynamic fields
        table_pattern = r'defineTable\s*\(\s*\{([^}]+)\}'
        for match in re.finditer(table_pattern, content):
            fields = match.group(1)
            static_fields = ['title', 'content', 'body', 'name', 'description']
            dynamic_fields = ['viewCount', 'lastViewed', 'updatedAt', 'clickCount', 'likes']

            has_static = any(f in fields for f in static_fields)
            has_dynamic = any(f in fields for f in dynamic_fields)

            if has_static and has_dynamic:
                line_num = content[:match.start()].count('\n') + 1
                findings.append({
                    "file": str(file_path),
                    "line": line_num,
                    "pattern": "mixed_update_frequency",
                    "severity": "medium",
                    "message": "Table mixes static and frequently-updated fields - consider splitting for bandwidth optimization",
                    "code": match.group()[:100] + "..."
                })

    return findings


def scan_directory(convex_dir: str) -> dict:
    """Scan entire convex directory for anti-patterns."""
    results = {
        "scanned_files": 0,
        "findings": [],
        "summary": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
    }

    convex_path = Path(convex_dir)

    if not convex_path.exists():
        results["error"] = f"Directory does not exist: {convex_dir}"
        return results

    # Scan all TypeScript files
    for ts_file in convex_path.glob("**/*.ts"):
        # Skip generated files
        if "_generated" in str(ts_file):
            continue

        results["scanned_files"] += 1
        findings = scan_file(ts_file)
        results["findings"].extend(findings)

    # Update summary
    for finding in results["findings"]:
        severity = finding.get("severity", "medium")
        results["summary"][severity] = results["summary"].get(severity, 0) + 1

    return results


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: anti_patterns_scanner.py <convex_directory>",
            "scanned_files": 0,
            "findings": [],
            "summary": {}
        }))
        sys.exit(1)

    convex_dir = sys.argv[1]
    results = scan_directory(convex_dir)

    print(json.dumps(results, indent=2))

    # Exit with error code if critical issues found
    if results["summary"].get("critical", 0) > 0:
        sys.exit(2)
    elif results["summary"].get("high", 0) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
