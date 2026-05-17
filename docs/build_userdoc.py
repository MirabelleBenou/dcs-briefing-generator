#!/usr/bin/env python3
"""
build_userdoc.py — Génère DCS_World_Briefing_Generator_User_Guide_FR.html
Documentation utilisateur du DCS World Briefing Generator.

Usage :
    python3 build_userdoc.py

Produit : DCS_World_Briefing_Generator_User_Guide_FR.html (autonome, imprimable en PDF via Chrome Ctrl+P)
"""

import json, os
from datetime import date

VERSION   = "1.1"
BUILD_DATE = date.today().strftime("%d/%m/%Y")

# ── Fonts ─────────────────────────────────────────────────────────────────────
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
        print(f"✓ Fonts chargées depuis {path}")
        break

if not FONT_FACE:
    FONT_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Stardos+Stencil:wght@400;700&family=Special+Elite&display=swap">'
    print("⚠ assets.json introuvable — Google Fonts CDN utilisé")

# ── CSS ───────────────────────────────────────────────────────────────────────
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

# ── Helpers ───────────────────────────────────────────────────────────────────
# Les captures d'écran sont hébergées sur GitHub Pages, pas embarquées dans le HTML.
# Pour ajouter une nouvelle capture : il suffit d'uploader shot_NN.png dans le dossier
# docs/screenshots/ du repo. Le HTML pointe directement dessus. Si l'image n'existe
# pas (404), un placeholder visuel est automatiquement injecté par JavaScript.
SHOTS_BASE_URL = "https://mirabellebenou.github.io/dcs-briefing-generator/docs/screenshots"

def _html_escape(s):
    """Échappe les caractères HTML dans une chaîne pour usage dans un attribut."""
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
                  .replace("<", "&lt;").replace(">", "&gt;"))

def shot(num, desc, caption, dims="", wide=False):
    _key = int(num) if str(num).isdigit() else 0
    _cls = "ud-screenshot ud-wide" if wide else "ud-screenshot"
    url = f"{SHOTS_BASE_URL}/shot_{_key:02d}.png"
    # Échappement pour les data-attributes et l'alt
    _esc_desc = _html_escape(desc)
    _esc_caption = _html_escape(caption)
    _esc_dims = _html_escape(dims)
    return (
        f'<figure class="{_cls}" data-shot="{num}"'
        f' data-desc="{_esc_desc}" data-caption="{_esc_caption}" data-dims="{_esc_dims}">\n'
        f'  <a class="ud-shot-link" href="{url}" target="_blank" rel="noopener" title="Cliquer pour agrandir">\n'
        f'    <img src="{url}" alt="{_esc_caption}" loading="lazy"'
        f' onerror="window.shotFallback&amp;&amp;window.shotFallback(this)">\n'
        f'    <span class="ud-zoom-icon" aria-hidden="true">⤢</span>\n'
        f'  </a>\n'
        f'  <figcaption>{caption}</figcaption>\n'
        '</figure>'
    )

def tip(t):   return f'<aside class="ud-tip"><span class="ud-ico">☞</span><div>{t}</div></aside>'
def warn(t):  return f'<aside class="ud-warn"><span class="ud-ico">⚠</span><div>{t}</div></aside>'
def admin(t): return f'<aside class="ud-admin"><span class="ud-ico">⚙</span><div>{t}</div></aside>'

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DCS World Briefing Generator — Guide utilisateur v{VERSION}</title>
{FONT_LINK}
<style>{CSS}</style>
</head>
<body>
<script>
/* Fallback navigateur : si une image shot_NN.png n'existe pas (404),
   on remplace le lien cliquable par un placeholder visuel. */
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
  ph.textContent = '[CAPTURE ' + num + ' : ' + desc + dimsText + ']';
  fig.classList.add('ud-placeholder');
  if (link && link.parentNode) {{
    link.parentNode.replaceChild(ph, link);
  }}
}};
</script>

<!-- COUVERTURE -->
<div class="cover">
  <div class="cover-badge">DOCUMENT DE RÉFÉRENCE // POUR PILOTES &amp; WING ADMINS</div>
  <div class="cover-title">DCS World<br>Briefing Generator</div>
  <div class="cover-sub">Guide Utilisateur</div>
  <div class="cover-divider"></div>
  <div class="cover-meta">
    Version {VERSION}<br>
    Édition du {BUILD_DATE}<br>
    <br>
    Imprimer en PDF → Chrome <kbd>Ctrl+P</kbd>
  </div>
  <div class="cover-stamp">V{VERSION} — {BUILD_DATE}</div>
</div>

