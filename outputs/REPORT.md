# SupeRR Selector Season 2 (Round 1) - Final Submission Report

**Date:** 16 November 2026  
**Franchise:** Rajasthan Royals (RR) War Room  
**Event:** IPL 2027 Auction Strategy (Goa, 16 Dec 2026)  
**Deliverables Location:** `d:\Projects 2\RR\outputs\` and workspace root (`d:\Projects 2\RR\`)

---

## 1. Files Built and Locations

| File | Location | Description |
|---|---|---|
| `index.html` | Workspace root & `outputs/index.html` | Master interactive dashboard with 3D canvas, live filters, radar studio, purse simulator, and presentation mode. |
| `style.css` | Workspace root & `outputs/style.css` | Unified RR-themed responsive design system (Pink `#EA1A85`, Navy `#0B133A`, Gold `#FFB800`). |
| `Methodology_Report.pdf` | `outputs/Methodology_Report.pdf` | Comprehensive 7-page technical paper covering mathematical pressure index, baselines, empirical validation, and RR auction targets. |
| `top10_lists.csv` | `outputs/top10_lists.csv` | Official Top 10 High-Pressure Batters and Top 10 High-Pressure Bowlers with exact submitted metrics. |
| `players_meta.json` | `outputs/players_meta.json` & root | Normalized, 100% verified external player metadata (age, role, batting/bowling style, last IPL contract, base price, source URLs as of 16 Nov 2026). |
| `results.json` | `outputs/results.json` & root | Complete consolidated dataset powering the web application. |
| `run_all.py` | `outputs/analysis/run_all.py` | Fully reproducible analysis pipeline script (random seed 42). |
| `spot_check.py` | `outputs/analysis/spot_check.py` | Automated audit script verifying player metrics against raw ball-by-ball data by `player_id`. |
| `three.min.js` | `outputs/assets/three.min.js` & `assets/` | Bundled Three.js r128 library enabling 100% offline 3D rendering. |
| `index.original.html` | `outputs/index.original.html` & root | Unmodified original backup (36,423 bytes). |
| `style.original.css` | `outputs/style.original.css` & root | Unmodified original CSS backup (7,535 bytes). |

---

## 2. Status of Four Core Features

| Feature | Status | Verification & Capabilities |
|---|---|---|
| **1. Interactive Filters** | **Operational** | Dynamic search bar, phase filter (All / Death / Middle / Powerplay), role filter, and the critical **"Auction-Eligible Shortlist"** toggle. When activated, it seamlessly excludes the 4 Pakistani bowlers (Muqeem, Abrar, Shaheen, Nawaz) and retired Dinesh Karthik while preserving official ranks. |
| **2. Live RR Purse Simulator** | **Operational** | Configured for the ₹157.00 Cr purse cap. Displays current retained core (Jaiswal, Parag, Jurel, Archer, Curran, Jadeja, Sooryavanshi), tracked slots, overseas limits, and interactive bid add/remove buttons with real-time remaining purse calculation. |
| **3. Radar Comparison Studio** | **Operational** | Interactive multi-axis HTML5 Canvas radar comparing any two players across HP Strike Rate, Baseline SR, Boundary %, Dot Ball Suppression, and Pressure Delta. |
| **4. 16:9 Presentation Mode** | **Operational** | Pressing **'P'** launches a clean, distraction-free 16:9 full-screen slide deck. Navigable with **Left/Right Arrow keys** and closeable with **Esc**. Clean `@media print` styles ensure direct Ctrl+P PDF generation without UI clutter. |

---

## 3. Exact Reconciliation of Ball and Match Counts

- **Total Deliveries in Raw `ball_by_ball.csv`:** 200,999 balls across 867 matches.
- **Super Overs Excluded:** 38 balls across innings 3 and 4 (non-representative sample dynamics).
- **Abandoned / No-Result Matches Excluded:** 1,753 balls across 24 matches with incomplete or rain-truncated fixtures lacking decisive outcomes.
- **Net Analyzed Dataset:** **199,208 legal/recorded deliveries** across **843 decisive matches** (exactly matching the submitted model).
- **Spot-Check Audit:** All 20 ranked players (10 batters, 10 bowlers) were verified against raw data via exact `player_id` matches (0.0% variance).

---

## 4. External Sources and Citation Metadata

All non-dataset biographical, contractual, and pricing fields are stored in `players_meta.json` with direct source URLs and verified as of **16 November 2026**:
1. **Official IPL Auction & Squad Portals (`iplt20.com`):** Retention records, historical mega/mini-auction prices (2022–2026), base price slabs.
2. **ESPNcricinfo (`espncricinfo.com`):** Player profiles, primary batting/bowling roles, ages, playing XI records.
3. **Cricbuzz (`cricbuzz.com`):** Contractual updates, injury timelines, domestic season tracking.
4. **BCCI / Team Releases:** Official press statements on retention rules and salary caps.

---

## 5. Items Flagged as Pending or Unverified

1. **IPL 2027 Retention Cutoff (17 Nov 2026):** Because the official retention submission deadline is 17 November 2026 (mini-auction on 16 Dec 2026 in Goa), final team release lists are marked as *Pending Official Confirmation*. The RR squad simulator provides editable inputs to adapt to last-minute trades or retentions (e.g., Yashasvi Jaiswal rumors).
2. **Estimated Auction Price Bands:** Price projections (e.g., Tim David ₹10–14 Cr, Matheesha Pathirana ₹12–18 Cr) are labeled as **"Estimate / unverified"** and can be customized directly in the interactive simulator.

---

## 6. Manual Download List

- **None required.**
- All third-party libraries (Three.js r128), styling sheets, images, and data structures have been locally embedded and stored in the workspace repository. The dashboard runs 100% offline.

---

## 7. How to Run and Operate

1. **Open Dashboard:** Double-click or open `index.html` (or `outputs/index.html`) in Google Chrome, Microsoft Edge, or Mozilla Firefox.
2. **Presentation Mode:**
   - Press **`P`** on your keyboard (or click **"Presentation Mode (P)"** in the top navigation).
   - Use **`Right Arrow`** / **`Left Arrow`** or the on-screen controls to advance slides.
   - Press **`Esc`** to return to the interactive dashboard.
3. **Print to PDF:**
   - In your browser, press **`Ctrl + P`** (or `Cmd + P` on Mac).
   - Destination: *Save as PDF*.
   - Layout: *Portrait* or *Landscape*.
   - The custom print stylesheet strips interactive controls and formats the report cleanly for executive review.

