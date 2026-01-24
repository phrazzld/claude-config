#!/usr/bin/env npx tsx
/**
 * Fetch metrics for MistyStep portfolio dashboard
 *
 * Uses:
 * - Vercel CLI auth token (from ~/Library/Application Support/com.vercel.cli/auth.json)
 * - Vercel Analytics API for traffic
 * - Site health checks via curl
 *
 * Usage:
 *   npx tsx fetch-metrics.ts              # All products, terminal output
 *   npx tsx fetch-metrics.ts --html       # Export to HTML
 *   npx tsx fetch-metrics.ts volume       # Single product
 */

import { execSync } from "child_process";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { parse } from "yaml";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { homedir } from "os";

const __dirname = dirname(fileURLToPath(import.meta.url));

interface Product {
  name: string;
  domain: string;
  description?: string;
  category?: string;
  vercel_project_id?: string;
  stripe_product_id?: string;
  github_repo?: string;
}

interface ProductMetrics {
  name: string;
  domain: string;
  visits: number;
  devices: number;
  bounceRate: number;
  healthy: boolean;
  status: "signal" | "ok" | "warning" | "unknown";
}

interface Config {
  products: Product[];
}

// Get Vercel token from CLI auth file
function getVercelToken(): string | null {
  const authPath = join(
    homedir(),
    "Library/Application Support/com.vercel.cli/auth.json"
  );
  if (!existsSync(authPath)) {
    return null;
  }
  try {
    const auth = JSON.parse(readFileSync(authPath, "utf-8"));
    return auth.token || null;
  } catch {
    return null;
  }
}

// Load products from YAML
function loadProducts(): Product[] {
  const configPath = join(__dirname, "..", "products.yaml");
  const content = readFileSync(configPath, "utf-8");
  const config = parse(content) as Config;
  return config.products;
}

// Fetch Vercel Analytics
async function fetchVercelAnalytics(
  projectId: string,
  token: string
): Promise<{ visits: number; devices: number; bounceRate: number }> {
  if (!projectId || !token) {
    return { visits: 0, devices: 0, bounceRate: 0 };
  }

  try {
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    const from = weekAgo.toISOString().split(".")[0] + "Z";
    const to = now.toISOString().split(".")[0] + "Z";

    const url = `https://vercel.com/api/web-analytics/overview?projectId=${projectId}&from=${from}&to=${to}`;

    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      return { visits: 0, devices: 0, bounceRate: 0 };
    }

    const data = (await res.json()) as {
      total?: number;
      devices?: number;
      bounceRate?: number;
    };

    return {
      visits: data.total ?? 0,
      devices: data.devices ?? 0,
      bounceRate: data.bounceRate ?? 0,
    };
  } catch {
    return { visits: 0, devices: 0, bounceRate: 0 };
  }
}

// Check if site is responding
function checkSiteHealth(domain: string): boolean {
  try {
    const result = execSync(
      `curl -s -o /dev/null -w "%{http_code}" "https://${domain}" 2>/dev/null`,
      { encoding: "utf-8", timeout: 10000 }
    ).trim();
    const code = parseInt(result, 10);
    return code >= 200 && code < 400;
  } catch {
    return false;
  }
}

// Determine status based on metrics
function determineStatus(
  visits: number,
  healthy: boolean
): ProductMetrics["status"] {
  if (!healthy) return "warning";
  if (visits > 100) return "signal"; // Notable traffic
  if (visits > 0) return "ok";
  return "unknown";
}

// Render terminal output
function renderTerminal(metrics: ProductMetrics[]): string {
  const now = new Date();
  const weekOf = now.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });

  let output = `
┌─────────────────────────────────────────────────────────────────────────────────┐
│ MISTYSTEP PORTFOLIO - Week of ${weekOf.padEnd(47)}│
├─────────────────────────────────────────────────────────────────────────────────┤
│ Product              │ Visits │ Devices │ Bounce │ Health │ Status             │
├─────────────────────────────────────────────────────────────────────────────────┤
`;

  let totalVisits = 0;
  let totalDevices = 0;

  for (const m of metrics) {
    totalVisits += m.visits;
    totalDevices += m.devices;

    const name = m.name.padEnd(20).slice(0, 20);
    const visits = m.visits.toString().padStart(6);
    const devices = m.devices.toString().padStart(7);
    const bounce = m.bounceRate > 0 ? `${m.bounceRate}%`.padStart(6) : "    —";
    const health = m.healthy ? "  🟢  " : "  🔴  ";
    const status =
      m.status === "signal"
        ? "⚠️  TRACTION"
        : m.status === "ok"
          ? "🟢 Active"
          : m.status === "warning"
            ? "🟡 Issue"
            : "⚪ No data";

    output += `│ ${name} │${visits} │${devices} │${bounce} │${health}│ ${status.padEnd(18)} │\n`;
  }

  output += `├─────────────────────────────────────────────────────────────────────────────────┤
│ TOTAL                │${totalVisits.toString().padStart(6)} │${totalDevices.toString().padStart(7)} │       │       │                    │
└─────────────────────────────────────────────────────────────────────────────────┘
`;

  // Summary
  const healthy = metrics.filter((m) => m.healthy).length;
  const total = metrics.length;
  const withTraffic = metrics.filter((m) => m.visits > 0).length;

  output += `\n📊 ${totalVisits} total visits across ${withTraffic} active products`;
  output += `\n🏥 ${healthy}/${total} sites healthy\n`;

  // Traction signals
  const signals = metrics.filter((m) => m.status === "signal");
  if (signals.length > 0) {
    output += `\n⚠️  TRACTION SIGNALS:\n`;
    for (const s of signals) {
      output += `   ${s.name}: ${s.visits} visits (${s.devices} devices)\n`;
    }
  }

  // Issues
  const issues = metrics.filter((m) => !m.healthy);
  if (issues.length > 0) {
    output += `\n🔴 Sites with issues:\n`;
    for (const i of issues) {
      output += `   - ${i.name} (${i.domain})\n`;
    }
  }

  return output;
}

