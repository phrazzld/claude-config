#!/usr/bin/env python3
"""Search curated prompt library using grep patterns.

Usage:
    python search_prompts.py "avatar professional"
    python search_prompts.py "social media instagram" --category social_media
    python search_prompts.py "product shot" --limit 5
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REFERENCES_DIR = Path(__file__).parent.parent / "references"

CATEGORIES = [
    "avatars",
    "social_media",
    "product_marketing",
    "infographic",
    "thumbnails",
    "comics",
    "ecommerce",
    "game_assets",
    "posters",
    "web_design",
]


def search_prompts(query: str, category: str | None = None, limit: int = 3) -> list[dict]:
    """Search prompts using case-insensitive pattern matching.

    Returns list of {category, prompt, index} dicts.
    """
    results = []
    pattern = re.compile(query, re.IGNORECASE)

    categories_to_search = [category] if category else CATEGORIES

    for cat in categories_to_search:
        filepath = REFERENCES_DIR / f"{cat}.json"
        if not filepath.exists():
            continue

        try:
            with open(filepath, "r") as f:
                prompts = json.load(f)

            for i, prompt in enumerate(prompts):
                prompt_text = prompt if isinstance(prompt, str) else prompt.get("prompt", "")
                if pattern.search(prompt_text):
                    results.append({
                        "category": cat,
                        "prompt": prompt_text,
                        "index": i,
                    })

                    if len(results) >= limit:
                        return results
        except (json.JSONDecodeError, KeyError):
            continue

    return results


def main():
    parser = argparse.ArgumentParser(description="Search curated prompt library")
    parser.add_argument("query", help="Search terms (supports regex)")
    parser.add_argument("--category", "-c", choices=CATEGORIES, help="Limit to category")
    parser.add_argument("--limit", "-l", type=int, default=3, help="Max results (default: 3)")

    args = parser.parse_args()

    results = search_prompts(args.query, args.category, args.limit)

    if not results:
        print(f"No prompts found matching '{args.query}'")
        print(f"\nAvailable categories: {', '.join(CATEGORIES)}")
        sys.exit(1)

    print(f"Found {len(results)} matching prompt(s):\n")

    for i, result in enumerate(results, 1):
        print(f"[{i}] Category: {result['category']}")
        print(f"    {result['prompt'][:200]}{'...' if len(result['prompt']) > 200 else ''}")
        print()

    # Output JSON for programmatic use
    if os.environ.get("OUTPUT_JSON"):
        print("\n---JSON---")
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
