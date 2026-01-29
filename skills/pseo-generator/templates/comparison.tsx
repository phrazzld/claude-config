import React from "react";

export const metadata = {
  title: "__TITLE__",
  description: "__DESCRIPTION__",
};

const pageData = __PAGE_DATA__;

function ValueRow({
  label,
  x,
  y,
  note,
}: {
  label: string;
  x?: string;
  y?: string;
  note?: string;
}) {
  return (
    <tr>
      <th>{label}</th>
      <td>{x || "—"}</td>
      <td>{y || "—"}</td>
      <td>{note || ""}</td>
    </tr>
  );
}

export default function Page() {
  const title = pageData.h1 || pageData.title || "Comparison";
  return (
    <main>
      <header>
        <p>Updated {pageData.updated || "—"}</p>
        <h1>{title}</h1>
        <p>{pageData.description}</p>
      </header>

      <section>
        <h2>Overview</h2>
        <div>
          <h3>{pageData.x?.name || "X"}</h3>
          <p>{pageData.x?.summary}</p>
        </div>
        <div>
          <h3>{pageData.y?.name || "Y"}</h3>
          <p>{pageData.y?.summary}</p>
        </div>
      </section>

      <section>
        <h2>Features</h2>
        <table>
          <thead>
            <tr>
              <th>Feature</th>
              <th>{pageData.x?.name || "X"}</th>
              <th>{pageData.y?.name || "Y"}</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {(pageData.features || []).map((f: any, i: number) => (
              <ValueRow
                key={f.name || i}
                label={f.name}
                x={f.x}
                y={f.y}
                note={f.note}
              />
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Pricing</h2>
        <div>
          <h3>{pageData.x?.name || "X"}</h3>
          <p>{pageData.pricing?.x}</p>
        </div>
        <div>
          <h3>{pageData.y?.name || "Y"}</h3>
          <p>{pageData.pricing?.y}</p>
        </div>
        <ul>
          {(pageData.pricing?.notes || []).map((n: string, i: number) => (
            <li key={i}>{n}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Verdict</h2>
        <p>
          <strong>Winner:</strong> {pageData.verdict?.winner || "—"}
        </p>
        <p>{pageData.verdict?.summary}</p>
        <ul>
          {(pageData.verdict?.bestFor || []).map((v: string, i: number) => (
            <li key={i}>{v}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
