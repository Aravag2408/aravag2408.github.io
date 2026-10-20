# Portfolio redesign: projects as products

Date: 2026-10-20 · Site: https://aravag2408.github.io (plain HTML + CSS, GitHub Pages)

## Why

Arava is a Technion IE&M '26 graduate looking for junior **Product** and **Data Analyst** roles in
Tel Aviv fintech / hi-tech (consulting is a secondary track, not the site's audience). The content
on the site today is strong (real numbers, live apps), but:

- the positioning targets "advisory, business analysis, consulting and strategy", not product/data;
- projects read as course case studies (narrative), not as products with users, decisions and metrics;
- project visuals are weak: low-res Hebrew screenshots, placeholder-looking bar blocks, an unreadable heatmap;
- skills (RAG, agents, evals, full stack, shipping, statistics) are buried inside pages.

**Success:** a recruiter who spends 30 seconds remembers: *she's technical and builds things herself,
and she takes a product from the real problem all the way to something live.*

## Goals

1. New homepage positioning, built around the agreed headline:
   **"Technical enough to build it. Product-minded enough to know what to build."**
   with a small line under it: *Product · Data · AI*. The "Open to roles" line names product and data analyst roles first.
2. A **"What I build"** skills section, each skill linked to the project that proves it.
3. Every major project page rebuilt as a **product page** (structure below).
4. New, consistent visuals across all project cards and pages.
5. New project order, biggest to smallest.

## Non-goals

- No framework, build step or JS library: stay plain HTML + the existing `assets/style.css`.
- No change to the visual identity (Plus Jakarta Sans, blue `#2f5bff`, ink borders with hard shadows).
- No new projects and no invented numbers. Every figure must come from the project folders or the current site.
- The learning roadmap is a separate, later piece of work (not part of this redesign).

## Anti-goals (failure even if it "works")

- Looking like a template or a generic AI portfolio.
- Overclaiming: team work presented as solo work, or a course project presented as a company product.
  Keep the existing honest role notes (e.g. "417 of 532 commits", "data collection was done by the research team").
- Jargon walls: a product manager must be able to read every page; tech detail lives in its own section.

## Project order

**Featured (big → small)**
1. SugarBuddy
2. AchvaLens
3. **Values Under Pressure** (renamed from "State, Not Trait"; rename the file to `work/values-under-pressure.html` and update all links)
4. Mercury
5. SugarBuddy and Beyond

**Small projects:** Fair city budgets, Warsaw 2023 (first), SugarBuddy Agent, Between the Lines, Does standardizing pay off?

## Product page structure (each featured project)

1. **Hero:** product name, one-sentence value proposition, live link, a strong product visual.
2. **Facts strip:** role · team · when · stack (keep the existing side box, tighten it).
3. **Who it's for & the pain:** the user and the moment the problem hurts.
4. **Product decisions & trade-offs:** 2–4 decisions, each with what was chosen, what was given up, and why.
5. **Under the hood:** an architecture diagram plus the technical highlights (guardrails, tests, deploy, eval method).
6. **Results:** the metrics as stat tiles, plus at least one real chart where data exists.
7. **What I'd measure next:** the success metric and how it would be tested (A/B, pilot, etc.). This shows product and analytics thinking.

## Visual system

- **Product shots:** real screenshots inside CSS-only device frames (phone frame for SugarBuddy, browser
  frame for web apps), at 2× resolution, compressed (WebP or JPG ≤ ~250 KB each).
- **Architecture diagrams:** inline SVG in the site's style (ink strokes, blue accents), one per featured project.
- **Charts:** inline SVG redrawn from the real numbers, replacing the bar blocks. Examples:
  - AchvaLens: before/after accuracy and F1.
  - Mercury: the leak funnel 20 → 18 → 6 of 20.
  - Values Under Pressure: LLM judge κ vs. the human-expert ceiling (0.700 vs 0.707; 0.569 vs 0.555).
  - SugarBuddy and Beyond: the 10 datasets, of which 5 passed curation.
- **Work cards:** each card uses that project's hero visual, cropped consistently (same aspect ratio).

## "What I build" (homepage)

| Skill | Proof |
|---|---|
| AI agents: bounded ReAct agent, guardrails, prompt-injection tests | SugarBuddy, SugarBuddy Agent |
| RAG: Pinecone retrieval with keyword fallback; auditing a leaking RAG | SugarBuddy Agent, Mercury |
| LLM evaluation: LLM-as-a-judge validated against experts, DSPy prompt optimization, benchmark building | Values Under Pressure, AchvaLens, SugarBuddy and Beyond |
| Full-stack products: FastAPI, React Native (Expo), MongoDB, WebSockets | SugarBuddy |
| Shipping: Docker, CI/CD with auto-rollback, Azure, ~735 tests | SugarBuddy, AchvaLens |
| Data & statistics: hypothesis tests, clustering, mixed models, simulation | Values Under Pressure, Warsaw budgets, Standardization sim |

## Sources (read-only)

- SugarBuddy: `OneDrive - Technion/school/Last/shani's sugerbuddy/shani-s_sugar_buddy`
- AchvaLens: `.../Last/AchvaLens/achvalens`
- Values Under Pressure: `.../Last/DemocracyGameProject/our_game` (figures, notebooks, `docs/llm_judge_methodology.md`)
- Mercury: `.../Last/Data ethics/mercury-audit`
- SugarBuddy Agent: `.../Last/Modern AI Agents/SugerBuddy_Agent`
- SugarBuddy and Beyond: `~/nlp_project`

Private code stays private: describe it, never copy source files into the public repo.

## Screenshots Arava provides

Taken by Arava (they need her login or demo accounts):
- **SugarBuddy** (phone size, around 390×844; demo family, no real data): event screen, check-in in progress,
  AI explanation, parent summary with recommendation, patterns, forum or family view.
- **Mercury** (desktop): user A's chat, and user B's reply showing A's leaked details, side by side.
- **Between the Lines** (desktop): coaching board and team view.

The builder captures the public apps itself: AchvaLens (scanner with highlights, report, dashboard)
and SugarBuddy Agent (GUI with the module inspector).

## Left to the builder

Exact copy wording (within the facts), card layout details, diagram layout, image cropping and compression,
and mobile layout (must work at 375px with no horizontal scroll).

## Decided with Arava

- The homepage photo stays (`assets/img/arava.jpg`).
- The "Why I do this" section stays, shortened.
