# AGENTS.md — Family Friendly Inc landing site

Single-page static marketing site. No build step, no framework, no package manager.
Files are served exactly as they sit in the repo root.

## Commands

```bash
python3 scripts/check.py      # the only check; CI runs exactly this
python3 -m http.server 8000   # preview at http://localhost:8000
```

## Layout

- `index.html` — the page. This is the whole site.
- `styles.css` — the styles.
- `CNAME` — `familyfriendlyinc.com`. Exactly one line. Deleting it breaks the custom domain.
- `scripts/check.py` — link/asset/a11y checker (stdlib only).
- `.github/workflows/pages.yml` — deploys the repo root to Pages on push to `main`.

## Gotchas

1. **No build step exists.** Do not add a bundler, framework, or `package.json` to solve a
   styling or layout problem. If you add one, `pages.yml` uploads the repo root verbatim and
   will publish your source files instead of a build — the site silently breaks.
2. **`CNAME` must survive every change.** GitHub Pages rewrites the custom-domain setting from
   this file on each deploy. Remove it and the domain 404s until someone re-enters it by hand.
3. **Every local `href`/`src` must resolve from the repo root**, because that is the Pages
   document root. A leading-slash path works in production and in `python3 -m http.server`;
   a `../` path escaping the root does not, and `check.py` will fail it.
4. **Third-party actions are SHA-pinned** with a version comment. Replacing a SHA with a tag
   passes CI and quietly removes the supply-chain guarantee.
5. **The `gate` job in `ci.yml` is the required check.** Renaming it makes every PR wait
   forever on a status that will never report.

## Accessibility — WCAG 2.2 AA

A UI change is any edit to `index.html` or `styles.css`. For every one:

- Use the native element. No ARIA is better than bad ARIA — reach for `<button>`, `<nav>`,
  `<details>` before `role=`.
- Every `<img>` needs `alt`; decorative images get `alt=""`, not a missing attribute.
- Text contrast ≥ 4.5:1 (≥ 3:1 for text ≥ 24px or bold ≥ 19px). Check both light and dark.
- Interactive targets ≥ 24×24 CSS px with a visible focus ring. Never `outline: none` without
  a replacement indicator.
- Headings descend without skipping; exactly one `<h1>`.
- `check.py` catches roughly a third of this at best. A green run is necessary, not sufficient —
  tab through the page before claiming a UI change is done.

## Docs currency

| If you change… | Update… |
|---|---|
| the domain, or `CNAME` | `README.md` (URL + DNS section), `AGENTS.md` layout section |
| `scripts/check.py` behaviour | the Commands section above |
| any workflow file | `AGENTS.md` Gotchas, if the required check or deploy path moves |
| page copy or contact details | nothing — the page is the source of truth |

Skipping a required doc update needs `Docs-not-needed: <reason>` in the PR body, with a real
sentence naming why. "N/A" is not a reason.

## Verification

PRs carry a `### Verified` section naming the commands actually run and where. Do not write
that a check passed unless you watched it pass.
