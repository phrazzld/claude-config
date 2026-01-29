import React from "react";

export const metadata = {
  title: "__TITLE__",
  description: "__DESCRIPTION__",
};

const pageData = __PAGE_DATA__;

export default function Page() {
  const title = pageData.h1 || pageData.title || "Best for";
  return (
    <main>
      <header>
        <p>Updated {pageData.updated || "—"}</p>
        <h1>{title}</h1>
        <p>{pageData.description}</p>
      </header>

      <section>
        <h2>
          Best {pageData.category || "tools"} for {pageData.persona?.name || "you"}
        </h2>
        <p>{pageData.persona?.summary}</p>
        <ul>
          {(pageData.persona?.pains || []).map((p: string, i: number) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Top picks</h2>
        <ol>
          {(pageData.picks || []).map((pick: any, i: number) => (
            <li key={pick.name || i}>
              <h3>{pick.name}</h3>
              <p>{pick.summary}</p>
              <ul>
                {(pick.why || []).map((w: string, j: number) => (
                  <li key={j}>{w}</li>
                ))}
              </ul>
              <p>
                <strong>Price:</strong> {pick.price || "—"}
              </p>
            </li>
          ))}
        </ol>
      </section>

      <section>
        <h2>Methodology</h2>
        <ul>
          {(pageData.methodology || []).map((m: string, i: number) => (
            <li key={i}>{m}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
