import React from "react";

type BlogCardProps = {
  title: string;
  author?: string;
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

export function BlogCard({ title, author, date, theme }: BlogCardProps): React.ReactElement {
  const { brandName, colors } = theme;
  return (
    <div
      style={{
        width: WIDTH,
        height: HEIGHT,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: 64,
        backgroundColor: colors.background,
        color: colors.foreground,
        fontFamily: "System",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontSize: 28, fontWeight: 600 }}>{brandName}</div>
        <div
          style={{
            padding: "10px 16px",
            borderRadius: 999,
            fontSize: 20,
            fontWeight: 600,
            backgroundColor: colors.accent,
            color: colors.foreground,
          }}
        >
          Blog
        </div>
      </div>

      <div style={{ fontSize: 74, fontWeight: 800, lineHeight: 1.05 }}>{title}</div>

      <div style={{ display: "flex", gap: 16, fontSize: 24, color: colors.muted }}>
        <div>{author ? `by ${author}` : "by Team"}</div>
        <div>{date ?? new Date().toISOString().slice(0, 10)}</div>
      </div>
    </div>
  );
}

