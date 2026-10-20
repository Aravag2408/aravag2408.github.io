# Portfolio Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the site for junior Product / Data Analyst roles and rebuild every featured project as a product page with strong visuals.

**Architecture:** The site stays plain static HTML and one stylesheet (`assets/style.css`). Shared building blocks are added as CSS classes, not JS: device frames, stat tiles, decision cards, a skills grid, and inline-SVG charts and diagrams. A Python checker (`tools/check_site.py`) is the test suite. It catches broken links and images, oversized images and missing required sections. Playwright screenshots at 375px and 1440px are the visual check.

**Tech Stack:** HTML, CSS, inline SVG · Python 3.13 with Pillow 12 (image optimizing) and Playwright (checks) · GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-20-portfolio-redesign-design.md`

## Global Constraints

- Plain HTML + `assets/style.css` only; no framework, build step or JS library.
- Keep the identity: Plus Jakarta Sans, `--blue:#2f5bff`, ink borders with hard shadows.
- Headline, verbatim: **"Technical enough to build it. Product-minded enough to know what to build."** with *Product · Data · AI* under it.
- No invented numbers. Every figure comes from the project folders (spec → Sources) or the current site. Keep honest role notes (e.g. "417 of 532 commits"; Values Under Pressure: data collection by the research team).
- Never copy private source code into this public repo.
- Published images: WebP, ≤ 250 KB each, stored in `assets/img/`. Raw screenshots stay in git-ignored `screenshots-raw/`.
- Every page works at 375px wide with no horizontal scroll.
- Featured order: SugarBuddy, AchvaLens, Values Under Pressure, Mercury, SugarBuddy and Beyond. Small projects order: Warsaw budgets, SugarBuddy Agent, Between the Lines, Standardization sim.
- The homepage photo `assets/img/arava.jpg` stays.

## Review Focus

1. **Old link `work/state-not-trait.html`**, already shared on the CV/LinkedIn: it must still land on the renamed page (Task 6 adds a redirect stub and a check).
2. **Long words and stat tiles at 375px** (e.g. "63.6% → 69.8%", stack lists) overflowing horizontally: Task 1's Playwright check asserts `scrollWidth <= clientWidth` on every page.
3. **Inline SVG charts unreadable on mobile**: charts use `viewBox` + `width:100%`, and labels stay ≥ 11px at 375px (Task 2 CSS; checked visually in Task 9).
4. **Hebrew screenshots inside English pages**: they need English captions and `alt` text; the checker fails on any `<img>` without a non-empty `alt` (Task 1).
5. **Live apps that sleep (Render)**: keep the existing "may take a few seconds to wake up" note next to every live link that has it today (Tasks 5–8 copy steps).

---

### Task 1: Checker, preview server and image optimizer

**Files:**
- Create: `tools/check_site.py`, `tools/optimize_images.py`, `tools/shoot.py`, `.claude/launch.json`
- Modify: `.gitignore` (add `tools/__pycache__/`, `shots/`)

**Interfaces:**
- Produces: `python tools/check_site.py` → exit 0 / prints failures. `python tools/optimize_images.py <src> <dest.webp> [--width N]`. `python tools/shoot.py` → writes `shots/<page>-<375|1440>.png` and fails if any page scrolls horizontally.

- [ ] **Step 1: Write `check_site.py`** with these checks over every `*.html` (excluding `docs/`, `screenshots-raw/`):
  - every local `href`/`src` resolves to an existing file;
  - every `<img>` has a non-empty `alt`;
  - every file under `assets/img/` is ≤ 250 KB except `arava.jpg` and `og.png`;
  - `REQUIRED_SECTIONS = {"work/sugarbuddy.html", "work/achvalens.html", "work/values-under-pressure.html", "work/mercury.html", "work/sugarbuddy-and-beyond.html"}`, and each must contain elements with ids `users`, `decisions`, `under-the-hood`, `results`, `next`;
  - `work/state-not-trait.html` must contain `http-equiv="refresh"` pointing to `values-under-pressure.html`.
- [ ] **Step 2: Run it** with `python tools/check_site.py`. Expected: FAIL on the missing section ids and the missing redirect, which proves the checker works.
- [ ] **Step 3: Write `optimize_images.py`** with Pillow: resize to `--width` (default 1600), save as WebP at quality 80, and lower the quality in steps of 5 until the file is ≤ 250 KB.
- [ ] **Step 4: Write `shoot.py`** with Playwright (chromium): serve the repo on port 8765 with `http.server`, load each page at 375×812 and 1440×900, take full-page screenshots, and assert `document.documentElement.scrollWidth <= clientWidth`.
- [ ] **Step 5: Add `.claude/launch.json`**, config `site`: `python -m http.server 8765`, port 8765, for previewing in the browser pane.
- [ ] **Step 6: Run `python tools/shoot.py`** on the current site. Expected: screenshots are written. Record any overflow it reports as baseline.
- [ ] **Step 7: Commit:** `chore: add site checker, image optimizer and screenshot tool`

