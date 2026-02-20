#!/usr/bin/env python3
"""Brand auto-detection — scan a repo for existing design infrastructure.

Detects brand.yaml, tailwind config, CSS tokens, fonts, component libraries.
Reports completeness score and remediation suggestions.

Standalone: python3 detect.py /path/to/repo
"""

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class BrandState:
    """Structured report of design infrastructure in a repo."""
    repo_path: str
    has_brand_yaml: bool = False
    has_legacy_brand: bool = False
    has_tailwind: bool = False
    has_design_tokens: bool = False
    has_dark_mode: bool = False
    brand_hue: Optional[int] = None
    fonts: list = field(default_factory=list)
    colors: dict = field(default_factory=dict)  # {name: value}
    color_count: int = 0
    component_lib: Optional[str] = None
    framework: Optional[str] = None
    completeness: float = 0.0
    gaps: list = field(default_factory=list)
    remediation: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v}

    def summary(self) -> str:
        lines = [f"Brand State: {self.repo_path}"]
        lines.append(f"  Completeness: {self.completeness:.0%}")

        found = []
        if self.has_brand_yaml:
            found.append("brand.yaml")
        if self.has_legacy_brand:
            found.append("brand-profile.yaml (legacy)")
        if self.has_tailwind:
            found.append("Tailwind CSS")
        if self.has_design_tokens:
            found.append("design tokens")
        if self.has_dark_mode:
            found.append("dark mode")
        if self.framework:
            found.append(self.framework)
        if self.component_lib:
            found.append(self.component_lib)
        if found:
            lines.append(f"  Found: {', '.join(found)}")

        if self.fonts:
            lines.append(f"  Fonts: {', '.join(self.fonts[:5])}")
        if self.brand_hue is not None:
            lines.append(f"  Brand hue: {self.brand_hue}")
        if self.color_count:
            lines.append(f"  Colors: {self.color_count} defined")

        if self.gaps:
            lines.append(f"  Gaps: {', '.join(self.gaps)}")
        if self.remediation:
            lines.append(f"  Remediation:")
            for r in self.remediation:
                lines.append(f"    - {r}")

        return "\n".join(lines)


def detect_brand_state(repo_path: str) -> BrandState:
    """Scan repo for design infrastructure. Returns structured BrandState."""
    root = Path(repo_path).resolve()
    state = BrandState(repo_path=str(root))

    _detect_brand_yaml(root, state)
    _detect_tailwind(root, state)
    _detect_tokens(root, state)
    _detect_fonts(root, state)
    _detect_component_lib(root, state)
    _detect_framework(root, state)
    _detect_dark_mode(root, state)
    _compute_completeness(state)

    return state


# ── Detectors ────────────────────────────────────────────────────────────────

def _detect_brand_yaml(root: Path, state: BrandState):
    """Check for brand.yaml or legacy brand-profile.yaml."""
    brand = root / "brand.yaml"
    if brand.exists():
        state.has_brand_yaml = True
        _parse_brand_yaml(brand, state)
        return

    legacy = root / "brand-profile.yaml"
    if legacy.exists():
        state.has_legacy_brand = True
        state.gaps.append("legacy brand-profile.yaml (needs migration)")
        state.remediation.append("Run /brand-init to migrate to brand.yaml")


def _parse_brand_yaml(path: Path, state: BrandState):
    """Extract key info from brand.yaml."""
    try:
        import yaml
        data = yaml.safe_load(path.read_text())
    except Exception:
        try:
            data = json.loads(path.read_text())
        except Exception:
            return

    if not isinstance(data, dict):
        return

    palette = data.get("palette", {})
    if isinstance(palette, dict):
        hue = palette.get("brand_hue")
        if hue is not None:
            try:
                state.brand_hue = int(hue)
            except (ValueError, TypeError):
                pass
        # Count semantic colors
        color_keys = [k for k in palette if k not in ("brand_hue", "scale")]
        state.color_count = len(color_keys)
        state.colors = {k: palette[k] for k in color_keys
                        if isinstance(palette[k], (str, dict))}

    typography = data.get("typography", {})
    if isinstance(typography, dict):
        for key in ("display", "sans", "serif", "mono"):
            font = typography.get(key)
            if font and font not in state.fonts:
                state.fonts.append(font)