<!-- TABLE DES MATIÈRES -->
<div class="toc-page">
  <div class="toc-title">Table des matières</div>

  <div class="toc-entry toc-h1"><span>1. Premier démarrage</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>1.1 Ouvrir l'application</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>1.2 Découverte de l'interface</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>1.3 Mode édition et mode aperçu</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>2. Créer un briefing complet</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.1 Métadonnées — onglet ⚙</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.2 Couverture — onglet ◉</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.3 Situation tactique — onglet ▣ SITAC</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.4 Aperçu mission — onglet ✈</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.5 Plan radio — onglet 📻</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.6 Missions individuelles — onglet ⊕</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.7 Équipage — onglet 👤</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.8 Charts — onglet 🗺</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>2.9 Annexes libres — onglet 📎</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>3. Sauvegarder et reprendre un briefing</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.1 La sauvegarde automatique</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.2 Exporter en JSON</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.3 Importer un briefing existant</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>3.4 Recommencer à zéro</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>4. Exporter en PDF</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.1 Vérification en mode aperçu</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.2 Exporter en PDF (Windows / macOS)</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.3 Exporter en PDF depuis Android</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.4 Export PNG kneeboard</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>4.5 Bonnes pratiques</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>5. Configuration du wing</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.1 Qu'est-ce qu'un « wing config » ?</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.2 Modifier l'identité du wing</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.3 Gérer les escadrons</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.4 Charger des logos</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h2"><span>5.5 Exporter, importer, réinitialiser</span><span class="toc-dots"></span></div>

  <div class="toc-entry toc-h1"><span>6. FAQ et astuces</span><span class="toc-dots"></span></div>
  <div class="toc-entry toc-h1"><span>7. Annexe — crédits et licences</span><span class="toc-dots"></span></div>
</div>

<!-- § 1 PREMIER DÉMARRAGE -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">01</span> Premier démarrage</h1>

<h2 class="subsec">1.1 Ouvrir l'application</h2>

<p>Pas d'installation, pas de serveur, pas de compte. Vous double-cliquez sur <code>DCS_World_Briefing_Generator.html</code> et c'est parti. L'application tourne entièrement dans votre navigateur, hors ligne.</p>

<ul>
  <li><strong>Navigateur recommandé : Chrome (ou un dérivé Chromium).</strong> C'est là que l'impression PDF est la plus propre, et c'est là que l'app a été conçue.</li>
  <li>Firefox et Safari fonctionnent pour remplir les formulaires, mais peuvent se comporter différemment à l'impression.</li>
  <li>Sur tablette Android, copiez le fichier HTML sur votre appareil (câble, Drive, mail…) et ouvrez-le avec Chrome.</li>
</ul>

{tip("Gardez le fichier HTML dans un dossier fixe sur votre PC — vos données de briefing sont liées à l'emplacement du fichier via le stockage du navigateur.")}

<h2 class="subsec">1.2 Découverte de l'interface</h2>

<p>Dès l'ouverture, vous êtes en mode <strong>édition</strong>. L'interface se divise en deux zones simples :</p>

{shot("01", "barre d'outils complète mode édition : Sauver / Charger / Imprimer / Reset visibles", "La barre d'outils en haut de l'écran", wide=True)}

<p>En haut, la <strong>barre d'outils</strong> — avec le nom de votre wing à gauche et les boutons principaux à droite. En dessous, les <strong>onglets</strong> qui donnent accès à chaque section du briefing.</p>

{shot("02", "vue éditeur globale PC : toolbar + onglets + formulaire ouvert, données de démonstration", "L'interface éditeur sur écran large")}

<p>Sur tablette, les onglets basculent en bas de l'écran, accessibles au pouce :</p>

{shot("03", "vue éditeur sur tablette Android : onglets iconiques en bas de l'écran", "Sur tablette — les onglets passent en bas")}

<p>Les onglets disponibles, dans l'ordre :</p>

<table class="ud-table">
  <thead><tr><th>Icône</th><th>Nom</th><th>Ce qu'on y fait</th></tr></thead>
  <tbody>
    <tr><td>⚙</td><td>Méta</td><td>Date, classification, référence du document</td></tr>
    <tr><td>◉</td><td>Couv.</td><td>Titre de l'opération, contexte, carte de couverture</td></tr>
    <tr><td>▣</td><td>SITAC</td><td>Situation tactique, météo, points de situation</td></tr>
    <tr><td>✈</td><td>Mission</td><td>Objectifs, bases, menaces (aperçu mission)</td></tr>
    <tr><td>📻</td><td>Radio</td><td>Fréquences communes et plans radio par appareil</td></tr>
    <tr><td>⊕</td><td>Missions</td><td>Fiches de mission individuelles par pilote</td></tr>
    <tr><td>👤</td><td>Équipage</td><td>Ordre de bataille — groupes et pilotes</td></tr>
    <tr><td>🗺</td><td>Charts</td><td>Charts d'aéroport (approche, taxiway, communication…)</td></tr>
    <tr><td>📎</td><td>Annexes libres</td><td>Contenu illustré libre en fin de briefing</td></tr>
    <tr><td>🛡</td><td>Wing</td><td>Configuration du wing (section admin)</td></tr>
    <tr><td>◈</td><td>Aperçu</td><td>Rendu final imprimable du briefing</td></tr>
  </tbody>
</table>

