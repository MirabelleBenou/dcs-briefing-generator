#!/usr/bin/env python3
"""
build_userdoc_en.py — Generates DCS_World_Briefing_Generator_User_Guide_EN.html
English user guide for DCS World Briefing Generator.
"""

import json, os
from datetime import date

VERSION    = "1.1"
BUILD_DATE = date.today().strftime("%Y-%m-%d")

ASSETS_PATHS = [
    "/home/claude/assets.json",
    "/mnt/project/assets.json",
    "./assets.json",
    "../assets.json",
]

FONT_FACE = ""
FONT_LINK = ""

for path in ASSETS_PATHS:
    if os.path.exists(path):
        with open(path) as f:
            A = json.load(f)
        FONT_FACE = f"""
@font-face {{
  font-family: 'Stardos Stencil';
  font-weight: 400;
  font-display: block;
  src: url('data:font/woff2;base64,{A["STARDOS_400"]}') format('woff2');
}}
@font-face {{
  font-family: 'Stardos Stencil';
  font-weight: 700;
  font-display: block;
  src: url('data:font/woff2;base64,{A["STARDOS_700"]}') format('woff2');
}}
@font-face {{
  font-family: 'Special Elite';
  font-weight: 400;
  font-display: block;
  src: url('data:font/woff2;base64,{A["SPECIAL_ELITE"]}') format('woff2');
}}"""
        print(f"Fonts loaded from {path}")
        break

if not FONT_FACE:
    FONT_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Stardos+Stencil:wght@400;700&family=Special+Elite&display=swap">'
    print("assets.json not found - using Google Fonts CDN")

