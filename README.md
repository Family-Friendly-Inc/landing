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

Push to `main`. `.github/workflows/pages.yml` publishes the repo root to GitHub Pages.

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

See [AGENTS.md](AGENTS.md) — it covers the commands, the invariants, and the accessibility bar.

© Family Friendly Inc. All rights reserved.
