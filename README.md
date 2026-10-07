# Reports

Public copies of research reports and presentations by Ekaterina Bogush and collaborators.

The library is published at **https://reports.ekat.world/** using GitHub Pages.

Original reports remain in their project repositories. The hosted PDFs are exact copies; `reports.json` records provenance, file sizes, page counts and SHA-256 checksums. Coauthors are credited on the index and inside each document. No new document license is implied by publication here.

## Publishing

GitHub Pages publishes the `docs/` directory on the `main` branch. `docs/.nojekyll` enables direct static publishing, and `docs/CNAME` retains the custom domain.

After adding or replacing a PDF, update its entry in `reports.json`, then run:

```sh
python3 scripts/build.py
```

Commit the updated PDF, metadata and generated index to `main`; GitHub Pages redeploys automatically. Preserve existing URLs when replacing an edition. Add a distinct filename if both editions need to remain available.

## DNS

At Namecheap, the `reports` host has a CNAME to `bshkatrin.github.io` (without a repository path). Domain registration, nameservers and existing website records remain unchanged. GitHub Pages must have `reports.ekat.world` configured as its custom domain, with HTTPS enforced once its certificate is issued.

## Local preview

```sh
python3 -m http.server 8765 --directory docs
```

Then open http://localhost:8765/.