CSS = f"""
{FONT_FACE}

:root {{
  --paper:        #d8c9a5;
  --paper-light:  #ede5ce;
  --paper-dark:   #b8a77c;
  --ink:          #1f1c16;
  --ink-faded:    #463f30;
  --olive:        #4a5230;
  --olive-dark:   #2c321e;
  --olive-deep:   #1a1e10;
  --khaki:        #807454;
  --khaki-light:  #a89a72;
  --rust:         #7a3a20;
  --red-stamp:    #a83524;
  --amber:        #c0892a;
  --amber-dark:   #8a5e15;
  --f-stencil:    'Stardos Stencil', 'Impact', 'Arial Narrow Bold', sans-serif;
  --f-body:       -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
  --f-mono:       ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
  --f-typewriter: 'Special Elite', 'Courier New', monospace;
  --radius: 3px;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ font-size: 16px; }}
body {{
  font-family: var(--f-body);
  background: #f0ead8;
  color: var(--ink);
  line-height: 1.65;
  font-size: 1rem;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}

/* COUVERTURE */
.cover {{
  min-height: 100vh;
  background: var(--olive-deep);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 60px 40px;
  position: relative;
  overflow: hidden;
}}
.cover::before {{
  content: '';
  position: absolute; inset: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 28px,
    rgba(255,255,255,.02) 28px, rgba(255,255,255,.02) 29px);
  pointer-events: none;
}}
.cover-badge {{
  font-family: var(--f-typewriter);
  font-size: 0.8rem;
  letter-spacing: 3px;
  color: var(--amber);
  text-transform: uppercase;
  border: 1px solid var(--amber-dark);
  padding: 4px 18px;
  margin-bottom: 48px;
}}
.cover-title {{
  font-family: var(--f-stencil);
  font-weight: 700;
  font-size: 3.5rem;
  letter-spacing: 4px;
  color: var(--paper-light);
  line-height: 1.1;
  text-transform: uppercase;
  text-shadow: 0 2px 12px rgba(0,0,0,.5);
  margin-bottom: 16px;
}}
.cover-sub {{
  font-family: var(--f-stencil);
  font-weight: 400;
  font-size: 1.75rem;
  letter-spacing: 6px;
  color: var(--khaki-light);
  text-transform: uppercase;
  margin-bottom: 56px;
}}
.cover-divider {{
  width: 120px; height: 2px;
  background: linear-gradient(90deg, transparent, var(--amber), transparent);
  margin: 0 auto 56px;
}}
.cover-meta {{
  font-family: var(--f-typewriter);
  font-size: 0.9rem;
  color: var(--khaki-light);
  line-height: 2.1;
}}
.cover-stamp {{
  position: absolute;
  bottom: 50px; right: 50px;
  font-family: var(--f-stencil);
  font-size: 1.2rem;
  letter-spacing: 2px;
  color: var(--red-stamp);
  border: 3px solid var(--red-stamp);
  padding: 6px 14px;
  transform: rotate(-8deg);
  opacity: .75;
  text-transform: uppercase;
}}

/* MISE EN PAGE — largeur web responsive */
.page, .toc-page {{
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 32px;
}}
@media (max-width: 720px) {{
  .page, .toc-page {{ padding: 32px 20px; }}
}}

/* TOC */
.toc-title {{
  font-family: var(--f-stencil);
  font-size: 1.5rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--olive-deep);
  border-bottom: 2px solid var(--khaki);
  padding-bottom: 8px;
  margin-bottom: 24px;
}}
.toc-entry {{
  display: flex; align-items: baseline; gap: 6px;
  padding: 4px 0; font-size: 0.95rem; color: var(--ink);
}}
.toc-entry.toc-h1 {{
  font-weight: 600; margin-top: 10px;
  font-size: 1rem; color: var(--olive-dark);
}}
.toc-entry.toc-h2 {{
  padding-left: 20px; color: var(--ink-faded); font-size: 0.9rem;
}}
.toc-dots {{
  flex: 1;
  border-bottom: 1px dotted var(--khaki-light);
  margin: 0 4px;
  position: relative; bottom: 3px;
}}

/* TITRES */
h1.sec-title {{
  font-family: var(--f-stencil);
  font-weight: 700;
  font-size: 2rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--olive-deep);
  padding: 14px 18px;
  background: linear-gradient(90deg, var(--paper-light) 0%, transparent 100%);
  border-left: 5px solid var(--olive);
  margin: 56px 0 24px;
  clear: both;
}}
h1.sec-title:first-child {{ margin-top: 0; }}
h1.sec-title .sec-num {{
  color: var(--khaki); margin-right: 12px; font-size: 1.65rem;
}}
h2.subsec {{
  font-family: var(--f-stencil);
  font-weight: 400; font-size: 1.2rem;
  letter-spacing: 2px; text-transform: uppercase;
  color: var(--olive);
  border-bottom: 1px solid var(--paper-dark);
  padding-bottom: 6px;
  margin: 32px 0 16px;
  clear: both;
}}
h3.subsubsec {{
  font-family: var(--f-body);
  font-weight: 700; font-size: 0.95rem;
  color: var(--ink-faded);
  margin: 22px 0 10px;
  text-transform: uppercase; letter-spacing: 1px;
}}

/* TEXTE */
p {{ margin-bottom: 12px; text-align: left; }}
ul, ol {{ margin: 8px 0 14px 22px; }}
li {{ margin-bottom: 5px; line-height: 1.55; }}
ul li::marker {{ color: var(--khaki); }}

code {{
  font-family: var(--f-mono); font-size: 0.88em;
  background: rgba(0,0,0,.07);
  border: 1px solid var(--paper-dark);
  padding: 1px 5px; border-radius: var(--radius);
  white-space: nowrap;
}}
kbd {{
  font-family: var(--f-mono); font-size: 0.85em;
  background: var(--olive-deep); color: var(--paper-light);
  border: 1px solid var(--khaki); border-bottom-width: 2px;
  padding: 2px 7px; border-radius: var(--radius); letter-spacing: .5px;
}}

/* ENCADRÉS */
.ud-tip, .ud-warn, .ud-admin {{
  display: flex; gap: 10px;
  padding: 12px 16px; border-radius: var(--radius);
  margin: 18px 0;
  font-size: 0.95rem; line-height: 1.55;
  clear: both;
}}
.ud-ico {{ font-size: 1.3rem; flex-shrink: 0; margin-top: 1px; }}
.ud-tip  {{ background: rgba(192,137,42,.12); border-left: 4px solid var(--amber); }}
.ud-tip  .ud-ico {{ color: var(--amber); }}
.ud-warn {{ background: rgba(168,53,36,.10); border-left: 4px solid var(--red-stamp); }}
.ud-warn .ud-ico {{ color: var(--red-stamp); }}
.ud-admin {{ background: rgba(74,82,48,.12); border-left: 4px solid var(--olive); }}
.ud-admin .ud-ico {{ color: var(--olive); }}

/* CAPTURES — vignettes uniformes, image entièrement visible, cliquables pour agrandir */
/* En inline-block : deux figures successives dans le HTML s'alignent automatiquement
   côte-à-côte sans wrapper. Sur mobile, elles repassent en pleine largeur.
   `object-fit: contain` garantit que toute l'image est visible, sans crop.
   Pour les bandes très horizontales (toolbar, etc.), la classe `ud-wide`
   affiche l'image en pleine largeur sans cadre fixe. */
figure.ud-screenshot {{
  display: inline-block;
  vertical-align: top;
  margin: 12px 12px 16px 0;
  padding: 0;
  width: 360px;
  max-width: 100%;
}}

figure.ud-screenshot .ud-shot-link {{
  display: block;
  position: relative;
  cursor: zoom-in;
  text-decoration: none;
  width: 100%;
  height: 220px;
  overflow: hidden;
  border: 1px solid var(--paper-dark);
  border-radius: var(--radius);
  box-shadow: 0 2px 12px rgba(0,0,0,.18);
  background: var(--paper-light);
  padding: 6px;
  transition: box-shadow .2s ease, transform .2s ease;
}}
figure.ud-screenshot .ud-shot-link:hover {{
  box-shadow: 0 5px 20px rgba(0,0,0,.30);
  transform: translateY(-2px);
}}

figure.ud-screenshot img {{
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center center;
}}

figure.ud-screenshot .ud-zoom-icon {{
  position: absolute;
  top: 8px; right: 8px;
  width: 28px; height: 28px;
  background: rgba(31,28,22,.75);
  color: var(--paper-light);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.95rem;
  opacity: 0;
  transition: opacity .2s ease;
  pointer-events: none;
  z-index: 2;
}}
figure.ud-screenshot .ud-shot-link:hover .ud-zoom-icon {{
  opacity: 1;
}}

figure.ud-screenshot figcaption {{
  font-size: 0.82rem; color: var(--ink-faded);
  text-align: center; font-style: italic;
  margin-top: 8px;
  line-height: 1.35;
}}

/* Variante WIDE — bandes horizontales (toolbars, lignes de boutons, toasts...) */
/* Pleine largeur de la colonne, hauteur auto, pas de crop */
figure.ud-screenshot.ud-wide {{
  display: block;
  width: 100%;
  margin: 16px auto 20px;
}}
figure.ud-screenshot.ud-wide .ud-shot-link {{
  height: auto;
  padding: 4px;
}}
figure.ud-screenshot.ud-wide img {{
  height: auto;
  max-height: 180px;
  object-fit: contain;
}}

/* Mobile : vignettes pleine largeur empilées */
@media (max-width: 720px) {{
  figure.ud-screenshot {{
    width: 100%;
    margin: 12px 0 16px;
  }}
  figure.ud-screenshot .ud-shot-link {{
    height: 200px;
  }}
}}

/* Placeholder injecté par JS quand l'image shot_NN.png n'existe pas (404) */
.ud-placeholder-box {{
  border: 2px dashed var(--khaki-light);
  background: rgba(216,201,165,.3);
  padding: 28px 20px; text-align: center;
  font-family: var(--f-mono); font-size: 0.8rem;
  color: var(--khaki); line-height: 1.6;
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  cursor: default;
}}
/* Placeholder dans une vignette standard : remplit le cadre 220px */
figure.ud-screenshot:not(.ud-wide) .ud-placeholder-box {{
  width: 100%;
  height: 220px;
}}
/* Placeholder dans une figure wide : hauteur raisonnable */
figure.ud-screenshot.ud-wide .ud-placeholder-box {{
  min-height: 120px;
  padding: 24px 20px;
}}
@media (max-width: 720px) {{
  figure.ud-screenshot:not(.ud-wide) .ud-placeholder-box {{
    height: 200px;
  }}
}}

/* TABLEAU */
table.ud-table {{
  width: 100%; border-collapse: collapse;
  font-size: 0.92rem; margin: 14px 0 22px;
  clear: both;
}}
.ud-table th {{
  background: var(--olive-deep); color: var(--paper-light);
  font-family: var(--f-stencil); font-weight: 700;
  letter-spacing: 1px; font-size: 0.88rem;
  padding: 9px 12px; text-align: left;
}}
.ud-table td {{
  padding: 9px 12px;
  border-bottom: 1px solid var(--paper-dark);
  vertical-align: top;
}}
.ud-table tr:nth-child(even) td {{ background: rgba(216,201,165,.3); }}

/* FAQ */
.faq-entry {{ margin: 18px 0; clear: both; }}
.faq-q {{
  font-weight: 700; color: var(--olive-dark);
  font-size: 0.98rem; margin-bottom: 5px;
}}
.faq-q::before {{ content: 'Q. '; color: var(--red-stamp); font-family: var(--f-stencil); }}
.faq-a {{ padding-left: 20px; color: var(--ink-faded); font-size: 0.95rem; }}

/* PRINT — préservation du rendu PDF d'origine */
@media print {{
  @page {{
    size: A4 portrait;
    margin: 20mm;
  }}
  html {{ font-size: 11pt; }}
  body {{ background: white; line-height: 1.58; }}
  .page, .toc-page {{
    max-width: 170mm;
    padding: 0;
  }}
  .cover {{ page-break-after: always; min-height: 297mm; }}
  .toc-page {{ page-break-after: always; }}
  h1.sec-title {{
    page-break-before: always;
    page-break-after: avoid;
    font-size: 22pt;
    margin: 0 0 24px;
  }}
  h1.sec-title:first-child {{ page-break-before: auto; }}
  h2.subsec {{ page-break-after: avoid; font-size: 13pt; }}
  h3.subsubsec {{ page-break-after: avoid; font-size: 10.5pt; }}
  p {{ text-align: justify; }}
  /* Vignettes en print : restaurer l'image complète (pas de crop), pleine largeur, sans loupe */
  figure.ud-screenshot {{
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 20px 0 !important;
    page-break-inside: avoid;
  }}
  figure.ud-screenshot .ud-shot-link {{
    height: auto !important;
    overflow: visible !important;
    box-shadow: none !important;
    border: 1px solid #999 !important;
    cursor: default !important;
    pointer-events: none;
    transform: none !important;
  }}
  figure.ud-screenshot .ud-shot-link::after {{ display: none !important; }}
  figure.ud-screenshot img {{
    height: auto !important;
    object-fit: contain !important;
  }}
  figure.ud-screenshot .ud-zoom-icon {{ display: none !important; }}
  .ud-tip, .ud-warn, .ud-admin,
  table.ud-table, .faq-entry {{ page-break-inside: avoid; }}
}}
"""

