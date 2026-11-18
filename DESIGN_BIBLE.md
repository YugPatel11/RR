# DESIGN BIBLE: HALLA BOL — INTO THE PRESSURE
**Editorial Philosophy & System Specification**  
*Art Direction Benchmark: FT Visual Journalism, The Pudding, Bloomberg Businessweek, Pentagram*

---

## 1. Visual Hierarchy & Palette
- **Aesthetic Direction:** Austere investigative data journalism with exactly ONE dramatic, photo-realistic 3D scene (The Crucible Chamber) and calm, editorial broadsheet sections elsewhere.
- **Strict Color Architecture (70 Navy / 20 Bone / 8 Pink / 2 Gold):**
  - `--color-bg-deep`: `#070B1E` (Dominant page canvas)
  - `--color-bg-surface`: `#0B133A` (Structured container fills)
  - `--color-bone`: `#E6E4DD` (Primary high-contrast editorial text)
  - `--color-bone-muted`: `rgba(230, 228, 221, 0.7)` (Secondary supporting prose)
  - `--color-pink`: `#EA1A85` (Franchise accent, actionable focus, active states)
  - `--color-gold`: `#D4AF37` (**Strictly isolated** to the composite Bayesian Pressure Rating score numeral; banned from borders, lines, tags, charts, and headings)
  - `--color-paper`: `#F2EFE9` with ink `#070B1E` (Approved tonal break for Sources & Methodology)

---

## 2. Typography & Spatial Grid
- **Display Typography:** `Fraunces` (700 bold, tight editorial tracking) for thematic findings and section numbers.
- **Categorical & Metadata:** `Barlow Condensed` (600/700 uppercase, letter-spacing 1px) for category tags, table column headers, and status flags.
- **Quantitative & Numerical:** `JetBrains Mono` (tabular numerals, right-aligned numbers, monospaced ranges).
- **Body & Prose:** `Plus Jakarta Sans` (400 regular, line-height 1.6) for sustained editorial readability.
- **Layout Grid:** 12-column editorial grid, 8px base spacing unit, hairline 1px solid rules (`rgba(230, 228, 221, 0.15)` on navy, `rgba(7, 11, 30, 0.15)` on bone paper). Zero drop-shadow glows or floating blurry cards.

---

## 3. Rajasthani Cultural System
- **Single Flat Treatment:** Massive cropped Devanagari watermark **"हल्ला बोल"** (35 to 50vw, 8% to 12% opacity) placed in 3 or 4 anchor sections.
- **Banned Faux-Heritage Elements:** Zero scalloped arches, zero gold filigree, zero Rajasthani jaali borders, zero cartoonish ornament. Clean architectural geometries only.

---

## 4. Visual Media & Iconography
- **Portrait Standardization:** 1:1 square duotone/monochrome portraits with hairline borders. Same crop, same aspect ratio across all sections.
- **Icon Set:** Single local SVG set (Lucide), consistent 1.75px stroke width. Custom SVG marks reserved exclusively for Locked (`#DC2626`), Actionable (`#10B981`), and Overseas status.

---

## 5. Banned Design Tropes (Anti-AI Guardrails)
- ❌ Zero glowing blobs, neon conduits, or particle dust.
- ❌ Zero glassmorphism, blur backdrops, or purple gradients.
- ❌ Zero centered heading + 3 identical rounded cards layout.
- ❌ Zero corporate filler buzzwords ("seamless", "unlock", "elevate", "revolutionize").
- ❌ Zero decorative-only animations. Motion must communicate data transitions or scroll depth.
