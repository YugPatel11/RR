# PROJECT BRIEF: "HALLA BOL: INTO THE PRESSURE"
Cinematic 3D scroll dashboard for the Rajasthan Royals "SupeRR Selector Season 2 – Round 1" submission: the most reliable under-pressure batters and bowlers (IPL + T20I, 2022 to Nov 2026) and who RR should back at the IPL 2027 mini-auction (Goa, 16 Dec 2026).

## Concept (one idea, executed well)
The user scrolls DOWN a procedural 3D Jaipur stepwell (square, concentric stair-rings of pink sandstone). Each group of steps = one real pressure band (4 bands). Deeper = more pressure. Colour = pressure: deep navy (calm) to RR pink to gold (extreme). At the bottom stand 10 pillars (the top 10): height = Pressure Rating, halo ring = 90% confidence band. Recurring Devanagari motif: हल्ला बोल.

## Look
Dark and cinematic. Colours: #070B1E and #0B133A navy, #EA1A85 pink, #D4AF37 gold, warm rose-sandstone. Fonts self-hosted via @fontsource: Fraunces (display), Barlow Condensed (headings/data), JetBrains Mono (numbers), Noto Serif Devanagari (accent). NO white backgrounds, purple gradients, glassmorphism, emoji icons, or generic card grids. Every animation must show data or progress. Respect prefers-reduced-motion.

## Stack (fixed, do not change it)
Vite + vanilla JavaScript (no TypeScript, no React) + three + gsap (ScrollTrigger) + lenis + d3-scale + d3-shape. Charts are SVG. Player info cards are HTML overlays (not textures inside the 3D scene). Procedural geometry only (InstancedMesh). No postprocessing, no audio. Everything free, no API keys, all assets and fonts local.

## Data rules (strict)
- Official rankings, ratings, confidence bands and pressure_validation come from the DATA object in old/index_1.html. Copy them to public/data/players.json. NEVER change those values. If you think one is wrong, log it in PROGRESS.md; do not fix it.
- The official top 10 includes players RR cannot buy: Muqeem, Abrar Ahmed, Shaheen Afridi, Nawaz (Pakistani) and Dinesh Karthik (retired). Show them, flagged as "locked", and add an "Auction-eligible only" toggle.
- Rs 157 Cr is the 2027 TOTAL SALARY CAP (auction purse + incremental performance pay + match fees). It is NOT the auction purse. The 2027 auction purse and RR's retained squad are not confirmed (retention deadline reportedly 17 Nov 2026). The simulator's purse and squad must be EDITABLE inputs labelled "unverified assumption, as of <date>". Do not use a Rs 102 Cr default.
- The 4 pressure groups are bands, not quartiles (they hold about 78.8% / 15.2% / 4.1% / 2.0% of balls). Always call them "pressure bands".
- The old page says 199,208 balls / 843 matches; the raw data pack has about 200,999 ball rows / 867 matches. Document the exclusion rule if you can find it; otherwise state "difference not reconciled". Never hide it.
- External facts (nationality, age, role, price, team status) go in public/data/players_meta.json with source_url and as_of. Set verified:true ONLY if you actually opened that source page. Otherwise "unverified". Never invent. Prices: only a verified base-price slab or last verified IPL sale price, else "Not listed yet".
- A Sources and Methodology section is mandatory (dataset, exclusion rules, every external source, image credits).

## Working rules
- Read PROGRESS.md first. Update it after every task.
- Make small edits. Do not rewrite files that already work.
- After each phase: run `npm run build` and fix errors, run the dev server, and make sure the browser console has no errors.
- Take screenshots at 1440x900 and 390x844, critique them as a ruthless art director (hierarchy, contrast, spacing, anything generic), fix, and check once more.
- If a download is blocked, stop retrying and add it to MANUAL_DOWNLOADS.md (name, URL, save-as filename, folder).
- Do ONLY the current phase, then STOP and report. Do not start the next phase.