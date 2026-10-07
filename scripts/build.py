#!/usr/bin/env python3
"""Build a dependency-free report directory and verify every copied PDF."""
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def main():
    reports = json.loads((ROOT / "reports.json").read_text())
    seen = set()
    groups = {}
    for report in reports:
        relative = report["path"]
        if relative in seen or ".." in Path(relative).parts or Path(relative).is_absolute():
            raise ValueError(f"Invalid or repeated report path: {relative}")
        seen.add(relative)
        data = (DOCS / relative).read_bytes()
        if not data.startswith(b"%PDF-"):
            raise ValueError(f"Not a PDF: {relative}")
        if len(data) != report["bytes"] or hashlib.sha256(data).hexdigest() != report["sha256"]:
            raise ValueError(f"PDF differs from its recorded source copy: {relative}")
        groups.setdefault(report["category"], {}).setdefault(report["title"], []).append(report)

    sections = []
    for category, projects in groups.items():
        cards = []
        for title, documents in projects.items():
            first = documents[0]
            links = []
            for document in documents:
                label = "Slides" if "slides" in document["kind"].lower() or "presentation" in document["kind"].lower() else "Report"
                links.append(
                    f'<li><a class="pdf" href="{escape(document["path"])}" '
                    f'aria-label="Read {escape(title)} {label.lower()} (PDF)">{label} <span>PDF</span></a>'
                    f'<span class="file-detail">{document["pages"]} pages / {document["bytes"] / 1_000_000:.2f} MB</span></li>'
                )
            repository = first["source_repository"]
            source_label = "Source (private repository)" if first["id"] == "wine" else "Source repository"
            year = f'<span>{escape(first["year"])}</span>' if first["year"] else ""
            cards.append(
                f'<article><div class="project-meta">{year}<span>{escape(first["kind"].replace(" slides", "").replace(" report", ""))}</span></div>'
                f'<h3>{escape(title)}</h3><p>{escape(first["description"])}</p>'
                f'<p class="authors">{escape(first["authors"])}</p>'
                f'<ul class="documents">{"".join(links)}</ul>'
                f'<a class="source" href="https://github.com/{escape(repository)}">{source_label}</a></article>'
            )
        sections.append(f'<section aria-label="{escape(category)}"><h2>{escape(category)}</h2><div class="projects">{"".join(cards)}</div></section>')

    html = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>Reports | Kat</title>
  <meta name="description" content="Research reports and presentations by Ekaterina Bogush and collaborators, covering machine learning, NLP and data science.">
  <link rel="canonical" href="https://reports.ekat.world/">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <a class="skip" href="#reports">Skip to reports</a>
  <div class="page">
    <header><a class="brand" href="./">ekat.world <span>/ reports</span></a><a href="https://github.com/BshKatrin">GitHub profile</a></header>
    <main id="reports">
      <div class="intro"><h1>Reports &amp; presentations</h1><p>Research and university projects by Ekaterina Bogush and collaborators.</p></div>
      SECTIONS
    </main>
    <footer>PDFs open directly in your browser. Original copies remain in their project repositories.</footer>
  </div>
</body>
</html>
'''.replace("SECTIONS", "\n".join(sections))
    (DOCS / "index.html").write_text(html)
    print(f"Verified {len(reports)} exact PDF copies and built docs/index.html.")


if __name__ == "__main__":
    main()
