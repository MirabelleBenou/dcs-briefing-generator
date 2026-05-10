# DCS World Briefing Generator
![Intro-image](https://forum.dcs.world/uploads/monthly_2026_05/Capturedcran2026-05-08231721.png.cadb306c79dce1a6f6745893bebc0ac4.png)
> Generate beautifully styled mission briefings for DCS World — fully offline, in a single HTML file.

![Version](https://img.shields.io/badge/version-2.0.0-brown)
![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Web-green)
![Offline](https://img.shields.io/badge/offline-yes-success)

A single-file, offline-capable web application designed for DCS World virtual pilots and wing administrators to compose professional-looking mission briefings styled as Cold War era kraft military documents.

Developped with the help of Claude AI (I'm not a dev !)

---

## ✨ Features

- **Fully offline** — runs in any modern browser without internet, no installation, no server
- **Single HTML file** — open it, use it, share it
- **Multi-wing configurable** — each wing customizes its branding, squadrons, and logos
- **4 graphical themes** — Cold War NATO (default), Cold War Soviet, Modern NATO, Modern Eastern Bloc
- **PDF export** — print-to-PDF from your browser, no extra tools needed
- **Multi-platform** — works on PC (Windows/macOS/Linux) and tablets (Android/iOS)
- **Auto-save** — your briefing is preserved in your browser's local storage
- **Import/Export** — share briefings as JSON files, share wing configs across teams

## 📸 Screenshots

![screen1](https://forum.dcs.world/uploads/monthly_2026_05/Capturedcran2026-05-08231452.png.383c79d043b2ab71ec6873fadfb92fd7.png)

![screen2](https://forum.dcs.world/uploads/monthly_2026_05/Capturedcran2026-05-08231550.png.db3fe247fdc66966887c1b98f0fc3858.png)

![screen3](https://forum.dcs.world/uploads/monthly_2026_05/Capturedcran2026-05-08231646.png.1a955e00f6f78059489012efe6f2669f.png)

## 🚀 Quick Start (for pilots)

1. Download the latest `DCS_World_Briefing_Generator.html` from the [Releases](../../releases) page
2. Open it in **Chrome** (recommended) or any modern browser
3. Edit your briefing using the tabs on the left
4. Click **Aperçu** to preview, then **Imprimer** (Ctrl+P) to export as PDF

That's it. No installation, no account, no internet required.

## 🛠️ For wing administrators

Want to customize the branding for your virtual wing?

1. Open the application
2. Go to the **🛡 WING** tab
3. Edit wing name, logo, squadrons, callsigns, aircraft
4. Click **📤 Exporter config** to save your wing configuration as JSON
5. Distribute the JSON file to your pilots — they import it via **📥 Importer config**

The default `MY WING` configuration is generic. Replace it with your own to match your virtual wing identity.

## 📚 Documentation

- **[User Guide (FR)](./Docs/DCS_World_Briefing_Generator_User_Guide.html)** — Full user documentation in French
- **[User Guide (EN)](./Docs/DCS_World_Briefing_Generator_User_Guide_EN.html)** — Full user documentation in English
- **[Technical Documentation](./DOCS_DCS_World_Briefing_Generator.md)** — For contributors and developers

## 🏗️ Building from source

If you want to modify the code yourself:

### Prerequisites

- Python 3.8+ (no external dependencies, just standard library)

### Build

```bash
# Generate the CSS file
python3 build_css.py

# Generate the final HTML (uses build_css.py output + assets.json)
python3 build_html.py
```

The output `DCS_World_Briefing_Generator.html` is the distributable file.

### Project structure

```
.
├── build_html.py              # Main HTML builder (Python)
├── build_css.py               # CSS builder (Python)
├── assets.json                # Embedded fonts, kraft texture (base64)
├── wing_config_4th_veaw.json  # Example wing configuration
├── docs/
│   └── DCS_World_Briefing_Generator_User_Guide.html
├── DOCS_DCS_World_Briefing_Generator.md
├── README.md
└── LICENSE
```

## 🗺️ Roadmap

Planned future enhancements (no committed timeline):

- **English UI** — full internationalization (FR/EN toggle in toolbar)
- **Auto-save indicator** — visible feedback when briefing is saved
- **Briefing templates** — pre-filled templates for common mission types (CAS, CAP, SEAD)
- **Per-page PNG export** — share single pages on Discord without exporting the full PDF
- **URL-based sharing** — share a briefing via a single link

## 🤝 Contributing

Bug reports and feature suggestions are welcome via the [Issues](../../issues) page.

If you're a developer and want to contribute code:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Read [`DOCS_DCS_World_Briefing_Generator.md`](./DOCS_DCS_World_Briefing_Generator.md) to understand the architecture
4. Test your changes by rebuilding the HTML and opening it in Chrome
5. Submit a pull request

## ⚠️ Compatibility notes

- **Chrome / Edge** (recommended): all features work, including print-to-PDF
- **Firefox**: works but PDF rendering may differ slightly
- **Safari**: works on macOS and iOS, with minor visual variations
- **Mobile**: optimized for tablet (Android/iOS), usable on smartphone

## 📄 License

[MIT License](./LICENSE) — free to use, modify, and distribute, including for commercial purposes.

## 🙏 Acknowledgments

- Built for the DCS World virtual aviation community
- Initial version developed for the **4th VEAW** virtual wing — distributed as `wing_config_4th_veaw.json` example
- Cold War kraft SVG file provided by Flappie, thanks to him !

---

*This project is not affiliated with or endorsed by Eagle Dynamics, the developers of DCS World.*
