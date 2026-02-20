#!/usr/bin/env python3
"""Recraft AI integration — vector logos, icons, and image vectorization.

Uses OpenAI-compatible API at https://external.api.recraft.ai/v1.
Auth: RECRAFT_AI_API_KEY (preferred) or RECRAFT_API_TOKEN (legacy).

Standalone test: RECRAFT_AI_API_KEY=xxx python3 recraft.py test
"""

import json
import os
import sys
import base64
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

API_BASE = "https://external.api.recraft.ai/v1"

# Styles that produce vector (SVG) output
VECTOR_STYLES = ("vector_illustration", "icon")
RASTER_STYLES = ("realistic_image", "digital_illustration")

# Recraft V3 substyles for vector_illustration
VECTOR_SUBSTYLES = (
    "flat_2_0", "engraving", "line_art", "line_circuit",
    "linocut", "doodle_fill", "doodle_offset_fill",
)


@dataclass
class GeneratedImage:
    style: str
    url: str = ""
    b64_json: Optional[str] = None
    local_path: Optional[str] = None


def _get_token() -> str:
    """Get API token from env."""
    for name in ("RECRAFT_AI_API_KEY", "RECRAFT_API_TOKEN"):
        token = os.environ.get(name, "").strip()
        if token:
            return token

    raise RuntimeError(
        "Missing Recraft API key. Set RECRAFT_AI_API_KEY (preferred) "
        "or RECRAFT_API_TOKEN. Get one at https://app.recraft.ai/profile/api"
    )


def _api_request(endpoint: str, payload: dict) -> dict:
    """Make authenticated POST to Recraft API."""
    token = _get_token()
    url = f"{API_BASE}{endpoint}"
    data = json.dumps(payload).encode()

    req = urllib.request.Request(
        url, data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"Recraft API {e.code}: {body}") from e


# ── Generation ───────────────────────────────────────────────────────────────

def generate_logo(prompt: str, brand_colors: list = None,
                  substyle: str = None, size: str = "1024x1024",
                  n: int = 4) -> list:
    """Generate vector logos. Returns list of GeneratedImage.

    Args:
        prompt: Description of the logo
        brand_colors: List of RGB tuples, e.g. [(26, 26, 46), (233, 69, 96)]
        substyle: Recraft V3 vector substyle (flat_2_0, line_art, etc.)
        size: Image dimensions
        n: Number of images (1-6)
    """
    payload = {
        "prompt": prompt,
        "style": "vector_illustration",
        "model": "recraftv3",
        "size": size,
        "n": min(n, 6),
        "response_format": "b64_json",
    }

    if substyle:
        payload["substyle"] = substyle

    controls = {}
    if brand_colors:
        controls["colors"] = [{"rgb": list(c)} for c in brand_colors]
    if controls:
        payload["controls"] = controls

    result = _api_request("/images/generations", payload)
    return [
        GeneratedImage(
            url=img.get("url", ""),
            style="vector_illustration",
            b64_json=img.get("b64_json"),
        )
        for img in result.get("data", [])
    ]


def generate_icon(prompt: str, brand_colors: list = None,
                  size: str = "1024x1024", n: int = 4) -> list:
    """Generate UI icons. Returns list of GeneratedImage."""
    payload = {
        "prompt": prompt,
        "style": "icon",
        "model": "recraft20b",
        "size": size,
        "n": min(n, 6),
        "response_format": "b64_json",
    }

    controls = {}
    if brand_colors:
        controls["colors"] = [{"rgb": list(c)} for c in brand_colors]
    if controls:
        payload["controls"] = controls

    result = _api_request("/images/generations", payload)
    return [
        GeneratedImage(
            url=img.get("url", ""),
            style="icon",
            b64_json=img.get("b64_json"),
        )
        for img in result.get("data", [])
    ]


def generate_illustration(prompt: str, style: str = "digital_illustration",
                          brand_colors: list = None,
                          size: str = "1024x1024", n: int = 4) -> list:
    """Generate raster illustrations. Returns list of GeneratedImage."""
    payload = {
        "prompt": prompt,
        "style": style,
        "model": "recraftv3",
        "size": size,
        "n": min(n, 6),
        "response_format": "b64_json",
    }

    controls = {}
    if brand_colors:
        controls["colors"] = [{"rgb": list(c)} for c in brand_colors]
    if controls:
        payload["controls"] = controls

    result = _api_request("/images/generations", payload)
    return [
        GeneratedImage(
            url=img.get("url", ""),
            style=style,
            b64_json=img.get("b64_json"),
        )
        for img in result.get("data", [])
    ]


