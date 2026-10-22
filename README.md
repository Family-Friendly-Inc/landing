# Family Friendly Inc — landing site

The single-page marketing site for Family Friendly Inc, served by GitHub Pages at
**https://familyfriendlyinc.com**.

## Quickstart

```bash
git clone https://github.com/Family-Friendly-Inc/landing.git
cd landing
python3 -m http.server 8000   # http://localhost:8000
python3 scripts/check.py      # link, asset, and basic a11y check
```

No build step, no dependencies. Edit `index.html` and `styles.css` and reload.

## Deploying

Push to `main`. `.github/workflows/pages.yml` copies an explicit allowlist of paths into `_site/`
and publishes that. A new top-level page directory (e.g. `games/`) must be added to the `cp` line
or it will not deploy (top-level files like `robots.txt` and `sitemap.xml` too, and add new indexable pages to `sitemap.xml`); repo-only files (README, scripts, workflows) never reach the site. Dot-directories such as `.well-known/` also need the `include-hidden-files: true` input on the upload step, which `pages.yml` sets.

### Cloudflare

The site is served by Cloudflare Workers static assets; GitHub Pages still deploys as a rollback until it is retired. `wrangler.jsonc` serves the same `_site/`
allowlist; `worker.js` handles only `/games/nogglets/daily/<N>` (fills `games/nogglets/daily/index.html`,
404 for non-numeric N or N < 1). `_headers` sets response headers, including `application/json` for
`/.well-known/apple-app-site-association`. `.github/workflows/cloudflare.yml` deploys it on every push to `main` (also runnable by hand;
needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets) and copies the same allowlist plus `_headers`.
No `package.json`: CI runs a pinned `npx wrangler`.

## DNS

`CNAME` pins the custom domain to `familyfriendlyinc.com`. The apex domain needs these four
A records at the DNS provider, plus a `www` CNAME to `family-friendly-inc.github.io`:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

## Contributing

Run `python3 scripts/check.py` before pushing. Keep `CNAME` intact, keep third-party actions
SHA-pinned, and meet WCAG 2.2 AA on every page.

© Family Friendly Inc. All rights reserved.
