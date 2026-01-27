#!/usr/bin/env ts-node
/* eslint-disable no-console */
import fs from "node:fs";
import path from "node:path";
import satori from "satori";
import sharp from "sharp";
import React from "react";
import { BlogCard } from "../templates/blog";
import { ProductCard } from "../templates/product";
import { ChangelogCard } from "../templates/changelog";

const WIDTH = 1200;
const HEIGHT = 630;

type TemplateName = "blog" | "product" | "changelog" | "comparison";

type Theme = {
  brandName: string;
  fontPath?: string;
  colors: {
    background: string;
    foreground: string;
    accent: string;
    muted: string;
  };
};

type CommonProps = {
  title: string;
  theme: Theme;
  date?: string;
  author?: string;
  version?: string;
  tagline?: string;
  competitor?: string;
};

async function main(): Promise<void> {
  const { template, title, extras, flags } = parseArgs(process.argv.slice(2));
  const theme = readTheme();
  const props: CommonProps = {
    title,
    theme,
    author: flags.author ?? extras.author,
    date: flags.date ?? extras.date,
    version: flags.version ?? extras.version,
    tagline: normalizeFlag(flags.tagline),
    competitor: normalizeFlag(flags.competitor),
  };

  const element = renderTemplate(template, props);
  const svg = await satori(element, {
    width: WIDTH,
    height: HEIGHT,
    fonts: [loadFont(theme)],
  });

  const slug = slugify(props.version ? `${props.version}-${title}` : title);
  const outFile = `og-${template}-${slug}.png`;
  const outPath = path.resolve(process.cwd(), outFile);

  await sharp(Buffer.from(svg)).png({ quality: 100 }).toFile(outPath);
  console.log(`Generated ${outFile}`);
}

function parseArgs(argv: string[]): {
  template: TemplateName;
  title: string;
  extras: { author?: string; date?: string; version?: string };
  flags: Record<string, string | undefined>;
} {
  const [templateRaw, ...rest] = argv;
  const template = (templateRaw ?? "").toLowerCase() as TemplateName;
  if (!template || !isTemplate(template)) {
    fail(
      "Missing/invalid template. Use: blog | product | changelog | comparison",
    );
  }
  if (rest.length === 0) {
    fail("Missing title. Example: blog \"Hello\" by Ada on 2026-01-27");
  }

  const { flags, positionals } = splitFlags(rest);
  const title = positionals[0];
  if (!title) {
    fail("Missing title. Example: blog \"Hello\" by Ada on 2026-01-27");
  }
  const extras = parseExtras(positionals.slice(1).join(" "));
  return { template, title, extras, flags };
}