SHOTS_BASE_URL = "https://mirabellebenou.github.io/dcs-briefing-generator/docs/screenshots"

def _html_escape(s):
    """Escape HTML special chars for safe use in attributes."""
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
                  .replace("<", "&lt;").replace(">", "&gt;"))

def shot(num, desc, caption, dims="", wide=False):
    _key = int(num) if str(num).isdigit() else 0
    _cls = "ud-screenshot ud-wide" if wide else "ud-screenshot"
    url = f"{SHOTS_BASE_URL}/shot_{_key:02d}.png"
    _esc_desc = _html_escape(desc)
    _esc_caption = _html_escape(caption)
    _esc_dims = _html_escape(dims)
    return (
        f'<figure class="{_cls}" data-shot="{num}"'
        f' data-desc="{_esc_desc}" data-caption="{_esc_caption}" data-dims="{_esc_dims}">\n'
        f'  <a class="ud-shot-link" href="{url}" target="_blank" rel="noopener" title="Click to enlarge">\n'
        f'    <img src="{url}" alt="{_esc_caption}" loading="lazy"'
        f' onerror="window.shotFallback&amp;&amp;window.shotFallback(this)">\n'
        f'    <span class="ud-zoom-icon" aria-hidden="true">⤢</span>\n'
        f'  </a>\n'
        f'  <figcaption>{caption}</figcaption>\n'
        '</figure>'
    )

def tip(t):    return f'<aside class="ud-tip"><span class="ud-ico">&#9758;</span><div>{t}</div></aside>'
def warn(t):   return f'<aside class="ud-warn"><span class="ud-ico">&#9888;</span><div>{t}</div></aside>'
def admin(t):  return f'<aside class="ud-admin"><span class="ud-ico">&#9881;</span><div>{t}</div></aside>'
def locale(t): return f'<aside class="ud-locale"><span class="ud-ico">&#127760;</span><div>{t}</div></aside>'

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DCS World Briefing Generator &mdash; User Guide v{VERSION}</title>
{FONT_LINK}
<style>{CSS}</style>
</head>
<body>
<script>
/* Browser-side fallback: if a shot_NN.png image fails to load (404),
   replace the clickable link with a visual placeholder. */
window.shotFallback = function(img) {{
  var fig = img.closest('figure.ud-screenshot');
  if (!fig) return;
  var link = img.closest('a.ud-shot-link');
  var num = fig.getAttribute('data-shot') || '?';
  var desc = fig.getAttribute('data-desc') || '';
  var dims = fig.getAttribute('data-dims') || '';
  var dimsText = dims ? ', ~' + dims : '';
  var ph = document.createElement('div');
  ph.className = 'ud-placeholder-box';
  ph.textContent = '[SCREENSHOT ' + num + ': ' + desc + dimsText + ']';
  fig.classList.add('ud-placeholder');
  if (link && link.parentNode) {{
    link.parentNode.replaceChild(ph, link);
  }}
}};
</script>

<!-- COVER -->
<div class="cover">
  <div class="cover-badge">Reference Document // For Pilots &amp; Wing Admins</div>
  <div class="cover-title">DCS World<br>Briefing Generator</div>
  <div class="cover-sub">User Guide</div>
  <div class="cover-divider"></div>
  <div class="cover-meta">
    Version {VERSION}<br>
    Edition of {BUILD_DATE}<br>
    <br>
    Print to PDF &rarr; Chrome <kbd>Ctrl+P</kbd>
  </div>
  <div class="cover-locale-notice">Application interface in French &mdash; English UI planned in a future release</div>
  <div class="cover-stamp">V{VERSION} &mdash; {BUILD_DATE}</div>
</div>

