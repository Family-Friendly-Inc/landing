#!/usr/bin/env python3
"""Static-site sanity check: local refs resolve, basic a11y musts hold.

ponytail: stdlib HTMLParser, no deps. Swap for a real a11y scanner (axe) only
if the page grows past a handful of components.
"""
import sys, pathlib
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []


class Check(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.saw_title = False
        self.saw_h1 = False

    def err(self, msg):
        errors.append(f"{self.path.relative_to(ROOT)}:{self.getpos()[0]}: {msg}")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html" and not a.get("lang"):
            self.err("<html> is missing lang")
        if tag == "title":
            self.saw_title = True
        if tag == "h1":
            self.saw_h1 = True
        if tag == "img" and a.get("alt") is None:
            self.err(f"<img src={a.get('src')!r}> is missing alt (use alt=\"\" if decorative)")
        if tag == "a" and (a.get("href") or "").startswith("http") and "noopener" not in (a.get("rel") or "") and a.get("target") == "_blank":
            self.err("target=_blank link is missing rel=noopener")
        for attr in ("href", "src"):
            ref = a.get(attr)
            if not ref or ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//", "#")):
                continue
            target = (self.path.parent / ref.split("#")[0].split("?")[0]).resolve()
            if not target.exists():
                self.err(f"{tag} {attr}={ref!r} does not exist")


pages = sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("**/*.html"))
pages = [p for p in dict.fromkeys(pages) if ".git" not in p.parts]
if not pages:
    errors.append("no HTML pages found")

for page in pages:
    c = Check(page)
    c.feed(page.read_text(encoding="utf-8"))
    if not c.saw_title:
        errors.append(f"{page.relative_to(ROOT)}: missing <title>")
    if not c.saw_h1:
        errors.append(f"{page.relative_to(ROOT)}: missing <h1>")

cname = ROOT / "CNAME"
if cname.exists() and len(cname.read_text().strip().splitlines()) != 1:
    errors.append("CNAME must contain exactly one domain")

for e in errors:
    print(f"error: {e}", file=sys.stderr)
print(f"checked {len(pages)} page(s), {len(errors)} error(s)")
sys.exit(1 if errors else 0)