function splitFlags(args: string[]): {
  flags: Record<string, string | undefined>;
  positionals: string[];
} {
  const flags: Record<string, string | undefined> = {};
  const positionals: string[] = [];
  for (let i = 0; i < args.length; i += 1) {
    const token = args[i];
    if (!token.startsWith("--")) {
      positionals.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = args[i + 1];
    const value = next && !next.startsWith("--") ? next : undefined;
    flags[key] = value;
    if (value) {
      i += 1;
    }
  }
  return { flags, positionals };
}

function parseExtras(raw: string): { author?: string; date?: string; version?: string } {
  if (!raw) {
    return {};
  }
  const authorMatch = raw.match(/\bby\s+(.+?)(?=\s+\bon\b|\s+\bv\b|$)/i);
  const dateMatch = raw.match(/\bon\s+([A-Za-z0-9,\- ]+)/i);
  const versionMatch = raw.match(/\b(v?\d+\.\d+(?:\.\d+)*)\b/i);
  return {
    author: authorMatch?.[1]?.trim(),
    date: dateMatch?.[1]?.trim(),
    version: versionMatch?.[1]?.trim(),
  };
}

function readTheme(): Theme {
  const defaults: Theme = {
    brandName: "Brand",
    colors: {
      background: "#0b1020",
      foreground: "#ffffff",
      accent: "#4f46e5",
      muted: "#94a3b8",
    },
  };

  const profilePath = path.resolve(process.cwd(), "brand-profile.yaml");
  if (!fs.existsSync(profilePath)) {
    return defaults;
  }

  const content = fs.readFileSync(profilePath, "utf8");
  const brandName = extractName(content) ?? defaults.brandName;
  const fontPath = extractFontPath(content);
  const palette = extractHexes(content);
  if (palette.length === 0) {
    return { ...defaults, brandName, fontPath };
  }

  const background = palette[0];
  const accent = palette[1] ?? defaults.colors.accent;
  const muted = palette[2] ?? defaults.colors.muted;
  const foreground = pickForeground(background);

  return {
    brandName,
    fontPath,
    colors: { background, foreground, accent, muted },
  };
}

function extractName(content: string): string | undefined {
  const match = content.match(/^\s*name:\s*(.+)\s*$/m);
  return match?.[1]?.replace(/^["']|["']$/g, "").trim();
}

function extractHexes(content: string): string[] {
  const matches = content.match(/#(?:[0-9a-fA-F]{3}){1,2}\b/g) ?? [];
  const deduped: string[] = [];
  for (const hex of matches) {
    if (!deduped.includes(hex)) {
      deduped.push(hex);
    }
  }
  return deduped.slice(0, 6);
}

function extractFontPath(content: string): string | undefined {
  const match = content.match(/^\s*fontPath:\s*(.+)\s*$/m);
  return match?.[1]?.replace(/^["']|["']$/g, "").trim();
}

function pickForeground(background: string): string {
  const { r, g, b } = hexToRgb(background);
  const luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
  return luminance > 0.6 ? "#0b1020" : "#ffffff";
}

function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const normalized = hex.replace("#", "");
  const full = normalized.length === 3
    ? normalized.split("").map((c) => c + c).join("")
    : normalized;
  const int = Number.parseInt(full, 16);
  return {
    r: (int >> 16) & 255,
    g: (int >> 8) & 255,
    b: int & 255,
  };
}

function loadFont(theme: Theme): { name: string; data: Buffer; weight: number; style: "normal" } {
  const brandFontPath = theme.fontPath
    ? path.resolve(process.cwd(), theme.fontPath)
    : undefined;
  if (brandFontPath && fs.existsSync(brandFontPath)) {
    return {
      name: "System",
      data: fs.readFileSync(brandFontPath),
      weight: 400,
      style: "normal",
    };
  }
  const candidates = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
  ];
  const fontPath = candidates.find((p) => fs.existsSync(p));
  if (!fontPath) {
    fail("No system font found. Add a font file and update loadFont().");
  }
  return {
    name: "System",
    data: fs.readFileSync(fontPath),
    weight: 400,
    style: "normal",
  };
}

function renderTemplate(template: TemplateName, props: CommonProps): React.ReactElement {
  switch (template) {
    case "blog":
      return React.createElement(BlogCard, props);
    case "product":
      return React.createElement(ProductCard, props);
    case "changelog":
      return React.createElement(ChangelogCard, props);
    case "comparison":
      return renderComparison(props);
    default:
      return exhaustive(template);
  }
}

function renderComparison(props: CommonProps): React.ReactElement {
  const competitor = props.competitor ?? "Competitor";
  const left = props.theme.brandName;
  const right = competitor;
  const { background, foreground, accent, muted } = props.theme.colors;
  const rootStyle: React.CSSProperties = {
    width: WIDTH,
    height: HEIGHT,
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    padding: 64,
    backgroundColor: background,
    color: foreground,
    fontFamily: "System",
  };
  return React.createElement(
    "div",
    { style: rootStyle },
    React.createElement("div", { style: { fontSize: 28, opacity: 0.8 } }, "Comparison"),
    React.createElement(
      "div",
      { style: { fontSize: 72, fontWeight: 700, lineHeight: 1.05 } },
      props.title,
    ),
    React.createElement(
      "div",
      { style: { display: "flex", gap: 24, alignItems: "center" } },
      React.createElement("div", { style: chip(accent, foreground) }, left),
      React.createElement("div", { style: { fontSize: 36, color: muted } }, "vs"),
      React.createElement("div", { style: chip("transparent", foreground, accent) }, right),
    ),
  );
}

function chip(
  backgroundColor: string,
  color: string,
  borderColor?: string,
): React.CSSProperties {
  return {
    padding: "16px 24px",
    borderRadius: 16,
    backgroundColor,
    color,
    border: borderColor ? `2px solid ${borderColor}` : "none",
    fontSize: 28,
    fontWeight: 600,
  };
}

function slugify(input: string): string {
  return input
    .toLowerCase()
    .replace(/['"]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function normalizeFlag(value: string | undefined): string | undefined {
  if (!value) {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function isTemplate(value: string): value is TemplateName {
  return value === "blog" || value === "product" || value === "changelog" || value === "comparison";
}

function exhaustive(_: never): never {
  throw new Error("Unhandled template");
}

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

void main().catch((err) => fail(err instanceof Error ? err.message : String(err)));
