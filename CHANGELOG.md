# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2026-05-08

First public release.

### Added

- **Multi-wing configuration** — the application now supports any virtual wing, not just a specific one
- **Generic default wing** (`MY WING`) embedded by default, with a generic `WG` cockade logo
- **4 graphical themes** with runtime selector in toolbar:
  - `cw-nato` — Cold War NATO (default, kraft beige + olive)
  - `cw-soviet` — Cold War Soviet (ocre warm + Soviet star seal)
  - `modern-nato` — Modern NATO (bone white + digital seals)
  - `modern-east` — Modern Eastern Bloc (greyed paper + dark blue accents)
- **Theme persistence** in localStorage (key `theme_v1`), independent from wing config and briefing state
- **Roboto Mono** typography for modern themes (replaces Special Elite typewriter)
- **Soviet star seal** with custom rendering for the Soviet theme
- **Digital square seals** with classification IDs for modern themes
- **User Guide (FR)** — full HTML/PDF user documentation with 17 screenshots
- **Version display** in toolbar (currently `v2.0.0`)

### Changed

- Default wing is now a generic placeholder (`MY WING` with one example squadron `SQN-01` flying F-16C Viper)
- The 4th VEAW wing is now distributed only as an example file (`wing_config_4th_veaw.json`), no longer embedded as default
- HTML file size reduced from ~800 KB to ~480 KB by removing legacy embedded wing-specific assets
- Print CSS harmonized with screen CSS to ensure perfect parity between preview mode and exported PDF
- Image annexes max-height tuned (190mm for full pages, 88mm for stacked pairs) to prevent footer overlap

### Fixed

- Image annexes overlapping the footer on print PDF
- Discrepancy between preview mode and PDF export (images smaller in PDF than in preview)
- Regex bug in `exportWingConfig` (`\\s` instead of `\s`)
- Tab-bar gradient (mobile/tablet view) now follows the active theme

---

## Project history (pre-2.0.0)

The application was developed iteratively through 9 internal phases before this first public release:

- **Phases 1–7B** — Multi-wing refactoring (initially hardcoded for a single wing)
- **Phase 8** — Generic default wing for public distribution
- **Phase X** — Graphical themes (this release)
- **Phase 9** (planned) — Full UI internationalization (FR/EN toggle)

Future planned enhancements are tracked in the [Roadmap section of the README](./README.md#roadmap).

