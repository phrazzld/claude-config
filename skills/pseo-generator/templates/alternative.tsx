import React from "react";

export const metadata = {
  title: "__TITLE__",
  description: "__DESCRIPTION__",
};

const pageData = __PAGE_DATA__;

export default function Page() {
  const title = pageData.h1 || pageData.title || "Alternatives";
  return (
    <main>
      <header>
        <p>Updated {pageData.updated || "—"}</p>
        <h1>{title}</h1>
        <p>{pageData.description}</p>
      </header>

      <section>
        <h2>Why look beyond {pageData.product?.name || "this product"}?</h2>
        <p>{pageData.product?.summary}</p>
      </section>

      <section>
        <h2>Top alternatives</h2>
        <ol>
          {(pageData.alternatives || []).map((alt: any, i: number) => (
            <li key={alt.name || i}>
              <h3>{alt.name}</h3>
              <p>{alt.summary}</p>
              <p>
                <strong>Best for:</strong> {alt.bestFor || "—"}
              </p>
              <p>
                <strong>Pricing:</strong> {alt.pricing || "—"}
              </p>
            </li>
          ))}
        </ol>
      </section>

      <section>
        <h2>Next step</h2>
        <a href={pageData.cta?.href || "#"}>{pageData.cta?.label || "Learn more"}</a>
      </section>
    </main>
  );
}