<h2 class="subsec">1.3 Mode édition et mode aperçu</h2>

<p>L'app a deux modes, et on passe de l'un à l'autre en un clic :</p>

<ul>
  <li><strong>Mode édition</strong> — vous remplissez les formulaires. C'est là que se passe tout le travail.</li>
  <li><strong>Mode aperçu</strong> — le briefing s'affiche en format A4, exactement comme il s'imprimera. Plus de formulaires, juste le rendu final.</li>
</ul>

<p>Pour basculer : cliquer directement sur l'onglet <strong>◈ Aperçu</strong>.</p>

{shot("04", "mode aperçu actif : page de couverture rendue A4 style kraft militaire, sans interface édition", "Mode aperçu — ce qu'on retrouvera dans le PDF final")}

{tip("Jetez un œil à l'aperçu régulièrement pendant que vous travaillez. C'est le meilleur moyen de voir si le briefing « rend » bien avant d'imprimer.")}

</div>

<!-- § 2 CRÉER UN BRIEFING COMPLET -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">02</span> Créer un briefing complet</h1>

<p>On va parcourir les onglets dans l'ordre, de gauche à droite. C'est comme ça que le briefing se construit, et c'est l'ordre le plus logique pour ne rien oublier.</p>

<h2 class="subsec">2.1 Métadonnées — onglet ⚙</h2>

<p>Ce sont les données d'en-tête qui s'affichent en pied de page sur chaque feuille imprimée. Quelques champs, vite remplis.</p>

{shot("05", "onglet Métadonnées rempli : Opération, Mission code, Date, Classification, Référence visibles", "Onglet ⚙ Méta")}

<ul>
  <li><strong>Opération</strong> — le nom de l'opération (ex. « IRON DAWN »).</li>
  <li><strong>Mission code</strong> — un code court pour identifier la sortie (ex. « ALPHA-7 »).</li>
  <li><strong>Date mission</strong> — en format libre (ex. « 14 JAN 2025 / ZULU »).</li>
  <li><strong>Classification</strong> — le niveau de classification fictif affiché sur les pages : CONFIDENTIEL DÉFENSE, SECRET DÉFENSE, TRÈS SECRET, NON CLASSIFIÉ, NATO RESTRICTED, NATO SECRET.</li>
  <li><strong>Référence document</strong> — numéro de document ou référence interne (ex. « 4VEAW/OPS/2025-001 »).</li>
</ul>

{tip("Ça prend deux minutes et ça donne un côté pro immédiat au briefing. Ne sautez pas cette étape.")}

<h2 class="subsec">2.2 Couverture — onglet ◉</h2>

<p>La première page du briefing imprimé. C'est ici que vous posez le décor pour tout ce qui suit.</p>

{shot("06", "onglet Couverture rempli avec carte d'opération chargée, titre et texte de contexte visibles", "Onglet ◉ Couv.")}

<ul>
  <li><strong>Titre opération</strong> — s'affiche en grand stencil sur la couverture. Courts et percutants, c'est mieux.</li>
  <li><strong>Récit / Contexte</strong> — paragraphe libre qui donne la situation aux pilotes. C'est le texte qu'ils liront avant de décoller.</li>
  <li><strong>Carte d'opération</strong> — glissez-déposez une image, ou cliquez sur la zone pour en choisir une. PNG, JPEG, WEBP — tout passe.</li>
</ul>

{tip("Un screenshot de la vue F10 DCS, recadré et annoté en 30 secondes dans Paint, fait parfaitement l'affaire. Visez 1200 px de large pour une belle qualité à l'impression.")}

<h2 class="subsec">2.3 Situation tactique — onglet ▣ SITAC</h2>

<p>Le résumé de la situation au moment de la mission — où en sont les forces, quel est le contexte, quel temps il fait.</p>

<ul>
  <li><strong>Date SITAC affichée</strong> — peut être différente de la date de la mission si la SITAC date de la veille.</li>
  <li><strong>Points de situation</strong> — une liste de points courts (bouton + Ajouter un point). Positions ennemies, zones interdites, alertes rouges…</li>
  <li><strong>METAR</strong> — météo au format METAR ou en texte libre (« Plafond 3000 ft, vent 270/15 kt »).</li>
  <li><strong>Carte SITAC</strong> — optionnel : une image annotée avec les positions amies/ennemies. Si vous n'en avez pas, la page reste propre.</li>
</ul>

<h2 class="subsec">2.4 Aperçu mission — onglet ✈</h2>

<p>Le corps opérationnel de la mission : ce qu'on doit faire, où on se pose, et ce qui peut nous tirer dessus.</p>

<ul>
  <li><strong>Objectifs principaux</strong> — une liste (+ Ajouter un objectif). Une ligne, une idée, c'est le bon format.</li>
  <li><strong>FARP &amp; Aéroports</strong> — les bases disponibles avec leur statut (amie, neutre, hostile).</li>
  <li><strong>Menaces</strong> — cases par type (Chars, APC, AAA, SAM) avec niveaux ou descriptions courtes.</li>
  <li><strong>Note menaces</strong> — zone libre si vous avez des infos sur des SAM actifs, des zones à éviter, ou autre chose qui ne rentre pas dans les cases.</li>
