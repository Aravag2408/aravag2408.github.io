"""Serve the site locally, screenshot every page at 375 and 1440 wide, and fail on horizontal overflow.

Usage: python tools/shoot.py [page.html ...]   (default: every page)
"""
import functools
import http.server
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from check_site import ROOT, pages  # noqa: E402

PORT = 8765
SIZES = [(375, 812), (1440, 900)]


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main(selected):
    out = ROOT / "shots"
    out.mkdir(exist_ok=True)
    srv = serve()
    overflow = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for rel, _ in pages():
            if selected and rel not in selected:
                continue
            for w, h in SIZES:
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto(f"http://127.0.0.1:{PORT}/{rel}", wait_until="networkidle")
                page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
                page.wait_for_load_state("networkidle")
                sw, cw = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                if sw > cw:
                    overflow.append(f"{rel} @ {w}: scrollWidth {sw} > {cw}")
                page.screenshot(path=str(out / f"{rel.replace('/', '__')[:-5]}-{w}.png"), full_page=True)
                page.close()
        browser.close()
    srv.shutdown()
    for o in overflow:
        print("OVERFLOW", o)
    print(f"screenshots in {out}; {len(overflow)} overflow(s)")
    return 1 if overflow else 0


if __name__ == "__main__":
    sys.exit(main(set(sys.argv[1:])))