def _detect_tailwind(root: Path, state: BrandState):
    """Check for Tailwind config files."""
    patterns = [
        "tailwind.config.ts", "tailwind.config.js",
        "tailwind.config.mjs", "tailwind.config.cjs",
    ]
    for p in patterns:
        if (root / p).exists():
            state.has_tailwind = True
            _parse_tailwind_config(root / p, state)
            return

    # Also check postcss for tailwind plugin
    for name in ("postcss.config.js", "postcss.config.mjs", "postcss.config.cjs"):
        f = root / name
        if f.exists():
            try:
                text = f.read_text()
                if "tailwindcss" in text:
                    state.has_tailwind = True
                    return
            except Exception:
                pass

    # Tailwind 4: check for @import "tailwindcss" in CSS
    for css in _find_css_files(root):
        try:
            text = css.read_text(errors="replace")
            if '@import "tailwindcss"' in text or "@import 'tailwindcss'" in text:
                state.has_tailwind = True
                return
        except Exception:
            pass


def _parse_tailwind_config(path: Path, state: BrandState):
    """Extract custom theme values from Tailwind config."""
    try:
        text = path.read_text()
    except Exception:
        return

    # Extract font families
    font_matches = re.findall(r'fontFamily\s*:\s*{[^}]*?"(\w+)"\s*:\s*\[', text)
    for f in font_matches:
        if f not in state.fonts:
            state.fonts.append(f)

    # Count custom colors
    color_block = re.search(r'colors\s*:\s*{([^}]+)}', text)
    if color_block:
        color_keys = re.findall(r'(\w+)\s*:', color_block.group(1))
        state.color_count = max(state.color_count, len(color_keys))


def _detect_tokens(root: Path, state: BrandState):
    """Check for compiled design tokens (@theme blocks, tokens.css)."""
    # Check for tokens.css
    for subdir in ("src/styles", "src", "styles", "app"):
        tokens = root / subdir / "tokens.css"
        if tokens.exists():
            state.has_design_tokens = True
            return

    # Check CSS files for @theme blocks
    for css in _find_css_files(root):
        try:
            text = css.read_text(errors="replace")
            if "@theme" in text:
                state.has_design_tokens = True
                _parse_theme_block(text, state)
                return
        except Exception:
            pass


def _parse_theme_block(text: str, state: BrandState):
    """Extract tokens from a @theme CSS block."""
    theme_match = re.search(r'@theme\s*{([^}]+)}', text, re.DOTALL)
    if not theme_match:
        return

    block = theme_match.group(1)

    # Extract brand hue
    hue_match = re.search(r'--brand-hue\s*:\s*(\d+)', block)
    if hue_match and state.brand_hue is None:
        state.brand_hue = int(hue_match.group(1))

    # Count color tokens
    color_vars = re.findall(r'--color-\w+', block)
    state.color_count = max(state.color_count, len(set(color_vars)))

    # Extract font tokens
    font_matches = re.findall(r'--font-\w+\s*:\s*"([^"]+)"', block)
    for f in font_matches:
        name = f.split(",")[0].strip().strip('"').strip("'")
        if name and name not in state.fonts:
            state.fonts.append(name)


def _detect_fonts(root: Path, state: BrandState):
    """Check for Google Fonts imports or local font loading."""
    for css in _find_css_files(root):
        try:
            text = css.read_text(errors="replace")
        except Exception:
            continue

        # Google Fonts
        for m in re.finditer(r'fonts\.googleapis\.com/css2?\?family=([^"&\s]+)', text):
            family = m.group(1).replace("+", " ").split(":")[0]
            if family not in state.fonts:
                state.fonts.append(family)

    # Check Next.js font imports
    for ext in ("ts", "tsx", "js", "jsx"):
        for f in root.glob(f"**/*.{ext}"):
            if "node_modules" in str(f) or ".next" in str(f):
                continue
            try:
                text = f.read_text(errors="replace")
                for m in re.finditer(r"from\s+['\"]next/font/google['\"]", text):
                    # Find font names in the same file
                    for fn in re.finditer(r'(\w+)\s*\(\s*{', text):
                        name = fn.group(1)
                        # Convert PascalCase to space-separated
                        spaced = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)
                        if spaced not in state.fonts and len(spaced) > 2:
                            state.fonts.append(spaced)
                break  # Only check first match per extension
            except Exception:
                continue