</ul>

<h2 class="subsec">2.5 Plan radio — onglet 📻</h2>

<p>Toutes les fréquences au même endroit. Cet onglet se divise en deux parties :</p>

{shot("09", "onglet Plan radio : items radio communs renseignés + un appareil avec ses canaux configurés", "Onglet 📻 Radio")}

<ul>
  <li><strong>Items radio</strong> (max 6) — les fréquences communes à tout le monde : ATC principal, fréquence de mission, urgence… Elles s'affichent sur la page 3 du briefing imprimé.</li>
  <li><strong>Plans radio par appareil</strong> — pour chaque avion utilisé (F-16C, F/A-18C, Mi-8…), vous définissez les radios et leurs canaux. Vous pouvez aussi charger une <strong>image</strong> (screenshot de la radio préconfigurée en jeu) qui remplace la table générée.</li>
</ul>

{tip("Définissez d'abord les items radio communs, puis assignez-les aux canaux par appareil. La cohérence entre les pages s'en trouve garantie.")}

<h2 class="subsec">2.6 Missions individuelles — onglet ⊕</h2>

<p>C'est souvent la section la plus longue à remplir — et la plus personnalisée. Chaque pilote ou équipage peut avoir sa propre fiche.</p>

{shot("07", "onglet Missions : une fiche mission ouverte avec pilote, escadron, appareil et notes visibles", "Onglet ⊕ Missions — une fiche ouverte")}

<ul>
  <li>Les boutons <kbd>◄</kbd> <kbd>►</kbd> naviguent entre les missions, <kbd>+</kbd> en crée une, <kbd>⎘</kbd> duplique, <kbd>↑</kbd> <kbd>↓</kbd> réordonnent, <kbd>×</kbd> supprime.</li>
  <li>Chaque mission : pilote, escadron (dans la liste du wing), appareil, emport, waypoints, notes libres.</li>
</ul>

{shot("08", "sélecteur d'escadron déroulé : liste des escadrons du wing (541-TFS / DUFF, 329-Mira / ARROW…)", "Le sélecteur d'escadron")}

{tip("Le sélecteur liste automatiquement les escadrons configurés dans l'onglet 🛡 Wing. S'il est vide, c'est que le wing n'a pas encore d'escadrons — direction § 5 pour ça.")}

{warn("Si un escadron est absent de la liste, les missions qui y font référence restent affichables mais sans branding d'escadron. Pas de crash, juste un champ vide.")}

<h2 class="subsec">2.7 Équipage — onglet 👤</h2>

<p>L'onglet Équipage génère une page d'ordre de bataille dans le briefing — mais seulement si vous y mettez des pilotes. Si vous laissez ça vide, pas de page équipage, pas de problème.</p>

<ul>
  <li>Organisez les pilotes par <strong>groupes</strong> (section, escadron, vol…).</li>
  <li>Chaque groupe contient les pilotes avec leur indicatif, rang, et notes éventuelles.</li>
</ul>

<h2 class="subsec">2.8 Charts — onglet 🗺</h2>

<p>L'onglet Charts permet d'ajouter des cartes aéroportuaires (charts) au briefing. Ces charts sont typiquement des PDF ou images d'approche, taxiway, communication, etc., téléchargées depuis des sources comme Chartfox ou les sites officiels.</p>

<p>Pour chaque chart, vous renseignez :</p>
<ul>
  <li>Un <strong>titre</strong> (ex : « LFMN — ILS RWY 04R »)</li>
  <li>Une <strong>image</strong> (PNG ou JPEG) chargée par glisser-déposer ou via le bouton de sélection</li>
  <li>Un <strong>commentaire</strong> facultatif pour annoter ou contextualiser la chart</li>
</ul>

<p>Le bouton <code>+ Ajouter une chart</code> permet d'en ajouter autant que nécessaire. Les charts apparaissent dans le briefing final dans l'ordre où vous les avez saisies.</p>

{shot("18", "onglet Charts : liste de charts avec bouton « + Ajouter une chart » visible", "L'onglet Charts")}

{tip("Optimisez vos images de charts avant de les charger. Un PNG de 4K en 8 Mo n'apportera rien de plus visuellement qu'un PNG de 1500 px à 500 Ko, et alourdira inutilement le briefing exporté.")}

<h2 class="subsec">2.9 Annexes libres — onglet 📎</h2>

<p>L'onglet Annexes libres remplit le rôle qu'avait l'onglet Annexes en v2.0.0 : il permet d'ajouter du contenu illustré libre en fin de briefing — schémas, notes, photos de référence, OOB ennemi, etc.</p>

