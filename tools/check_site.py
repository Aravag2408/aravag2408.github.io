"""Static checks for the portfolio site. Exit code 0 means every check passed."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {"docs", "screenshots-raw", ".superpowers", "shots", "node_modules", ".git"}
EXCLUDE_FILES = {"tools/components.html"}
MAX_IMG_BYTES = 250 * 1024
IMG_SIZE_EXEMPT = {"arava.jpg", "og.png"}
REQUIRED_SECTIONS = {
    "work/sugarbuddy.html",
    "work/achvalens.html",
    "work/values-under-pressure.html",
    "work/mercury.html",
    "work/sugarbuddy-and-beyond.html",
}
SECTION_IDS = ["users", "decisions", "under-the-hood", "results", "next"]
REDIRECT_PAGE = "work/state-not-trait.html"
REDIRECT_TARGET = "values-under-pressure.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.imgs_without_alt, self.metas = [], set(), 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "img" and not (a.get("alt") or "").strip():
            self.imgs_without_alt += 1
        if tag == "meta":
            self.metas.append(a)


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.split("/")[0] in EXCLUDE_DIRS or rel in EXCLUDE_FILES:
            continue
        yield rel, p


def check():
    failures = []
    for rel, path in pages():
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for ref in parser.refs:
            u = urlparse(ref)
            if u.scheme or ref.startswith(("#", "mailto:", "//")):
                continue
            target = (path.parent / u.path).resolve()
            if not target.exists():
                failures.append(f"{rel}: broken link {ref}")
        if parser.imgs_without_alt:
            failures.append(f"{rel}: {parser.imgs_without_alt} <img> without alt")
        if rel in REQUIRED_SECTIONS:
            missing = [i for i in SECTION_IDS if i not in parser.ids]
            if missing:
                failures.append(f"{rel}: missing section ids {missing}")
        if rel == REDIRECT_PAGE:
            ok = any(m.get("http-equiv", "").lower() == "refresh" and REDIRECT_TARGET in m.get("content", "")
                     for m in parser.metas)
            if not ok:
                failures.append(f"{rel}: no refresh redirect to {REDIRECT_TARGET}")
    for rel in REQUIRED_SECTIONS | {REDIRECT_PAGE}:
        if not (ROOT / rel).exists():
            failures.append(f"{rel}: page missing")
    for img in (ROOT / "assets" / "img").iterdir():
        if img.name not in IMG_SIZE_EXEMPT and img.stat().st_size > MAX_IMG_BYTES:
            failures.append(f"assets/img/{img.name}: {img.stat().st_size // 1024} KB > 250 KB")
    return failures


if __name__ == "__main__":
    fails = check()
    for f in fails:
        print("FAIL", f)
    print(f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)
