import React from "react";

type ProductCardProps = {
  title: string;
  tagline?: string;
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

export function ProductCard({ title, tagline, theme }: ProductCardProps): React.ReactElement {
  const { brandName, colors } = theme;
  return (
    <div
      style={{
        width: WIDTH,
        height: HEIGHT,
        display: "flex",
        padding: 56,
        gap: 40,
        backgroundColor: colors.background,
        color: colors.foreground,
        fontFamily: "System",
      }}
    >
      <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div
            style={{
              width: 44,
              height: 44,
              borderRadius: 12,
              backgroundColor: colors.accent,
            }}
          />
          <div style={{ fontSize: 28, fontWeight: 700 }}>{brandName}</div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ fontSize: 68, fontWeight: 800, lineHeight: 1.04 }}>{title}</div>
          <div style={{ fontSize: 28, color: colors.muted }}>
            {tagline ?? "Ship faster with a crisp product narrative."}
          </div>
        </div>

        <div style={{ fontSize: 22, color: colors.muted }}>Product</div>
      </div>

      <div
        style={{
          width: 520,
          borderRadius: 28,
          padding: 18,
          backgroundColor: "rgba(255,255,255,0.08)",
          border: `2px solid ${colors.accent}`,
          display: "flex",
        }}
      >
        <div
          style={{
            flex: 1,
            borderRadius: 20,
            backgroundColor: "#0f172a",
            border: "1px solid rgba(255,255,255,0.1)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#e5e7eb",
            fontSize: 24,
            fontWeight: 600,
          }}
        >
          Screenshot
        </div>
      </div>
    </div>
  );
}