<p>Chaque annexe combine :</p>
<ul>
  <li>Un <strong>titre</strong> obligatoire</li>
  <li>Une <strong>image</strong> facultative (chargée par glisser-déposer)</li>
  <li>Une <strong>zone de commentaire</strong> textuelle de longueur libre</li>
</ul>

{shot("19", "onglet Annexes libres : liste avec champ titre, zone image et zone de commentaire pour une annexe", "L'onglet Annexes libres")}

{admin("Les annexes apparaissent dans le briefing final dans l'ordre où vous les avez saisies. Pour réordonner, utilisez les flèches haut/bas à côté de chaque annexe.")}

</div>

<!-- § 3 SAUVEGARDER -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">03</span> Sauvegarder et reprendre un briefing</h1>

<h2 class="subsec">3.1 La sauvegarde automatique</h2>

<p>Bonne nouvelle : vous n'avez rien à faire. L'app sauvegarde en permanence votre briefing en cours dans le stockage local du navigateur (localStorage). Fermez l'onglet, éteignez le PC, revenez le lendemain — votre travail est là.</p>

{warn("Cette sauvegarde automatique est liée au <strong>navigateur</strong> et à l'<strong>emplacement du fichier HTML</strong> sur votre disque. Si vous déplacez ou renommez le fichier HTML, ou si vous effacez les données du navigateur, le briefing en cours part avec. Pour une vraie sauvegarde durable, utilisez l'export JSON.")}

<h2 class="subsec">3.2 Exporter un briefing en JSON</h2>

<p>L'export JSON c'est la sauvegarde permanente — un fichier que vous pouvez archiver, envoyer à un camarade, ou recharger dans six mois.</p>

{shot("11", "zoom sur le bouton Sauver dans la toolbar, curseur positionné dessus", "Le bouton Sauver", wide=True)}

<ul>
  <li>Cliquez sur <kbd>Sauver</kbd> dans la barre d'outils.</li>
  <li>Un fichier <code>briefing_OPERATION_DATE.json</code> est téléchargé automatiquement.</li>
  <li>Gardez-le quelque part de sûr — c'est votre seule copie portable du briefing.</li>
</ul>

{tip("Bonne habitude : exportez en JSON dès que le briefing commence à avoir de la substance. Une convention de nommage simple — <code>OPNAME_YYYYMMDD.json</code> — vous sauvera la mise quand vous chercherez dans vos archives.")}

<h2 class="subsec">3.3 Importer un briefing existant</h2>

<p>Vous reprenez un briefing d'une session précédente, ou un camarade vous envoie le sien :</p>

<ul>
  <li>Cliquez sur <kbd>Charger</kbd> dans la barre d'outils.</li>
  <li>Sélectionnez le fichier <code>.json</code> dans l'explorateur.</li>
  <li>Le briefing se charge immédiatement.</li>
</ul>

{warn("Le chargement <strong>remplace</strong> le briefing en cours, sans confirmation supplémentaire. Si vous avez du travail non sauvegardé, exportez-le en JSON d'abord.")}

<h2 class="subsec">3.4 Recommencer à zéro</h2>

<ul>
  <li>Cliquez sur <kbd>Reset</kbd> dans la barre d'outils.</li>
  <li>Une confirmation vous est demandée — c'est le seul garde-fou.</li>
  <li>Tout le briefing est effacé, y compris la sauvegarde auto dans le navigateur.</li>
</ul>

{tip("Si vous avez un briefing « template » que vous réutilisez souvent (structure fixe, wing configuré, radios communes), exportez-le en JSON et rechargez-le au début de chaque nouvelle mission plutôt que de repartir de zéro.")}

</div>

<!-- § 4 EXPORTER EN PDF -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">04</span> Exporter en PDF</h1>

<h2 class="subsec">4.1 Vérification en mode aperçu</h2>

<p>Avant d'imprimer, jetez un œil en <strong>mode aperçu</strong> — onglet ◈. Vérifiez rapidement que :</p>
<ul>
  <li>La couverture affiche bien le titre et la carte.</li>
  <li>Les pages de contenu ne sont pas tronquées.</li>
  <li>Toutes les missions individuelles sont présentes.</li>
  <li>Les images de cartes et de charts sont lisibles.</li>
</ul>

{tip("Ce que vous voyez en aperçu est exactement ce qui sera dans le PDF final. Mieux vaut repérer les problèmes maintenant qu'après l'export.")}

<h2 class="subsec">4.2 Exporter en PDF (Windows / macOS)</h2>

<p>Tout se passe dans Chrome, sans logiciel tiers. Le bouton <kbd>Imprimer</kbd> bascule automatiquement en mode aperçu.</p>

<ol>
  <li>Appuyez sur <kbd>Ctrl</kbd>+<kbd>P</kbd> (Windows/Linux) ou <kbd>⌘</kbd>+<kbd>P</kbd> (macOS).</li>
  <li>Sélectionnez <strong>« Enregistrer en PDF »</strong> comme destination.</li>
  <li>Réglez les options :</li>
</ol>