<!-- TABLE OF CONTENTS -->
<div class="toc-page">
  <div class="toc-title">Table of Contents</div>

  <div class="toc-entry toc-h1"><span>1. Getting Started</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>1.1 Opening the application</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>1.2 Interface overview</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>1.3 Edit mode vs Preview mode</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>2. Creating a Complete Briefing</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.1 Metadata &mdash; &#9881; tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.2 Cover page &mdash; &#9685; tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.3 Tactical situation &mdash; &#9635; SITAC tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.4 Mission overview &mdash; &#9992; tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.5 Radio plan &mdash; &#128251; tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.6 Individual missions &mdash; &#8853; tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.7 Crew &mdash; &#128100; tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.8 Charts &mdash; 🗺 tab</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.9 Free-form Appendices &mdash; &#128206; tab</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>3. Saving and Resuming a Briefing</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.1 Automatic local save</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.2 Exporting a briefing as JSON</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.3 Importing an existing briefing</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.4 Starting fresh</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>4. Exporting to PDF</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.1 Preview mode verification</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.2 Exporting to PDF (Windows / macOS)</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.3 Exporting to PDF on Android</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.4 PNG kneeboard export</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.5 Best practices</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>5. Wing Configuration (Admin)</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.1 What is a wing config?</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.2 Editing the wing identity</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.3 Managing squadrons</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.4 Loading logos</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.5 Exporting, importing, resetting</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>6. FAQ and Tips</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h1"><span>7. Appendix &mdash; Credits and Licenses</span><span class="toc-dots"></span></div>

</div>

<!-- § 1 GETTING STARTED -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">01</span> Getting Started</h1>

{locale("""<div>
<strong>About localization</strong><br><br>
This guide is the English version of the user documentation.
The application interface itself remains in French at the time of writing.
Screenshots in this guide therefore show French labels &mdash; alongside each label
you will find the English equivalent in parentheses
(e.g., &laquo;&nbsp;<strong>Sauver</strong>&nbsp;(Save)&nbsp;&raquo;).
A full English UI is planned for a future release.
</div>""")}

<h2 class="subsec">1.1 Opening the Application</h2>

<p>No installation, no server, no account required. Double-click <code>DCS_World_Briefing_Generator.html</code> and you are ready to go. The application runs entirely in your browser, offline.</p>

<ul>
  <li><strong>Recommended browser: Chrome (or any Chromium-based browser).</strong> PDF output is cleanest in Chrome, and that is the primary target platform.</li>
  <li>Firefox and Safari work for editing, but may behave differently when printing.</li>
  <li>On Android tablets, copy the HTML file to your device (USB cable, Drive, email&hellip;) and open it with Chrome.</li>
</ul>

{tip("Keep the HTML file in a fixed folder on your PC &mdash; your briefing data is tied to the file&rsquo;s location via browser storage.")}

<h2 class="subsec">1.2 Interface Overview</h2>

<p>When the application opens, you are in <strong>edit mode</strong>. The interface is split into two simple zones:</p>

{shot("01", "full toolbar in edit mode: Sauver / Charger / Imprimer / Reset visible", "The toolbar at the top of the screen", wide=True)}

<p>At the top, the <strong>toolbar</strong> &mdash; your wing name on the left, the main action buttons on the right. Below it, the <strong>tabs</strong> that give access to each section of the briefing.</p>

{shot("02", "full editor view on desktop: toolbar + tabs + open form, demo data visible", "The editor on a wide screen")}

<p>On a tablet, the tabs move to the bottom of the screen, within thumb reach:</p>

{shot("03", "editor on Android tablet: icon-only tabs at the bottom of the screen", "On tablet &mdash; tabs move to the bottom")}

<p>Available tabs, left to right:</p>

<table class="ud-table">
  <thead><tr><th>Icon</th><th>Name</th><th>What you do there</th></tr></thead>
  <tbody>
    <tr><td>&#9881;</td><td>Meta</td><td>Date, classification, document reference</td></tr>
    <tr><td>&#9685;</td><td>Cover</td><td>Operation title, context, cover map</td></tr>
    <tr><td>&#9635;</td><td>SITAC</td><td>Tactical situation, weather, SITREP entries</td></tr>
    <tr><td>&#9992;</td><td>Mission</td><td>Objectives, bases, threats (mission overview)</td></tr>
    <tr><td>&#128251;</td><td>Radio</td><td>Common frequencies and per-aircraft radio plans</td></tr>
    <tr><td>&#8853;</td><td>Missions</td><td>Individual mission cards per pilot</td></tr>
    <tr><td>&#128100;</td><td>Crew</td><td>Order of battle &mdash; groups and pilots</td></tr>
    <tr><td>🗺</td><td>Charts</td><td>Airport charts (approach, taxiway, communication…)</td></tr>
    <tr><td>&#128206;</td><td>Free-form Appendices</td><td>Free illustrated content at the end of the briefing</td></tr>
    <tr><td>&#128737;</td><td>Wing</td><td>Wing configuration (admin section)</td></tr>
    <tr><td>&#9672;</td><td>Preview</td><td>Print-ready rendering of the briefing</td></tr>
  </tbody>
</table>

<h2 class="subsec">1.3 Edit Mode vs Preview Mode</h2>

<p>The application has two modes, and switching between them takes a single click:</p>

<ul>
  <li><strong>Edit mode</strong> &mdash; you fill in the forms. This is where all the work happens.</li>
  <li><strong>Preview mode</strong> &mdash; the briefing is displayed in A4 format, exactly as it will print. No forms, just the final rendering.</li>
</ul>

<p>To switch: click the <strong>&#9672; Aperçu</strong> tab directly.</p>

{shot("04", "active preview mode: A4 cover page rendered in military kraft style, no editor UI", "Preview mode &mdash; what you will get in the final PDF")}

{tip("Check the preview regularly while you work. It is the best way to catch layout issues before printing.")}

</div>

<!-- § 2 CREATING A COMPLETE BRIEFING -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">02</span> Creating a Complete Briefing</h1>

<p>We will walk through the tabs in order, left to right. That is how a briefing naturally builds up, and it is the best way to make sure nothing gets missed.</p>

<h2 class="subsec">2.1 Metadata &mdash; &#9881; Tab</h2>

<p>These are the header fields that appear in the footer of every printed page. A few fields, quickly filled.</p>