def _detect_component_lib(root: Path, state: BrandState):
    """Detect UI component libraries."""
    pkg = root / "package.json"
    if not pkg.exists():
        return

    try:
        data = json.loads(pkg.read_text())
    except Exception:
        return

    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

    if "@radix-ui/react-dialog" in deps or "@radix-ui/themes" in deps:
        state.component_lib = "Radix UI"
    elif "@headlessui/react" in deps:
        state.component_lib = "Headless UI"
    elif "@mui/material" in deps:
        state.component_lib = "MUI"
    elif "antd" in deps:
        state.component_lib = "Ant Design"
    elif "@chakra-ui/react" in deps:
        state.component_lib = "Chakra UI"

    # shadcn/ui detection (components.json)
    if (root / "components.json").exists():
        state.component_lib = "shadcn/ui"


def _detect_framework(root: Path, state: BrandState):
    """Detect frontend framework."""
    pkg = root / "package.json"
    if not pkg.exists():
        return

    try:
        data = json.loads(pkg.read_text())
    except Exception:
        return

    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

    if "next" in deps:
        state.framework = "Next.js"
    elif "@remix-run/react" in deps:
        state.framework = "Remix"
    elif "nuxt" in deps:
        state.framework = "Nuxt"
    elif "astro" in deps:
        state.framework = "Astro"
    elif "svelte" in deps or "@sveltejs/kit" in deps:
        state.framework = "SvelteKit"
    elif "react" in deps:
        state.framework = "React"
    elif "vue" in deps:
        state.framework = "Vue"


def _detect_dark_mode(root: Path, state: BrandState):
    """Check for dark mode support."""
    for css in _find_css_files(root):
        try:
            text = css.read_text(errors="replace")
            if "prefers-color-scheme: dark" in text or ".dark" in text:
                state.has_dark_mode = True
                return
        except Exception:
            continue

    # Check Tailwind config for darkMode
    for name in ("tailwind.config.ts", "tailwind.config.js"):
        f = root / name
        if f.exists():
            try:
                text = f.read_text()
                if "darkMode" in text:
                    state.has_dark_mode = True
                    return
            except Exception:
                pass


def _compute_completeness(state: BrandState):
    """Score 0-1 based on what exists."""
    checks = [
        (state.has_brand_yaml, 0.25, "no brand.yaml", "Run /brand-init"),
        (state.has_tailwind, 0.15, "no Tailwind CSS", "Add Tailwind CSS 4"),
        (state.has_design_tokens, 0.20, "no design tokens", "Run /brand-compile"),
        (len(state.fonts) > 0, 0.10, "no custom fonts", "Define typography in brand.yaml"),
        (state.color_count >= 3, 0.10, "fewer than 3 semantic colors", "Define palette in brand.yaml"),
        (state.has_dark_mode, 0.10, "no dark mode", "Add dark mode tokens"),
        (state.component_lib is not None, 0.05, "no component library", "Consider shadcn/ui or Radix"),
        (state.brand_hue is not None, 0.05, "no brand hue defined", "Set brand_hue in palette"),
    ]

    score = 0.0
    for passes, weight, gap, fix in checks:
        if passes:
            score += weight
        else:
            state.gaps.append(gap)
            state.remediation.append(fix)

    state.completeness = min(1.0, score)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _find_css_files(root: Path, limit: int = 30) -> list:
    """Find CSS files, skipping node_modules and build dirs."""
    skip = {"node_modules", ".next", "dist", "build", ".git", ".design-evolution"}
    results = []
    for css in root.rglob("*.css"):
        if any(s in css.parts for s in skip):
            continue
        results.append(css)
        if len(results) >= limit:
            break
    return results


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect.py /path/to/repo")
        sys.exit(1)

    repo = sys.argv[1]
    state = detect_brand_state(repo)
    print(state.summary())
    if "--json" in sys.argv:
        print(json.dumps(state.as_dict(), indent=2))