### Task 2: Shared components in `assets/style.css`

**Files:** Modify `assets/style.css` (append a `/* Product pages */` block and a mobile block)

**Interfaces:**
- Produces these classes for Tasks 3–8:
  - `.frame-phone` (rounded bezel, notch, child `img` fills it)
  - `.frame-browser` (top bar with three dots, child `img`)
  - `.stats` > `.stat` > `b` (big number) + `span` (label)
  - `.decisions` > `.decision` > `h3`, `p.chose`, `p.gave-up`, `p.why`
  - `.skills` > `a.skill` > `h3`, `p`, `span.proof`
  - `.chart` (wrapper for inline SVG, `svg{width:100%;height:auto}`)
  - `.diagram` (same, for architecture)
  - `.pp-section` (product-page section: label column + content, like `.why .wrap`)
  - `.card-visual` (fixed 16:10 crop for work cards, `object-fit:cover`)
- [ ] **Step 1: Build a scratch file `tools/components.html`** that uses every class once (not linked from the site), and add it to the checker's exclude list.
- [ ] **Step 2: Implement the classes** in the existing style: 2px ink borders, `box-shadow:6px 6px 0 var(--ink)`, blue accents, no rounded corners except the phone frame. Charts use the CSS variables for color. At `max-width:860px` everything stacks to one column.
- [ ] **Step 3: Verify** by opening `tools/components.html` through the `site` preview at 375 and 1440. Expected: nothing overflows and everything is readable.
- [ ] **Step 4: Commit:** `feat(css): shared product-page components`

### Task 3: Homepage

**Files:** Modify `index.html`, `assets/style.css` (hero tweaks only)

**Interfaces:** Consumes `.skills` and `.skill` from Task 2.