def vectorize(image_url: str) -> str:
    """Convert raster image to SVG. Returns URL of vectorized image."""
    result = _api_request("/images/vectorize", {"image_url": image_url})
    return result.get("data", [{}])[0].get("url", "")


# ── Download ─────────────────────────────────────────────────────────────────

def download_and_save(images: list, output_dir: Path,
                      prefix: str = "recraft") -> list:
    """Download generated images, save locally. Returns list of saved paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    token = None
    try:
        token = _get_token()
    except RuntimeError:
        token = None

    for i, img in enumerate(images):
        # Determine extension from style
        ext = "svg" if img.style in VECTOR_STYLES else "png"
        filename = f"{prefix}-{i + 1}.{ext}"
        filepath = output_dir / filename

        try:
            if img.b64_json:
                filepath.write_bytes(base64.b64decode(img.b64_json))
            else:
                headers = {"Authorization": f"Bearer {token}"} if token else {}
                req = urllib.request.Request(img.url, headers=headers, method="GET")
                with urllib.request.urlopen(req, timeout=120) as resp:
                    filepath.write_bytes(resp.read())
            img.local_path = str(filepath)
            saved.append(filepath)
        except Exception as e:
            print(f"  Failed to download {img.url}: {e}", file=sys.stderr)

    return saved


# ── Color helpers ────────────────────────────────────────────────────────────

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert #hex to (R, G, B) tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def parse_color_arg(color_str: str) -> list:
    """Parse comma-separated hex colors: '#1a1a2e,#e94560' → [(26,26,46), (233,69,96)]."""
    if not color_str:
        return []
    return [hex_to_rgb(c.strip()) for c in color_str.split(",")]


# ── CLI ──────────────────────────────────────────────────────────────────────

def _cli():
    import argparse
    p = argparse.ArgumentParser(prog="recraft", description="Recraft AI image generation")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("logo", help="Generate vector logos")
    s.add_argument("prompt", help="Logo description")
    s.add_argument("--colors", help="Brand colors as hex: '#1a1a2e,#e94560'")
    s.add_argument("--substyle", choices=VECTOR_SUBSTYLES)
    s.add_argument("--size", default="1024x1024")
    s.add_argument("--n", type=int, default=4)
    s.add_argument("--out", default=".", help="Output directory")

    s = sub.add_parser("icon", help="Generate UI icons")
    s.add_argument("prompt", help="Icon description")
    s.add_argument("--colors", help="Brand colors as hex")
    s.add_argument("--size", default="1024x1024")
    s.add_argument("--n", type=int, default=4)
    s.add_argument("--out", default=".", help="Output directory")

    s = sub.add_parser("illustrate", help="Generate illustrations")
    s.add_argument("prompt", help="Illustration description")
    s.add_argument("--style", default="digital_illustration",
                   choices=["digital_illustration", "realistic_image"])
    s.add_argument("--colors", help="Brand colors as hex")
    s.add_argument("--size", default="1024x1024")
    s.add_argument("--n", type=int, default=4)
    s.add_argument("--out", default=".", help="Output directory")

    s = sub.add_parser("vectorize", help="Convert raster to SVG")
    s.add_argument("image_url", help="URL of image to vectorize")

    sub.add_parser("test", help="Quick API connectivity test")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(1)

    if args.cmd == "test":
        print("Testing Recraft API connectivity...")
        try:
            images = generate_logo("simple geometric circle logo", n=1)
            print(f"  Generated {len(images)} image(s)")
            for img in images:
                print(f"  URL: {img.url[:80]}...")
            print("  API test passed.")
        except Exception as e:
            print(f"  API test failed: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.cmd == "logo":
        colors = parse_color_arg(args.colors) if args.colors else None
        images = generate_logo(args.prompt, brand_colors=colors,
                               substyle=args.substyle, size=args.size, n=args.n)
        saved = download_and_save(images, Path(args.out), "logo")
        for s in saved:
            print(f"  Saved: {s}")

    elif args.cmd == "icon":
        colors = parse_color_arg(args.colors) if args.colors else None
        images = generate_icon(args.prompt, brand_colors=colors,
                               size=args.size, n=args.n)
        saved = download_and_save(images, Path(args.out), "icon")
        for s in saved:
            print(f"  Saved: {s}")

    elif args.cmd == "illustrate":
        colors = parse_color_arg(args.colors) if args.colors else None
        images = generate_illustration(args.prompt, style=args.style,
                                       brand_colors=colors, size=args.size, n=args.n)
        saved = download_and_save(images, Path(args.out), "illustration")
        for s in saved:
            print(f"  Saved: {s}")

    elif args.cmd == "vectorize":
        url = vectorize(args.image_url)
        print(f"  Vectorized: {url}")


if __name__ == "__main__":
    _cli()
