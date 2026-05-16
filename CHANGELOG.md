# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] — YYYY-MM-DD

### Added

- **PNG kneeboard export** — Export individual pages or all pages as a ZIP archive. Each PNG is rendered at strict A4 dimensions (794×1123 px) for use as in-game kneeboards in DCS World.
- **Unified export modal** with PDF/PNG choice and page selector — pick exactly which pages you want.
- **Progress feedback during PNG export** — the modal stays open with a dynamic "Generating X/N…" button while pages are rendered. No more wondering whether the app is frozen.
- **Charts section** with an unlimited dynamic list of airport charts (replaces the previous limit of 2 hardcoded charts). Add, reorder, and remove charts freely.
- **Free-form Annexes section** — a new editor section for arbitrary annexes with title + image + optional caption. Useful for additional briefings, intel images, navigation notes, or any custom content.
- **Automatic migration** of legacy briefings: old `annexes.chart1*`/`chart2*` fields are seamlessly converted to the new `state.charts[]` array on first load. No data loss.
- **Dedicated mobile tabs** 🗺 Charts and 📎 Annexes for tablet portrait use.

### Changed

- **Source filenames cleaned up**: no more version numbers in filenames. The build now uses stable names: `build_html.py`, `build_css.py`, `assets.json`. Versioning is tracked by Git tags and the `APP_VERSION` constant in `build_html.py`.
- **Relative paths via `__file__`**: build scripts now use `os.path.join(HERE, ...)` instead of hardcoded absolute paths. You can now run `python3 build_html.py` on any machine — the script reads its dependencies from its own directory.
- **Simplified toolbar**: the eye/preview toggle button (`btn-mode`) was removed. It was redundant with the mobile tab bar on tablets and unused on desktop.
- **Larger chart and annex images on page**: `max-height` increased from 190mm to 200mm. Charts now make better use of the available A4 page space, especially for portrait-format images.
- **Editor section numbering**: 08 Charts / 09 Annexes / 10 Wing Configuration (was previously 08 Annexes / 09 Wing).

### Fixed

#### UX & responsive
- `btn-mode` regression — the click handler binding was lost in a previous refactor, breaking the toolbar's preview toggle.
- Toolbar overflow on landscape tablets (Xiaomi Pad 6 and similar 1100-1366px viewports).
- Kraft background clipped in tablet portrait preview.
- Roster page not refreshing after mission edits (added 11 missing `renderRoster()` calls on mission CRUD events).
- PNG export modal text mismatched the actual export dimensions ("900×1200" → "794×1123 A4").

#### PNG export
- PNG dimensions incorrect on high-DPI devices — html2canvas was applying `window.devicePixelRatio` (×2.5 on Xiaomi Pad 6) by default. Now uses `scale: 1` explicitly for guaranteed 794×1123 pixel output.
- Squadron and header logos distorted in PNG output — html2canvas does not handle `<img>` + `object-fit: contain` correctly. Logos now use `<div>` + `background-image: url(...)` with `background-size: contain`, which is reliably rendered.
- Empty rectangle instead of squadron name on PNG mission pages — html2canvas does not handle `display: inline-flex` + `overflow: hidden` correctly. The `.squadron-chip` element now uses `display: flex; width: fit-content` instead.

#### Intermittent rendering
- "Disappearing page" bug — a hard-to-reproduce issue where a page would occasionally fail to render in preview. Mitigated with a preventive multi-layer CSS fix: `font-display: swap` on all `@font-face` declarations (eliminates 3-second font black-out), `overscroll-behavior: contain` on scrollable containers (isolates scroll, prevents cascade reflows), `contain: layout` on `.ed-section` (isolates layout computation), removal of deprecated `-webkit-overflow-scrolling: touch`.

#### v2.1.0 regressions caught before release
- Annexes section invisible on portrait tablets — missing `data-active-tab="annexes"` mapping in the responsive CSS. Now correctly maps to its editor section.
- Chart images overflowing the page — `max-height: 230mm` was too aggressive on A4 paper (297mm tall). Adjusted to 200mm with a safety margin.

### Migration from 2.0.0

No action required. Briefings saved in `localStorage` are migrated automatically on the next load. The legacy `annexes.chart1*`/`chart2*` fields are converted into the new `state.charts[]` array, and the new empty `state.annexes[]` array is initialized for free-form annexes.

If you exported a briefing as JSON in 2.0.0, you can re-import it in 2.1.0 without any modification.

### Technical notes

- HTML file size: ~825 KB (vs ~487 KB in 2.0.0). The increase is due to embedded html2canvas and JSZip libraries used for PNG export.
- The build pipeline now generates an intermediate `briefing.css` file alongside the scripts (was previously hidden under a temporary name). This file is not committed.
- All scripts now work from any directory thanks to `__file__`-relative paths.

---

## [2.0.0] — 2026-05-10

Initial public release. See README for feature overview.

[2.1.0]: https://github.com/MirabelleBenou/dcs-briefing-generator/releases/tag/v2.1.0
[2.0.0]: https://github.com/MirabelleBenou/dcs-briefing-generator/releases/tag/v2.0.0