- [ ] **Step 1: Hero copy.** Eyebrow stays. `h1` becomes the headline (keep "Hi, I'm Arava." as a smaller line above it, or fold it into the eyebrow; builder's call). Under it: *Product · Data · AI*. Lede: one sentence that she builds things herself and takes them from the real problem to live. The roles line names product and data analyst roles first, then consulting.
- [ ] **Step 2: Hero tiles.** Keep the three tiles, rewritten to point at proof: "End-to-end ownership" → SugarBuddy, "AI that's measured" → Values Under Pressure, "Bridging business and tech" → AchvaLens.
- [ ] **Step 3: "What I build" section** goes after the hero and uses the six rows of the spec's skills table. Each `a.skill` links to its first proof project.
- [ ] **Step 4: Shorten "Why I do this"** to at most 2 sentences, keeping its meaning.
- [ ] **Step 5: Update `<meta>` description and `og:description`** to the new headline.
- [ ] **Step 6: Run** `python tools/check_site.py` (the homepage-related checks should pass) and `python tools/shoot.py`.
- [ ] **Step 7: Commit:** `feat(home): product/data positioning and What I build`

### Task 4: Work page

**Files:** Modify `work.html`; create images in `assets/img/` with `optimize_images.py`

- [ ] **Step 1: Reorder** to the featured and small orders in Global Constraints. Rename the State, Not Trait card to **Values Under Pressure** and link it to `work/values-under-pressure.html`.
- [ ] **Step 2: Card visuals.** Every featured card uses `.card-visual`:
  - SugarBuddy: `sb-0-login.webp` cropped in a browser frame
  - AchvaLens: a fresh capture (Task 6)
  - Values Under Pressure: its κ chart (Task 7)
  - Mercury: `mercury-0-home.webp` in a browser frame
  - Beyond: its datasets chart (Task 8)
  Small cards: Between the Lines → `btl-1-board.webp`, Warsaw → existing `pb-fairness.png` (re-optimized).
- [ ] **Step 3: Rewrite each card's blurb** as product-first: who it's for · what it does · one metric. Keep it to at most 3 lines at 1440px.
- [ ] **Step 4: Run** the checker and the screenshots. Expected: no broken links or images.
- [ ] **Step 5: Commit:** `feat(work): new order, product cards and visuals`

### Task 5: SugarBuddy product page

**Files:** Modify `work/sugarbuddy.html`. Source: `shani-s_sugar_buddy/` (README, docs/, tests/, ops/).

- [ ] **Step 1: Read the sources** for 2–4 real product decisions with trade-offs (candidates: one adaptive follow-up question rather than a long chat; no insulin dosing ever; life-threatening events always reach the parent; showing nothing instead of a wrong answer; moving to the $0 stack). Use only what the code and docs support.
- [ ] **Step 2: Restructure** to the spec's 7 parts with ids `users`, `decisions`, `under-the-hood`, `results`, `next`. Hero visual: `sb-0-login.webp` in a browser frame. Keep the existing screens (`sb-*.jpg`) in phone frames with English captions until Arava sends new ones.
- [ ] **Step 3: Under the hood:** redraw the architecture as inline SVG (sensor → background service → backend → app; DB / AI model / notifications). Keep the guardrails, tests, rollback and frozen-app bug points, plus the Azure → $0 comparison.
- [ ] **Step 4: Results:** stat tiles for 417/532 commits, ~735 tests and $0/month.
- [ ] **Step 5: What I'd measure next:** the north-star metric (share of glucose events that end in a completed check-in plus a parent response) and a 1-month pilot with a few families. Present it as her plan, not as a result.
- [ ] **Step 6: Checker + screenshots, then commit:** `feat(sugarbuddy): product page`

### Task 6: AchvaLens product page

**Files:** Modify `work/achvalens.html`. Source: `achvalens/` (README, research/, docs/, benchmark_model_accuracy.py).

- [ ] **Step 1: Capture the public live app** with Playwright at 1440px: the scanner with highlighted text (use a short neutral sample text), the report, and the reviewer dashboard if it is reachable without login. Optimize to `assets/img/al-*.webp`.
- [ ] **Step 2: Restructure** to the 7 parts. Decisions: splitting the task into two stages, the automated optimizer (DSPy) rather than hand-written prompts, the reviewer feedback loop. Add more only if the sources support them.
- [ ] **Step 3: Results:** a before/after SVG chart for accuracy (63.6% → 69.8%) and F1 for harmful terms (0.52 → 0.67), plus a stat tile for 81% on "needs attention or not" and a note that there were 162 test terms.
- [ ] **Step 4: Next:** clean up the 249 inconsistent root labels, then measure reviewer time saved per document.
- [ ] **Step 5: Checker + screenshots, then commit:** `feat(achvalens): product page`

### Task 7: Values Under Pressure page (rename)

**Files:** Create `work/values-under-pressure.html`; replace `work/state-not-trait.html` with a redirect stub (`<meta http-equiv="refresh" content="0; url=values-under-pressure.html">` plus a link). Update every link to the old page. Source: `DemocracyGameProject/our_game/` (README, docs/llm_judge_methodology.md, notebooks, figures).

- [ ] **Step 1: Write the page** in the 7 parts, framed as an analytics product: "Does what people say match what they do?"
  - Users: the research team and educators.
  - Decisions: the LLM judge rather than manual coding; validation against two experts; the anti-overfitting split; prompt variants.
  - Role note: Arava did the analysis and modeling; the research team collected the data.
- [ ] **Step 2: Charts (inline SVG):**
  - κ of the best judge vs. the human ceiling (justice 0.700 vs 0.707; argument quality 0.569 vs 0.555)
  - findings as stat tiles: 0/42 stable; r=0.19 across worlds; 28.7% click/rationale agreement; r≈0.00 say vs do; −0.54 shift under pressure (p<0.001)
- [ ] **Step 3: Next:** what she would test next, taken from the README/notebooks (e.g. the LLM-player vs. human comparison).
- [ ] **Step 4: Run the checker.** Expected: the redirect check passes and no link points to the old page except the stub.
- [ ] **Step 5: Commit:** `feat(values-under-pressure): renamed product page with redirect`

### Task 8: Mercury and SugarBuddy and Beyond pages

**Files:** Modify `work/mercury.html` and `work/sugarbuddy-and-beyond.html`. Sources: `mercury-audit/` and `~/nlp_project/`.

- [ ] **Step 1: Mercury in the 7 parts.**
  - Hero: `mercury-0-home.webp` in a browser frame.
  - Under the hood: an SVG of the static RAG plus the shared live memory merging into the search, with the missing user filter marked.
  - Results: an SVG funnel 20 → 18 → 6 of 20.
  - Decisions: why audit through the normal UI only; the fix (per-user filter) and its GDPR mapping.
- [ ] **Step 2: SugarBuddy and Beyond in the 7 parts.**
  - Results: an SVG of 10 datasets (5 passed curation), plus stat tiles for the 94-cause taxonomy and 145/145 citations checked.
  - Keep "code and paper are private".
- [ ] **Step 3: Checker + screenshots, then commit:** `feat: Mercury and Beyond product pages`

### Task 9: Final verification

- [ ] **Step 1: Run** `python tools/check_site.py`. Expected: exit 0, no failures.
- [ ] **Step 2: Run** `python tools/shoot.py`. Expected: no overflow on any page at 375 or 1440. Look at every screenshot for unreadable chart labels or broken frames.
- [ ] **Step 3: Grep** for `State, Not Trait` and `consulting and strategy` in the HTML. Expected: no hits except the redirect stub.
- [ ] **Step 4: Show Arava** the 1440 and 375 screenshots of the homepage, the work page and one product page. **Push only after she approves**, since the site is public.