{shot("05", "Metadata tab filled in: Operation, Mission code, Date, Classification, Reference visible", "&#9881; Meta tab")}

<ul>
  <li><strong>Operation</strong> &mdash; the operation name (e.g., &ldquo;IRON DAWN&rdquo;).</li>
  <li><strong>Mission code</strong> &mdash; a short code identifying the sortie (e.g., &ldquo;ALPHA-7&rdquo;).</li>
  <li><strong>Mission date</strong> &mdash; free-form (e.g., &ldquo;14 JAN 2025 / ZULU&rdquo;).</li>
  <li><strong>Classification</strong> &mdash; the fictional classification level displayed on every page: CONFIDENTIEL D&Eacute;FENSE, SECRET D&Eacute;FENSE, TR&Egrave;S SECRET, NON CLASSIFI&Eacute;, NATO RESTRICTED, NATO SECRET.</li>
  <li><strong>Document reference</strong> &mdash; document number or internal reference (e.g., &ldquo;4VEAW/OPS/2025-001&rdquo;).</li>
</ul>

{tip("Takes two minutes and gives the briefing an immediate professional feel. Don&rsquo;t skip it.")}

<h2 class="subsec">2.2 Cover Page &mdash; &#9685; Tab</h2>

<p>The first page of the printed briefing. This is where you set the scene for everything that follows.</p>

{shot("06", "Cover tab filled in with an operation map loaded, title and context text visible", "&#9685; Cover tab")}

<ul>
  <li><strong>Operation title</strong> &mdash; displayed in large stencil lettering on the cover. Short and punchy works best.</li>
  <li><strong>Narrative / Context</strong> &mdash; a free-text paragraph giving the situation to the pilots. This is the text they will read before take-off.</li>
  <li><strong>Operation map</strong> &mdash; drag-and-drop an image, or click the zone to select one. PNG, JPEG, WEBP &mdash; all formats accepted.</li>
</ul>

{tip("A DCS F10 map screenshot, cropped and annotated in 30 seconds in any image editor, works perfectly. Aim for 1200 px wide for clean print quality.")}

<h2 class="subsec">2.3 Tactical Situation &mdash; &#9635; SITAC Tab</h2>

<p>A summary of the situation at mission time &mdash; where forces stand, what the context is, what the weather looks like.</p>

<ul>
  <li><strong>SITAC date</strong> &mdash; may differ from the mission date if the SITAC was compiled the day before.</li>
  <li><strong>SITREP entries</strong> &mdash; a list of short situation points (+ Add entry button). Enemy positions, restricted areas, red alerts&hellip;</li>
  <li><strong>METAR</strong> &mdash; weather in METAR format or plain text (&ldquo;Ceiling 3 000 ft, wind 270/15 kt&rdquo;).</li>
  <li><strong>SITAC map</strong> &mdash; optional: an annotated image showing friendly/enemy positions. If left blank, the page stays clean.</li>
</ul>

<h2 class="subsec">2.4 Mission Overview &mdash; &#9992; Tab</h2>

<p>The operational body of the mission: what needs to be done, where to land, and what can shoot back.</p>

<ul>
  <li><strong>Primary objectives</strong> &mdash; a list (+ Add objective). One line, one idea &mdash; that is the right format.</li>
  <li><strong>FARPs &amp; Airfields</strong> &mdash; available bases with their status (friendly, neutral, hostile).</li>
  <li><strong>Threats</strong> &mdash; check-boxes by type (Armor, APC, AAA, SAM) with levels or short descriptions.</li>
  <li><strong>Threat notes</strong> &mdash; free-text field for active SAMs, no-fly zones, or anything that does not fit the check-boxes.</li>
</ul>

<h2 class="subsec">2.5 Radio Plan &mdash; &#128251; Tab</h2>

<p>All frequencies in one place. This tab is split into two parts:</p>

{shot("09", "Radio plan tab: common radio items filled in + one aircraft with its channels configured", "&#128251; Radio tab")}

<ul>
  <li><strong>Radio items</strong> (max 6) &mdash; frequencies common to all pilots: primary ATC, mission frequency, guard&hellip; These appear on page 3 of the printed briefing.</li>
  <li><strong>Per-aircraft radio plans</strong> &mdash; for each aircraft type in use (F-16C, F/A-18C, Mi-8&hellip;), define the radios and their preset channels. You can also load an <strong>image</strong> (a screenshot of the in-game radio preset) to replace the generated table.</li>
</ul>

{tip("Define the common radio items first, then map them to the per-aircraft presets. Consistency across pages is guaranteed that way.")}

<h2 class="subsec">2.6 Individual Missions &mdash; &#8853; Tab</h2>

<p>Often the longest section to fill in &mdash; and the most personalized. Each pilot or crew can have their own mission card.</p>

{shot("07", "Missions tab: one open mission card with pilot, squadron, aircraft and notes visible", "&#8853; Missions tab &mdash; an open card")}

<ul>
  <li>The <kbd>&#9668;</kbd> <kbd>&#9658;</kbd> buttons navigate between missions; <kbd>+</kbd> creates one; <kbd>&#9672;</kbd> duplicates; <kbd>&#8593;</kbd> <kbd>&#8595;</kbd> reorder; <kbd>&times;</kbd> deletes.</li>
  <li>Each mission card includes: pilot, <strong>Escadron affect&eacute;</strong> (Assigned squadron, from the wing roster), <strong>Sous-groupe</strong> (optional sub-element/flight name), aircraft type, loadout, execution steps, and free-text notes.</li>
</ul>

{shot("08", "squadron selector drop-down: wing squadrons listed (541-TFS / DUFF, 329-Mira / ARROW...)", "The squadron selector")}

{tip("The selector automatically lists the squadrons configured in the &#128737; Wing tab. If it is empty, the wing has no squadrons yet &mdash; see &sect; 5.")}

{warn("If a squadron is missing from the selector, missions that reference it will still display, but without squadron branding. No crash &mdash; just a blank field.")}

<h2 class="subsec">2.7 Crew &mdash; &#128100; Tab</h2>

<p>The Crew tab generates an order of battle (ORBAT) page in the briefing &mdash; but only if you actually add pilots here. Leave it empty and no crew page is generated.</p>

<ul>
  <li>Organize pilots into <strong>groups</strong> (flight, section, squadron&hellip;).</li>
  <li>Each group lists pilots with their callsign, rank, and optional notes.</li>