// Render HTML output
function renderHTML(metrics: ProductMetrics[]): string {
  const now = new Date();
  const weekOf = now.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  const totalVisits = metrics.reduce((sum, m) => sum + m.visits, 0);
  const healthy = metrics.filter((m) => m.healthy).length;
  const signals = metrics.filter((m) => m.status === "signal");

  return `<!DOCTYPE html>
<html>
<head>
  <title>MistyStep Dashboard - ${weekOf}</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 1100px;
      margin: 40px auto;
      padding: 20px;
      background: #0a0a0a;
      color: #fafafa;
    }
    h1 { margin: 0 0 8px 0; font-weight: 600; }
    .subtitle { color: #888; margin-bottom: 24px; }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .stat {
      background: #1a1a1a;
      padding: 16px 20px;
      border-radius: 8px;
      border: 1px solid #333;
    }
    .stat-value { font-size: 28px; font-weight: 600; }
    .stat-label { color: #888; font-size: 14px; margin-top: 4px; }
    table {
      width: 100%;
      border-collapse: collapse;
      background: #1a1a1a;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid #333;
    }
    th, td { padding: 12px 16px; text-align: left; }
    th { background: #0f0f0f; font-weight: 500; color: #888; font-size: 13px; text-transform: uppercase; }
    tr:not(:last-child) td { border-bottom: 1px solid #222; }
    tr:hover td { background: #222; }
    .health-ok { color: #22c55e; }
    .health-error { color: #ef4444; }
    .visits { font-variant-numeric: tabular-nums; }
    .signal { background: rgba(234, 179, 8, 0.1); }
    a { color: #60a5fa; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 500;
    }
    .badge-signal { background: #854d0e; color: #fef08a; }
    .badge-ok { background: #14532d; color: #86efac; }
    .badge-warning { background: #7f1d1d; color: #fca5a5; }
    .badge-unknown { background: #333; color: #888; }
  </style>
</head>
<body>
  <h1>MistyStep Portfolio</h1>
  <p class="subtitle">Week of ${weekOf}</p>

  <div class="stats">
    <div class="stat">
      <div class="stat-value">${totalVisits.toLocaleString()}</div>
      <div class="stat-label">Total Visits</div>
    </div>
    <div class="stat">
      <div class="stat-value">${healthy}/${metrics.length}</div>
      <div class="stat-label">Sites Healthy</div>
    </div>
    <div class="stat">
      <div class="stat-value">${signals.length}</div>
      <div class="stat-label">Traction Signals</div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Product</th>
        <th>Domain</th>
        <th style="text-align:right">Visits</th>
        <th style="text-align:right">Devices</th>
        <th style="text-align:right">Bounce</th>
        <th>Health</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      ${metrics
        .map(
          (m) => `
        <tr class="${m.status === "signal" ? "signal" : ""}">
          <td><strong>${m.name}</strong></td>
          <td><a href="https://${m.domain}" target="_blank">${m.domain}</a></td>
          <td class="visits" style="text-align:right">${m.visits.toLocaleString()}</td>
          <td class="visits" style="text-align:right">${m.devices.toLocaleString()}</td>
          <td style="text-align:right">${m.bounceRate > 0 ? m.bounceRate + "%" : "—"}</td>
          <td class="${m.healthy ? "health-ok" : "health-error"}">●</td>
          <td><span class="badge badge-${m.status}">${m.status.toUpperCase()}</span></td>
        </tr>
      `
        )
        .join("")}
    </tbody>
  </table>
</body>
</html>`;
}

// Main
async function main() {
  const args = process.argv.slice(2);
  const htmlMode = args.includes("--html");
  const productFilter = args.find((a) => !a.startsWith("--"));

  const token = getVercelToken();
  if (!token) {
    console.error("⚠️  Vercel CLI not authenticated. Run: npx vercel login");
    process.exit(1);
  }

  const products = loadProducts();
  const filtered = productFilter
    ? products.filter((p) =>
        p.name.toLowerCase().includes(productFilter.toLowerCase())
      )
    : products;

  console.log(`Checking ${filtered.length} products...\n`);

  const metrics: ProductMetrics[] = [];

  for (const product of filtered) {
    process.stdout.write(`  ${product.name}...`);

    const [analytics, healthy] = await Promise.all([
      fetchVercelAnalytics(product.vercel_project_id ?? "", token),
      Promise.resolve(checkSiteHealth(product.domain)),
    ]);

    const status = determineStatus(analytics.visits, healthy);

    metrics.push({
      name: product.name,
      domain: product.domain,
      visits: analytics.visits,
      devices: analytics.devices,
      bounceRate: analytics.bounceRate,
      healthy,
      status,
    });

    const indicator = !healthy ? " 🔴" : analytics.visits > 0 ? " ✓" : " ·";
    console.log(indicator);
  }

  console.log("");

  if (htmlMode) {
    const html = renderHTML(metrics);
    const outPath = join(homedir(), "dashboard.html");
    writeFileSync(outPath, html);
    console.log(`Dashboard exported to: ${outPath}`);
    console.log(`Open with: open ${outPath}`);
  } else {
    console.log(renderTerminal(metrics));
  }
}

main().catch(console.error);
