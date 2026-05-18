# Changelog

All notable changes to the **DCS World Briefing Generator** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.1] — 2026-05-19

### Fixed

- **Charts and Annexes images were not compressed on upload** (regression introduced in v2.1.0).
  Both new sections — Charts and Annexes — bypassed the canvas-based compression pipeline and stored raw uploaded files (including 4–5 MB PNGs with alpha channel) directly into the briefing state. Briefings with a couple of high-resolution screenshots could easily exceed 10 MB once exported to PDF, which made them unshareable via Discord.
  The `change` listeners in `renderCharts` and `renderAnnexes` now call `compressImageFile(f)` like the other sections (Cover, SITAC, Phases, Radio Plan), producing JPEG q82 at most 1600 px wide on a white background.

### Added

- **Silent auto-recompression of legacy briefings.**
  A new function `recompressOversizedImagesInState(state)` walks the briefing state at load time and recompresses any embedded image whose base64 payload exceeds 800 KB. It runs in two places:
  - On JSON import (`loadJsonFile`) — awaited, followed by an immediate state persist and a discreet toast notification.
  - On app startup (`init`) — non-blocking; the UI renders immediately and the optimization happens in the background, then persists and refreshes the preview when done.
  Image paths visited are explicit (no magic walk): `cover.mapImage`, `sitac.mapImage`, `phases[*].mapImage`, `phases[*].images[*].data`, `charts[*].img`, `annexes[*].img`, `radioPlan.aircraftPlans[*].image`.
- New constant `IMG_RECOMPRESS_THRESHOLD = 800 * 1024` (configurable via `build_html.py`).

### Changed

- Bumped `APP_VERSION` from `2.1.0` to `2.1.1` in `build_html.py`.

### Preserved (explicitly not changed)

- **Wing and squadron logos** still go through `compressLogoFile` (PNG output, 256 px max, alpha channel preserved). Logos must blend onto the kraft texture, so they are intentionally excluded from the JPEG-conversion path and from the auto-recompression migration.

### Impact (measured on test briefing `foothold_m6`)

| Metric | Before v2.1.1 | After v2.1.1 | Delta |
|---|---|---|---|
| Briefing JSON size | 13 MB | 2 MB | -84 % |
| Exported PDF size | 13 MB | 5.3 MB | -59 % |
| Discord 10 MB limit | ❌ rejected | ✅ accepted with ~5 MB headroom | — |

The threshold of 800 KB was deliberately calibrated to leave already-optimized images untouched: on the test briefing, 5 of the 7 embedded images (cover 360 KB, SITAC 298 KB, two charts 310/410 KB, one phase image 348 KB) were below the threshold and preserved as-is. Only the two oversized PNG annexes (5.8 MB and 5.5 MB) triggered the recompression, each shrinking by roughly 97 %.

---

## [2.1.0] — 2026-05-16

### Added

- **PNG kneeboard export** — single page or multi-page ZIP, strict 794×1123 A4 format. Unified PDF/PNG export modal with a page selector.
- **Charts section** with an unlimited dynamic list of airport charts (replaces the two previously hardcoded charts).
- **Free-form Annexes section** — title + image + optional caption, unlimited list.
- Dedicated mobile tabs: 🗺 Charts and 📎 Annexes.

### Changed

- Automatic migration of legacy briefings: `annexes.chart1*/chart2*` fields are now mapped to `state.charts[]`.
- Chart and annex images can grow larger on the page (`max-height` 190 mm → 200 mm).
- Source files renamed: no more versions in filenames (`build_html.py`, `build_css.py`, `assets.json`).
- Python build scripts use `__file__`-relative paths for portability across environments.

### Fixed

- Toolbar overflow on tablet landscape (Xiaomi Pad 6, viewports 1100–1366 px).
- Roster page not refreshing after mission edits (11 missing `renderRoster()` calls).
- `btn-mode` regression — listener binding lost during refactor; the now-redundant button was removed entirely (mobile tab-bar already covers it).
- Inconsistent PNG export modal text ("900×1200" corrected to "794×1123 A4").
- Kraft background truncated in tablet portrait preview.
- **Bug A** — PNG export came out at 1985×2807 instead of 794×1123 (html2canvas was applying `devicePixelRatio` by default). Fixed with explicit `scale: 1`.
- **Bug B** — Squadron and header logos distorted in PNG export (html2canvas + `object-fit: contain` incompatibility). Fixed by replacing `<img>` with `<div background-image>`.
- **Bug C** — Squadron name rendered as an empty rectangle in PNG export (html2canvas + `inline-flex` incompatibility). Fixed with `display: flex; width: fit-content`.
- No progress feedback during PNG export. The export modal now stays open with a "Generating X/N…" button and a live toast.
- Intermittent "disappearing page" bug — preventive multi-layer CSS fix (`font-display: swap`, `overscroll-behavior: contain`, `contain: layout`, removal of `-webkit-overflow-scrolling: touch`).
- Annexes section invisible on tablet portrait (regression introduced when the section was added) — `data-active-tab` mapping fixed in `build_css.py`.
- Chart images overflowing A4 page bottom (`max-height: 230mm` too large) — reduced to `200mm`.

---

## [2.0.0] — 2025-XX-XX

### Added

- **Multi-wing support** — the application is now wing-agnostic. A wing configuration (id, name, logo, HQ stamp, squadrons) can be edited via the WING tab and exported as a JSON file for distribution. Pilots import the JSON to reskin the app for their wing.
- **Default generic wing** — `MY WING` with an `WG` SVG roundel, used when no wing config is present.
- **Four graphical themes** with a dropdown selector in the toolbar: `cw-nato` (Cold War NATO), `cw-soviet` (Cold War Soviet), `modern-nato`, `modern-east`. Theme preference is persisted in localStorage independently from briefing and wing state.
- **French and English user guides** as standalone responsive HTML, generated via `build_userdoc.py` and `build_userdoc_en.py`.

### Changed

- Three independent localStorage keys: `khr26_briefing_state_v2` (briefing in progress, kept for backward compatibility), `wing_config_v1` (wing config), `theme_v1` (theme).
- Public release on GitHub under MIT license: [github.com/MirabelleBenou/dcs-briefing-generator](https://github.com/MirabelleBenou/dcs-briefing-generator).

---

[2.1.1]: https://github.com/MirabelleBenou/dcs-briefing-generator/releases/tag/v2.1.1
[2.1.0]: https://github.com/MirabelleBenou/dcs-briefing-generator/releases/tag/v2.1.0
[2.0.0]: https://github.com/MirabelleBenou/dcs-briefing-generator/releases/tag/v2.0.0