</ul>

<h2 class="subsec">2.8 Charts &mdash; 🗺 Tab</h2>

<p>The Charts tab lets you add airport charts to the briefing. These charts are typically approach, taxiway, or communication diagrams downloaded from sources such as Chartfox or official aeronautical publications.</p>

<p>For each chart, you fill in:</p>
<ul>
  <li>A <strong>title</strong> (e.g., &ldquo;LFMN &mdash; ILS RWY 04R&rdquo;)</li>
  <li>An <strong>image</strong> (PNG or JPEG) loaded by drag-and-drop or via the selection button</li>
  <li>An optional <strong>comment</strong> to annotate or provide context for the chart</li>
</ul>

<p>The <code>+ Add a chart</code> button lets you add as many charts as needed. Charts appear in the final briefing in the order they were entered.</p>

{shot("18", "Charts tab: list of charts with the '+ Add a chart' button visible", "The Charts tab")}

{tip("Optimise your chart images before loading them. A 4K PNG at 8 MB will add no visual value over a 1500 px PNG at 500 KB, and will only bloat the exported briefing.")}

<h2 class="subsec">2.9 Free-form Appendices &mdash; &#128206; Tab</h2>

<p>The Free-form Appendices tab fills the role of the Appendices tab in v2.0.0: it lets you add free illustrated content at the end of the briefing &mdash; diagrams, reference notes, photos, enemy OOB, etc.</p>

<p>Each appendix combines:</p>
<ul>
  <li>A mandatory <strong>title</strong></li>
  <li>An optional <strong>image</strong> (loaded by drag-and-drop)</li>
  <li>A free-length <strong>comment field</strong></li>
</ul>

{shot("19", "Free-form Appendices tab: list entry showing title field, image zone, and comment area", "The Free-form Appendices tab")}

{admin("Appendices appear in the final briefing in the order they were entered. To reorder them, use the up/down arrows next to each appendix.")}

</div>

<!-- § 3 SAVING -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">03</span> Saving and Resuming a Briefing</h1>

<h2 class="subsec">3.1 Automatic Local Save</h2>

<p>Good news: there is nothing to do. The application continuously saves your current briefing to browser local storage (localStorage). Close the tab, shut down the PC, come back the next day &mdash; your work is still there.</p>

{warn("This automatic save is tied to the <strong>browser</strong> and to the <strong>location of the HTML file</strong> on your drive. If you move or rename the HTML file, or if you clear browser data, the current briefing is lost with it. For a durable save, use the JSON export.")}

<h2 class="subsec">3.2 Exporting a Briefing as JSON</h2>

<p>The JSON export is the permanent save &mdash; a file you can archive, share with a squadronmate, or reload six months later.</p>

{shot("11", "close-up of the Sauver button in the toolbar, cursor hovering over it", "The Sauver (Save) button", wide=True)}

<ul>
  <li>Click <kbd>Sauver</kbd> (Save) in the toolbar.</li>
  <li>A file named <code>briefing_OPERATION_DATE.json</code> is downloaded automatically.</li>
  <li>Keep it somewhere safe &mdash; it is your only portable copy of the briefing.</li>
</ul>

{tip("Good habit: export to JSON as soon as the briefing has meaningful content. A simple naming convention &mdash; <code>OPNAME_YYYYMMDD.json</code> &mdash; will save you when searching your archives.")}

<h2 class="subsec">3.3 Importing an Existing Briefing</h2>

<p>Resuming a briefing from a previous session, or a squadronmate sends you theirs:</p>

<ul>
  <li>Click <kbd>Charger</kbd> (Load) in the toolbar.</li>
  <li>Select the <code>.json</code> file in the file picker.</li>
  <li>The briefing loads immediately.</li>
</ul>

{warn("Loading <strong>replaces</strong> the current briefing without further confirmation. If you have unsaved work, export it as JSON first.")}

<h2 class="subsec">3.4 Starting Fresh</h2>

<ul>
  <li>Click <kbd>R&eacute;initialiser</kbd> (Reset) in the toolbar.</li>
  <li>A confirmation prompt appears &mdash; that is the only safeguard.</li>
  <li>The entire briefing is cleared, including the automatic browser save.</li>
</ul>

{tip("If you have a template briefing you reuse regularly (fixed structure, wing configured, common radios set), export it as JSON and reload it at the start of each new mission rather than starting from scratch.")}

</div>

<!-- § 4 EXPORTING TO PDF -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">04</span> Exporting to PDF</h1>

<h2 class="subsec">4.1 Preview Mode Verification</h2>

<p>Before printing, take a quick look in <strong>Preview mode</strong> &mdash; the &#9672;&nbsp;Aperçu tab. Check that:</p>
<ul>
  <li>The cover page shows the correct title and map.</li>
  <li>Content pages are not truncated.</li>
  <li>All individual mission cards are present.</li>
  <li>Map and chart images are legible.</li>
</ul>

{tip("What you see in Preview is exactly what will appear in the final PDF. Better to catch issues now than after the export.")}

<h2 class="subsec">4.2 Exporting to PDF (Windows / macOS)</h2>

<p>Everything happens inside Chrome &mdash; no third-party software needed. The <kbd>Imprimer</kbd> (Print) button automatically switches to Preview mode first.</p>

<ol>
  <li>Press <kbd>Ctrl</kbd>+<kbd>P</kbd> (Windows / Linux) or <kbd>&#8984;</kbd>+<kbd>P</kbd> (macOS).</li>
  <li>Select <strong>&ldquo;Save as PDF&rdquo;</strong> as the destination.</li>
  <li>Set the following options:</li>
</ol>

{shot("12", "Chrome print dialog: Save as PDF selected, Margins and Background graphics options visible", "The Chrome print dialog")}

<table class="ud-table">
  <thead><tr><th>Option</th><th>Recommended value</th></tr></thead>
  <tbody>
    <tr><td>Paper size</td><td>A4</td></tr>
    <tr><td>Orientation</td><td>Portrait</td></tr>
    <tr><td>Margins</td><td>None (the app manages its own margins)</td></tr>
    <tr><td>Scale</td><td>100%</td></tr>
    <tr><td>Background graphics</td><td>&#10003; Enabled &mdash; required for the kraft background</td></tr>
  </tbody>
