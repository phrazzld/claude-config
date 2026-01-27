import React from "react";

type ChangelogCardProps = {
  title: string;
  version?: string;
  date?: string;
  theme: {
    brandName: string;
    colors: {
      background: string;
      foreground: string;
      accent: string;
      muted: string;
    };
  };
};

const WIDTH = 1200;
const HEIGHT = 630;

export function ChangelogCard({
  title,
  version,
  date,
  theme,
}: ChangelogCardProps): React.ReactElement {
  const { brandName, colors } = theme;
  const v = version ?? "v1.0.0";
  const d = date ?? new Date().toISOString().slice(0, 10);
  return (
    <div
      style={{
        width: WIDTH,
        height: HEIGHT,
        display: "flex",
        flexDirection: "column",
        padding: 60,
        gap: 28,
        backgroundColor: colors.background,
        color: colors.foreground,
        fontFamily: "System",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontSize: 28, fontWeight: 700 }}>{brandName} Changelog</div>
        <div style={{ fontSize: 22, color: colors.muted }}>{d}</div>
      </div>

      <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
        <div
          style={{
            padding: "8px 14px",
            borderRadius: 14,
            fontSize: 22,
            fontWeight: 700,
            backgroundColor: colors.accent,
            color: colors.foreground,
          }}
        >
          {v}
        </div>
        <div style={{ fontSize: 54, fontWeight: 800, lineHeight: 1.05 }}>{title}</div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 14, marginTop: 10 }}>
        <div style={row(colors.accent, colors.foreground)}>Faster onboarding flow</div>
        <div style={row(colors.accent, colors.foreground)}>Improved search relevance</div>
        <div style={row(colors.accent, colors.foreground)}>Cleaner billing controls</div>
      </div>
    </div>
  );
}

function row(accent: string, foreground: string): React.CSSProperties {
  return {
    padding: "14px 18px",
    borderRadius: 16,
    fontSize: 26,
    fontWeight: 600,
    color: foreground,
    backgroundColor: "rgba(255,255,255,0.06)",
    border: `1px solid ${accent}`,
  };
}