{shot("12", "boîte dialogue impression Chrome : 'Enregistrer en PDF' sélectionné, options Marges et Arrière-plans visibles", "La boîte de dialogue d'impression Chrome")}

<table class="ud-table">
  <thead><tr><th>Option</th><th>Valeur recommandée</th></tr></thead>
  <tbody>
    <tr><td>Format</td><td>A4</td></tr>
    <tr><td>Orientation</td><td>Portrait</td></tr>
    <tr><td>Marges</td><td>Aucune (l'app gère ses propres marges)</td></tr>
    <tr><td>Mise à l'échelle</td><td>100 %</td></tr>
    <tr><td>Graphiques d'arrière-plan</td><td>✓ Activé — obligatoire pour le fond kraft</td></tr>
  </tbody>
</table>

{warn("Si vous oubliez d'activer <strong>« Graphiques d'arrière-plan »</strong>, le fond kraft devient blanc et les en-têtes perdent leur couleur. Le contenu reste imprimable, mais l'effet visuel disparaît.")}

<h2 class="subsec">4.3 Exporter en PDF depuis Android</h2>

<p>Sur Android avec Chrome, le bouton <kbd>Imprimer</kbd> ouvre directement le système d'export natif Android ou le menu de partage (Web Share API) :</p>

<ul>
  <li>Touchez <kbd>Imprimer</kbd> dans la toolbar.</li>
  <li>Sélectionnez <strong>« Enregistrer en PDF »</strong> comme destination.</li>
  <li>Mêmes réglages qu'en version PC (échelle 100 %, arrière-plans activés, format A4).</li>
</ul>

{tip("Sur Android, si l'aperçu d'impression semble tronqué, vérifiez que l'échelle est à 100 % et non « Ajuster à la page » — Chrome Android peut proposer les deux.")}

<h2 class="subsec">4.4 Export PNG kneeboard</h2>

<p>En plus de l'export PDF classique, le générateur produit un export PNG optimisé pour les <strong>kneeboards</strong> de DCS — les blocs-notes virtuels affichés en jeu lors du vol.</p>

<p>Pour exporter en PNG kneeboard :</p>
<ol>
  <li>Cliquer sur le bouton <code>Imprimer</code> dans la toolbar</li>
  <li>Dans la modale d'export, choisir l'option <strong>PNG kneeboard</strong> (par défaut : PDF)</li>
  <li>Cocher les pages à exporter dans la liste proposée (toutes par défaut)</li>
  <li>Cliquer sur <code>Exporter</code></li>
</ol>

<p>Un fichier ZIP est généré, contenant un PNG par page sélectionnée. Chaque PNG est dimensionné aux ratios kneeboard DCS standard.</p>

{shot("20", "modale d'export du briefing : choix entre PDF et PNG kneeboard, sélecteur de pages à cocher", "La modale d'export multi-format")}

{tip("Vous pouvez décocher les pages non nécessaires en vol (page de garde, annexes administratives) pour n'avoir que l'essentiel dans le kneeboard et économiser de l'espace mental en cockpit.")}

<h2 class="subsec">4.5 Bonnes pratiques</h2>

<ul>
  <li><strong>Préparez tôt.</strong> Un briefing fait la veille, c'est un briefing qu'on a le temps de relire et de corriger.</li>
  <li><strong>Gardez le PDF généré</strong> après export — c'est l'archive de la mission, et ça peut servir si un camarade a raté le briefing oral.</li>
  <li><strong>Partagez le JSON, pas le PDF</strong>, si un autre pilote veut modifier le briefing.</li>
</ul>

</div>

<!-- § 5 CONFIGURATION WING -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">05</span> Configuration du wing</h1>

{admin("Cette section s'adresse aux <strong>wing admins</strong> — ceux qui configurent l'application pour toute l'équipe. Si votre admin a déjà fait ça, vous pouvez aller directement à la § 6.")}

<h2 class="subsec">5.1 Qu'est-ce qu'un « wing config » ?</h2>

<p>La configuration du wing, c'est l'ensemble des données qui personnalisent l'app pour votre wing virtuel. Concrètement :</p>

<ul>
  <li>Le <strong>nom et l'identité</strong> du wing — ce qui s'affiche dans la toolbar, les en-têtes, les pieds de page.</li>
  <li>La liste des <strong>escadrons</strong> avec leurs noms, indicatifs et logos.</li>
  <li>Le <strong>logo wing principal</strong> qui apparaît sur la couverture.</li>
  <li>Le <strong>tampon HQ</strong> affiché sur la couverture.</li>
</ul>

<p>Une fois configurée, cette config s'applique à tous les briefings créés avec cette installation. Elle s'exporte en JSON pour être distribuée à tous les pilotes du wing en un fichier.</p>

{admin("La config wing et le briefing sont deux couches indépendantes. Reset du briefing ne touche pas à la config wing. Changer de wing ne touche pas au briefing en cours.")}

<h2 class="subsec">5.2 Modifier l'identité du wing</h2>

{shot("13", "onglet Wing complet : section Identité du wing avec nom court, identifiant, nom complet, logo chargé", "Onglet 🛡 Wing")}

<p>Dans l'onglet <strong>🛡 Wing</strong>, section « Identité du wing » :</p>

<ul>
  <li><strong>Nom court</strong> — s'affiche dans la toolbar (ex. « 4th VEAW »). Gardez-le sous 10 caractères.</li>
  <li><strong>Identifiant</strong> — clé technique sans espace ni slash (ex. « 4th-veaw »). Utilisé en interne.</li>
  <li><strong>Nom complet</strong> — nom complet du wing (ex. « 4th Virtual Expeditionary Air Wing »).</li>
  <li><strong>Titre de l'application</strong> — texte dans l'onglet du navigateur.</li>
  <li><strong>Tampon HQ</strong> — texte affiché comme tampon sur la couverture (ex. « HQ VEAW // CLASSIFIED »).</li>
</ul>

<h2 class="subsec">5.3 Gérer les escadrons</h2>

<p>Les escadrons configurés ici alimentent directement le sélecteur dans l'onglet ⊕ Missions.</p>

{shot("14", "carte d'escadron ouverte en édition : champs Nom, Indicatif, Logo visibles", "Édition d'une fiche escadron")}

<ul>
  <li>Cliquez sur <kbd>+ Ajouter un escadron</kbd> pour créer une nouvelle unité.</li>
  <li>Chaque escadron : <strong>nom</strong> (ex. « 541st Tactical Fighter Squadron »), <strong>indicatif</strong> (ex. « DUFF »), <strong>logo</strong> optionnel.</li>
  <li>Cliquez sur une carte existante pour la modifier ou la supprimer.</li>
</ul>

{warn("Supprimer un escadron ne modifie pas les missions qui y font déjà référence — elles conservent l'identifiant, mais le nom et le logo n'apparaîtront plus. À faire avant de distribuer un briefing final, pas après.")}

<h2 class="subsec">5.4 Charger des logos</h2>

{shot("15", "zone drag-drop d'un logo d'escadron avec indicateur de glisser-déposer actif", "Chargement d'un logo par glisser-déposer", wide=True)}

<ul>
  <li><strong>Logo wing principal</strong> — apparaît sur la couverture. Recommandé : PNG transparent, 400×400 px minimum, &lt; 200 Ko.</li>
  <li><strong>Logo d'escadron</strong> (un par escadron) — affiché sur les fiches de mission. Mêmes recommandations.</li>
</ul>

<p>Glissez-déposez l'image sur la zone, ou cliquez dessus pour ouvrir le sélecteur de fichiers.</p>

{tip("Les logos sont stockés en base64 dans la config. Des logos volumineux (>500 Ko) alourdissent le JSON exporté. Optimisez vos PNG avant de les charger — un logo de wing n'a pas besoin d'être en 4K.")}

<h2 class="subsec">5.5 Exporter, importer, réinitialiser</h2>

{shot("16", "boutons Import / Export / Reset en bas de l'onglet Wing avec taille de config affichée", "Boutons de gestion de la config wing", wide=True)}

<ul>
  <li><kbd>📥 Importer config</kbd> — charge un fichier JSON de configuration wing.</li>
  <li><kbd>📤 Exporter config</kbd> — télécharge la configuration actuelle en JSON.</li>
  <li><kbd>♻ Réinitialiser (4th VEAW)</kbd> — restaure la configuration d'exemple embarquée dans l'app.</li>
</ul>

{admin("Le workflow de distribution : <ol style='margin:6px 0 0 16px'><li>L'admin configure le wing dans l'app.</li><li>Il exporte la config via <kbd>📤 Exporter config</kbd>.</li><li>Il distribue le fichier JSON aux pilotes (Discord, mail, Drive…).</li><li>Chaque pilote importe via <kbd>📥 Importer config</kbd>.</li><li>Tout le monde voit les mêmes escadrons dans le sélecteur.</li></ol>")}

</div>

<!-- § 6 FAQ -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">06</span> FAQ et astuces</h1>

<div class="faq-entry">
  <div class="faq-q">J'ai fermé l'onglet par accident. Mon briefing est perdu ?</div>
  <div class="faq-a">Non. La sauvegarde automatique (localStorage) a tout gardé. Rouvrez simplement <code>DCS_World_Briefing_Generator.html</code> dans le même navigateur — votre travail est là. <em>Exception :</em> si vous avez vidé les données du navigateur ou déplacé le fichier HTML depuis, là c'est perdu. D'où l'export JSON régulier.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">Mon escadron n'apparaît pas dans le sélecteur de mission.</div>
  <div class="faq-a">Le sélecteur liste uniquement les escadrons définis dans l'onglet 🛡 Wing. Vérifiez qu'au moins un escadron y est configuré. Si vous venez d'importer une config wing, rechargez la page. Un toast d'avertissement apparaît parfois en bas de l'écran pour vous signaler le problème.</div>
</div>

{shot("17", "toast d'avertissement bas d'écran : 'Aucun escadron configuré dans le wing'", "Toast d'avertissement — escadrons absents", wide=True)}

<div class="faq-entry">
  <div class="faq-q">Le PDF a des pages blanches intercalées.</div>
  <div class="faq-a">Ça arrive quand une section dépasse la hauteur d'une page A4. Dans Chrome (<kbd>Ctrl+P</kbd>), vérifiez que les marges sont sur « Aucune » et l'échelle à 100 %. Si ça persiste, raccourcissez légèrement le contenu incriminé — un paragraphe de contexte trop long, une liste d'objectifs trop fournie.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">Quelle taille pour les logos ?</div>
  <div class="faq-a">PNG transparent, 400×400 px ou plus, moins de 200 Ko si possible. L'app redimensionne automatiquement, mais les petits logos seront flous à l'impression. Évitez les JPEG (artefacts visibles sur fond kraft).</div>
</div>

<div class="faq-entry">
  <div class="faq-q">Puis-je utiliser l'app sur plusieurs PC avec la même config ?</div>
  <div class="faq-a">Oui. Copiez le fichier HTML sur l'autre PC. Exportez votre config wing depuis le premier PC (<kbd>📤 Exporter config</kbd>) et importez-la sur le second (<kbd>📥 Importer config</kbd>). Idem pour les briefings en cours — export JSON sur un PC, import sur l'autre.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">Le fond kraft n'apparaît pas dans le PDF.</div>
  <div class="faq-a">Dans la boîte d'impression Chrome, activez <strong>« Graphiques d'arrière-plan »</strong>. Chrome désactive les backgrounds par défaut pour économiser l'encre — il faut le réactiver manuellement à chaque impression.</div>
</div>

<div class="faq-entry">
  <div class="faq-q">Peut-on faire le briefing à plusieurs en même temps ?</div>
  <div class="faq-a">Non — l'app est conçue pour un usage local, un seul rédacteur à la fois. Pour collaborer, la méthode est simple : un seul rédacteur prépare, exporte le JSON, le partage sur Discord ou Drive, et les autres le chargent pour consultation.</div>
</div>

<h2 class="subsec" style="margin-top:32px">Bonnes pratiques générales</h2>
<ul>
  <li><strong>Préparez tôt.</strong> Un briefing fait la veille, c'est un briefing qu'on a le temps de relire et de corriger.</li>
  <li><strong>Gardez un template JSON.</strong> Un briefing avec juste le wing configuré et les radios communes — rechargez-le au début de chaque nouvelle mission, gagnez 10 minutes.</li>
  <li><strong>Nommez vos fichiers de façon cohérente.</strong> <code>OPNAME_YYYYMMDD.json</code> vous sauvera quand vous chercherez dans vos archives dans 6 mois.</li>
  <li><strong>Incluez la config wing dans vos partages.</strong> Si vous envoyez un briefing JSON à quelqu'un qui n'a pas la même config, les escadrons s'afficheront mal.</li>
</ul>

</div>

<!-- § 7 ANNEXE CRÉDITS -->
<div class="page">
<h1 class="sec-title"><span class="sec-num">07</span> Annexe — Crédits et licences</h1>

<h2 class="subsec">Application</h2>
<p>Le <strong>DCS World Briefing Generator</strong> est un outil développé pour la communauté DCS World francophone. Elle est distribuée librement pour un usage personnel et communautaire au sein des wings virtuels.</p>

<h2 class="subsec">Typographies embarquées</h2>
<table class="ud-table">
  <thead><tr><th>Police</th><th>Utilisation</th><th>Licence</th></tr></thead>
  <tbody>
    <tr><td>Stardos Stencil</td><td>Titres, en-têtes de section, branding</td><td>Open Font License (OFL)</td></tr>
    <tr><td>Special Elite</td><td>Corps de l'application (style machine à écrire)</td><td>Apache License 2.0</td></tr>
  </tbody>
</table>

<h2 class="subsec">DCS World</h2>
<p>DCS World est un produit d'<strong>Eagle Dynamics SA</strong>. Les noms d'appareils, de théâtres et tous les éléments relatifs à DCS World sont la propriété de leurs ayants droit respectifs. Cet outil n'en revendique aucun.</p>

<h2 class="subsec">Ce guide</h2>
<p>Distribué avec l'application, dans le même esprit : usage libre, non commercial, pour la communauté.</p>

<p style="margin-top:48px; text-align:center; font-family:var(--f-stencil); letter-spacing:3px; color:var(--khaki); font-size:13pt;">◆ BON VOL ◆</p>
</div>

</body>
</html>"""

OUTPUT = "DCS_World_Briefing_Generator_User_Guide_FR.html"
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(HTML)

size_kb = os.path.getsize(OUTPUT) // 1024
print(f"✓ {OUTPUT} généré ({size_kb} Ko)")
print("  → Ouvrez dans Chrome, Ctrl+P pour générer le PDF.")