</table>

{warn("If you forget to enable <strong>Background graphics</strong>, the kraft background turns white and section headers lose their color. Content remains printable, but the visual effect disappears.")}

<h2 class="subsec">4.3 Exporting to PDF on Android</h2>

<p>On Android with Chrome, the <kbd>Imprimer</kbd> (Print) button opens the native Android print system or share menu directly:</p>

<ul>
  <li>Tap <kbd>Imprimer</kbd> (Print) in the toolbar.</li>
  <li>Select <strong>&ldquo;Save as PDF&rdquo;</strong> as the destination.</li>
  <li>Same settings as the desktop version (scale 100&nbsp;%, backgrounds enabled, A4).</li>
</ul>

{tip("On Android, if the print preview appears cropped, verify that the scale is set to 100% and not &ldquo;Fit to page&rdquo; &mdash; Chrome on Android may offer both.")}

<h2 class="subsec">4.4 PNG Kneeboard Export</h2>

<p>In addition to the standard PDF export, the generator produces a PNG export optimised for DCS <strong>kneeboards</strong> &mdash; the virtual kneepads displayed in-game during a flight.</p>

<p>To export as PNG kneeboard:</p>
<ol>
  <li>Click the <code>Imprimer</code> (Print) button in the toolbar</li>
  <li>In the export modal, select the <strong>PNG kneeboard</strong> option (default: PDF)</li>
  <li>Check the pages to export in the list shown (all pages checked by default)</li>
  <li>Click <code>Export</code></li>
</ol>

<p>A ZIP file is generated, containing one PNG per selected page. Each PNG is sized to standard DCS kneeboard ratios.</p>

{shot("20", "briefing export modal: choice between PDF and PNG kneeboard, page selector with checkboxes", "The multi-format export modal")}

{tip("You can uncheck pages not needed during flight (cover page, administrative appendices) to keep only what matters in the kneeboard and reduce cognitive load in the cockpit.")}

<h2 class="subsec">4.5 Best Practices</h2>

<ul>
  <li><strong>Prepare early.</strong> A briefing done the evening before is a briefing you have time to review and fix.</li>
  <li><strong>Keep the exported PDF.</strong> It is the mission archive, and it comes in handy if a squadronmate missed the live brief.</li>
  <li><strong>Share the JSON, not the PDF</strong>, if another pilot needs to edit the briefing.</li>
</ul>

</div>

<!-- § 5 WING CONFIGURATION -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">05</span> Wing Configuration</h1>

{admin("This section is for <strong>wing admins</strong> &mdash; those who configure the application for the whole team. If your admin has already taken care of this, you can skip ahead to &sect;&nbsp;6.")}

<h2 class="subsec">5.1 What Is a Wing Config?</h2>

<p>The wing configuration is the set of data that personalizes the app for your virtual wing:</p>

<ul>
  <li>The <strong>name and identity</strong> of the wing &mdash; what appears in the toolbar, page headers, and footers.</li>
  <li>The list of <strong>squadrons</strong> with their names, callsigns, and logos.</li>
  <li>The <strong>main wing logo</strong> displayed on the cover page.</li>
  <li>The <strong>HQ stamp</strong> shown on the cover page.</li>
</ul>

<p>Once configured, this config applies to all briefings created with that installation. It exports to a single JSON file for easy distribution to every pilot in the wing.</p>

{admin("The wing config and the briefing are two independent layers. Resetting the briefing does not touch the wing config. Changing the wing config does not affect the current briefing.")}

<h2 class="subsec">5.2 Editing the Wing Identity</h2>

{shot("13", "Wing tab fully open: wing Identity section with Short name, ID, Full name, logo loaded", "The &#128737; Wing tab")}

<p>In the <strong>&#128737;&nbsp;Wing</strong> tab, under the Wing identity section:</p>

<ul>
  <li><strong>Nom court</strong> (Short name) &mdash; displayed in the toolbar (e.g., &ldquo;4th VEAW&rdquo;). Keep it under 10 characters.</li>
  <li><strong>Identifiant</strong> (ID) &mdash; a technical key with no spaces or slashes (e.g., &ldquo;4th-veaw&rdquo;). Used internally.</li>
  <li><strong>Nom complet</strong> (Full name) &mdash; the wing&rsquo;s full name (e.g., &ldquo;4th Virtual Expeditionary Air Wing&rdquo;).</li>
  <li><strong>Titre de l&rsquo;application</strong> (App title) &mdash; text shown in the browser tab.</li>
  <li><strong>Tampon HQ</strong> (HQ stamp) &mdash; stamp text on the cover page (e.g., &ldquo;HQ VEAW // CLASSIFIED&rdquo;).</li>
</ul>

<h2 class="subsec">5.3 Managing Squadrons</h2>

<p>The squadrons configured here feed directly into the squadron selector in the &#8853;&nbsp;Missions tab.</p>

{shot("14", "Squadron card expanded for editing: ID, Callsign, Full name, Nickname, Aircraft and Logo visible", "Editing a squadron card")}

<ul>
  <li>Click <kbd>+ Ajouter un escadron</kbd> (Add a squadron) to create a new squadron.</li>
  <li>Each squadron entry includes: an <strong>ID</strong> (e.g., &ldquo;541-TFS&rdquo;), a <strong>callsign</strong> (e.g., &ldquo;DUFF&rdquo;), a <strong>full name</strong>, an optional <strong>nickname</strong>, the <strong>aircraft types</strong> it flies, and an optional <strong>logo</strong>.</li>
  <li>Click an existing card to expand, edit, or delete it.</li>
</ul>

{warn("Deleting a squadron does not modify missions that already reference it &mdash; they retain the ID, but the name and logo will no longer appear. Do this before distributing a final briefing, not after.")}

<h2 class="subsec">5.4 Loading Logos</h2>

{shot("15", "Squadron logo drag-and-drop zone with active drop indicator", "Loading a logo by drag-and-drop", wide=True)}

<ul>
  <li><strong>Main wing logo</strong> &mdash; appears on the cover page. Recommended: transparent PNG, 400&times;400&nbsp;px minimum, &lt;&nbsp;200&nbsp;KB.</li>
  <li><strong>Squadron logo</strong> (one per squadron) &mdash; displayed on mission cards. Same recommendations.</li>
</ul>

<p>Drag and drop an image onto the zone, or click it to open the file picker.</p>

{tip("Logos are stored as base64 inside the config file. Large logos (&gt;500&nbsp;KB) inflate the exported JSON considerably. Optimize your PNGs before loading &mdash; a wing logo does not need to be in 4K.")}

<h2 class="subsec">5.5 Exporting, Importing, Resetting</h2>

{shot("16", "Import / Export / Reset buttons at the bottom of the Wing tab with config file size displayed", "Wing config management buttons", wide=True)}

<ul>
  <li><kbd>&#128229;&nbsp;Importer config</kbd> (Import config) &mdash; loads a wing configuration JSON file.</li>
  <li><kbd>&#128228;&nbsp;Exporter config</kbd> (Export config) &mdash; downloads the current configuration as a JSON file.</li>
  <li><kbd>&#9851;&nbsp;R&eacute;initialiser</kbd> (Reset) &mdash; restores the example wing configuration bundled with the app.</li>
</ul>

{admin("Distribution workflow: once the admin has set up the wing, they export the config via <kbd>&#128228;&nbsp;Exporter config</kbd> and share the JSON file with all pilots (Discord, email, Drive&hellip;). Each pilot imports it via <kbd>&#128229;&nbsp;Importer config</kbd>. Everyone then sees the same squadrons in the selector.")}

</div>

<!-- § 6 FAQ -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">06</span> FAQ and Tips</h1>

<div class="faq-entry">
  <div class="faq-q">I accidentally closed the tab. Is my briefing lost?</div>
  <div class="faq-a">No. The automatic save (localStorage) kept everything. Simply reopen <code>DCS_World_Briefing_Generator.html</code> in the same browser &mdash; your work is there. <em>Exception:</em> if you cleared browser data or moved the HTML file since then, the briefing is gone. Hence the importance of regular JSON exports.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">My squadron does not appear in the mission selector.</div>
  <div class="faq-a">The selector only lists squadrons defined in the &#128737;&nbsp;Wing tab. Make sure at least one squadron is configured there. If you just imported a wing config, reload the page. A warning toast appears at the bottom of the screen to flag the issue.</div>
</div>

{shot("17", "Warning toast at the bottom of the screen: missing squadron alert", "Warning toast &mdash; missing squadron", wide=True)}

<div class="faq-entry">
  <div class="faq-q">The PDF has blank pages inserted between sections.</div>
  <div class="faq-a">This happens when a section overflows the A4 page height. In Chrome (<kbd>Ctrl+P</kbd>), verify that margins are set to &ldquo;None&rdquo; and scale to 100%. If it persists, shorten the content slightly &mdash; an overly long context paragraph or an objective list with too many items.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">What size should logos be?</div>
  <div class="faq-a">Transparent PNG, 400&times;400&nbsp;px or larger, under 200&nbsp;KB where possible. The app scales automatically, but small logos will appear blurry when printed. Avoid JPEG &mdash; compression artifacts are visible on the kraft background.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">Can I use the app on multiple PCs with the same config?</div>
  <div class="faq-a">Yes. Copy the HTML file to the other PC. Export your wing config from the first PC (<kbd>&#128228;&nbsp;Exporter config</kbd>) and import it on the second (<kbd>&#128229;&nbsp;Importer config</kbd>). Same workflow for in-progress briefings &mdash; JSON export on one PC, import on the other.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">The kraft background does not appear in the PDF.</div>
  <div class="faq-a">In Chrome&rsquo;s print dialog, enable <strong>&ldquo;Background graphics&rdquo;</strong>. Chrome disables backgrounds by default to save ink &mdash; you need to re-enable it manually each time you print.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">Can we fill in the briefing as a team at the same time?</div>
  <div class="faq-a">No &mdash; the app is designed for local, single-author use. The collaborative workflow is: one author prepares, exports the JSON, shares it on Discord or Drive, and the others load it for review.</div>
</div>

<h2 class="subsec" style="margin-top:32px">General Best Practices</h2>
<ul>
  <li><strong>Prepare early.</strong> A briefing done the evening before is one you have time to review and correct.</li>
  <li><strong>Keep a template JSON.</strong> A briefing with the wing configured and common radios pre-set &mdash; reload it at the start of each mission and save ten minutes.</li>
  <li><strong>Use consistent file naming.</strong> <code>OPNAME_YYYYMMDD.json</code> will save you when searching your archives six months from now.</li>
  <li><strong>Include the wing config when sharing.</strong> If you send a briefing JSON to someone with a different wing config loaded, the squadrons will not display correctly.</li>
</ul>

</div>

<!-- § 7 APPENDIX -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">07</span> Appendix &mdash; Credits and Licenses</h1>

<h2 class="subsec">Application</h2>
<p>The <strong>DCS World Briefing Generator</strong> is a community tool developed for DCS World virtual wings. It is freely distributed for personal and community use within virtual wings.</p>

<h2 class="subsec">Embedded Typefaces</h2>
<table class="ud-table">
  <thead><tr><th>Font</th><th>Usage</th><th>License</th></tr></thead>
  <tbody>
    <tr><td>Stardos Stencil</td><td>Titles, section headers, branding</td><td>Open Font License (OFL)</td></tr>
    <tr><td>Special Elite</td><td>Application body text (typewriter style)</td><td>Apache License 2.0</td></tr>
  </tbody>
</table>

<h2 class="subsec">DCS World</h2>
<p>DCS World is a product of <strong>Eagle Dynamics SA</strong>. Aircraft names, theater names, and all DCS World-related elements are the property of their respective rights holders. This tool makes no claim to any of them.</p>

<h2 class="subsec">This Guide</h2>
<p>Distributed with the application, in the same spirit: free use, non-commercial, for the community.</p>

<p style="margin-top:48px; text-align:center; font-family:var(--f-stencil); letter-spacing:3px; color:var(--khaki); font-size:13pt;">&#9670; GOOD HUNTING &#9670;</p>
</div>

</body>
</html>"""
OUTPUT = "DCS_World_Briefing_Generator_User_Guide_EN.html"
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(HTML)

size_kb = os.path.getsize(OUTPUT) // 1024
print(f"OK: {OUTPUT} generated ({size_kb} KB)")
print("  -> Open in Chrome, Ctrl+P to generate the PDF.")
