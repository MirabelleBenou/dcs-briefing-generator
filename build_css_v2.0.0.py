#!/usr/bin/env python3
"""Build the v2 KHR-26 Cold War briefing generator with tablet support."""

import json

with open('/home/claude/assets.json') as f:
    A = json.load(f)

CSS = r"""
/* ============================================
   COLD WAR BRIEFING GENERATOR v2 — KHR-26
   Tablet-ready, fonts embedded, offline-first
   ============================================ */

@font-face {
  font-family: 'Stardos Stencil';
  font-weight: 400;
  font-display: block;
  src: url('data:font/woff2;base64,__STARDOS_400__') format('woff2');
}
@font-face {
  font-family: 'Stardos Stencil';
  font-weight: 700;
  font-display: block;
  src: url('data:font/woff2;base64,__STARDOS_700__') format('woff2');
}
@font-face {
  font-family: 'Special Elite';
  font-weight: 400;
  font-display: block;
  src: url('data:font/woff2;base64,__SPECIAL_ELITE__') format('woff2');
}
@font-face {
  /* Phase X — étape C : Roboto Mono Regular pour les 2 thèmes modernes
     (subset latin, ~12 KB). Glyphes manquants du subset (░ ▮ ★ etc.)
     resolvent via fallback sur 'Courier New' / 'Courier' / monospace. */
  font-family: 'Roboto Mono';
  font-weight: 400;
  font-display: block;
  src: url('data:font/woff2;base64,__ROBOTO_MONO_400__') format('woff2');
}

:root {
  /* Typography stack — partagée par tous les thèmes (la phase X — étape C
     redéfinira --f-typewriter sur les thèmes modernes). */
  --f-stencil: 'Stardos Stencil', 'Impact', 'Arial Narrow Bold', sans-serif;
  --f-typewriter: 'Special Elite', 'Courier New', 'Courier', monospace;
  --f-condensed: 'Impact', 'Arial Narrow', 'Helvetica Condensed', sans-serif;
  --f-mono: ui-monospace, 'SF Mono', 'Menlo', 'Consolas', monospace;

  /* Variables sémantiques constantes sur tous les thèmes
     (cf. phase X § 1.5 et Q1/Q2 de validation utilisateur). */
  --amber:        #c0892a;  /* accent UI : onglets actifs, branding, warn */
  --amber-dark:   #8a5e15;
  --green-radar:  #4f6b3a;  /* threat chips et accents tactiques sémantiques */
}

/* ============================================
   THÈMES — phase X
   Bascule via <body data-theme="..."> :
     cw-nato (défaut) | cw-soviet | modern-nato | modern-east
   Le JS de l'étape E posera l'attribut au démarrage via loadTheme().
   ============================================ */

/* --- Thème : Cold War OTAN (défaut, valeurs originales préservées) --- */
body[data-theme="cw-nato"] {
  --paper:        #d8c9a5;
  --paper-light:  #e3d6b5;
  --paper-dark:   #b8a77c;
  --paper-edge:   #8a7a52;
  --page-bg:      #d6c7a3;  /* fond .page sous la texture kraft */
  --ink:          #1f1c16;
  --ink-faded:    #463f30;
  --olive:        #4a5230;
  --olive-dark:   #2c321e;
  --olive-deep:   #1a1e10;
  --khaki:        #807454;
  --khaki-light:  #a89a72;
  --rust:         #7a3a20;
  --red-stamp:    #a83524;
  --red-faded:    #c4574a;
  --kraft-bg: url('data:image/svg+xml;base64,__KRAFT_SVG_NATO__');
}

/* --- Thème : Cold War Soviétique --- */
body[data-theme="cw-soviet"] {
  --paper:        #d8c479;  /* ocre chaud */
  --paper-light:  #e8d690;
  --paper-dark:   #b8a64a;
  --paper-edge:   #8a7a30;
  --page-bg:      #d4c075;
  --ink:          #1f1c16;
  --ink-faded:    #463f30;
  --olive:        #2a3a5a;  /* bleu nuit (accent secondaire) */
  --olive-dark:   #1a2540;
  --olive-deep:   #0e1830;
  --khaki:        #3a4a2e;  /* vert armée russe (accent principal) */
  --khaki-light:  #5a6a48;
  --rust:         #5e1414;
  --red-stamp:    #841e1e;  /* rouge bordeaux */
  --red-faded:    #a04040;
  --kraft-bg: url('data:image/svg+xml;base64,__KRAFT_SVG_SOVIET__');
}

/* --- Thème : OTAN moderne --- */
body[data-theme="modern-nato"] {
  --paper:        #e8e3d8;  /* blanc cassé */
  --paper-light:  #f0ece2;
  --paper-dark:   #c8c0b0;
  --paper-edge:   #948c7c;
  --page-bg:      #e4dfd2;
  --ink:          #15181c;  /* gris-bleu froid */
  --ink-faded:    #3a4048;
  --olive:        #2a3038;  /* anthracite (accent secondaire) */
  --olive-dark:   #1c2026;
  --olive-deep:   #0e1014;
  --khaki:        #5c6b7a;  /* gris-bleu militaire (accent principal) */
  --khaki-light:  #7a8a98;
  --rust:         #2a2a2a;  /* moderne : pas de rouge, neutre */
  --red-stamp:    #1a1a1a;  /* tampons noirs */
  --red-faded:    #4a4a4a;
  --kraft-bg: url('data:image/svg+xml;base64,__KRAFT_SVG_MODERN_NATO__');
}

/* --- Thème : Bloc Est moderne --- */
body[data-theme="modern-east"] {
  --paper:        #cdc6b8;  /* papier grisé */
  --paper-light:  #ddd6c8;
  --paper-dark:   #ada69a;
  --paper-edge:   #7a7466;
  --page-bg:      #c8c1b2;
  --ink:          #1a1610;  /* brun chaud */
  --ink-faded:    #3d3024;
  --olive:        #3d3024;  /* brun terre (accent secondaire) */
  --olive-dark:   #2a2018;
  --olive-deep:   #1a140e;
  --khaki:        #4a5238;  /* vert digital (accent principal) */
  --khaki-light:  #6a7256;
  --rust:         #5a1a1a;
  --red-stamp:    #7a2424;  /* rouge sombre */
  --red-faded:    #a04040;
  --kraft-bg: url('data:image/svg+xml;base64,__KRAFT_SVG_MODERN_EAST__');
}

/* Phase X — étape C : police de corps des thèmes modernes
   Roboto Mono remplace Special Elite (typewriter) sur les 2 thèmes modernes
   pour un rendu technique/digital. La stack de fallback couvre les glyphes
   absents du subset latin (░ ▮ ★ etc. → fallback sur Courier/monospace). */
body[data-theme="modern-nato"],
body[data-theme="modern-east"] {
  --f-typewriter: 'Roboto Mono', 'Courier New', 'Courier', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; overscroll-behavior: none; }
button { font: inherit; cursor: pointer; }
input, select, textarea { font: inherit; }

body {
  font-family: var(--f-typewriter);
  background: var(--olive-deep);
  color: var(--ink);
  font-size: 14px;
  line-height: 1.5;
  overflow: hidden;
  -webkit-tap-highlight-color: transparent;
  -webkit-text-size-adjust: 100%;
}

/* ============ TOOLBAR ============ */
.toolbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 56px;
  background: linear-gradient(180deg, var(--olive-dark) 0%, var(--olive-deep) 100%);
  border-bottom: 2px solid var(--amber-dark);
  display: flex;
  align-items: center;
  padding: 0 14px;
  gap: 8px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0,0,0,.4);
  padding-left: max(14px, env(safe-area-inset-left));
  padding-right: max(14px, env(safe-area-inset-right));
}

.tb-brand {
  display: flex; align-items: center; gap: 10px;
  color: var(--paper);
  font-family: var(--f-stencil);
  font-weight: 700;
  letter-spacing: 2px;
  font-size: 15px;
  border-right: 1px solid var(--khaki);
  padding-right: 12px;
  margin-right: 4px;
  white-space: nowrap;
}
.tb-brand::before {
  content: '';
  display: inline-block;
  width: 8px; height: 8px;
  background: var(--amber);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--amber);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%      { opacity: .4; }
}

.tb-btn {
  font-family: var(--f-condensed);
  font-weight: 700;
  letter-spacing: 1.5px;
  font-size: 12px;
  text-transform: uppercase;
  background: transparent;
  color: var(--paper);
  border: 1px solid var(--khaki);
  padding: 0 14px;
  height: 40px;
  min-width: 44px;
  cursor: pointer;
  transition: all .15s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  white-space: nowrap;
}
.tb-btn:hover, .tb-btn:focus-visible {
  background: var(--olive);
  border-color: var(--amber);
  color: var(--amber);
  outline: none;
}
.tb-btn:active { transform: translateY(1px); }
.tb-btn.active {
  background: var(--amber-dark);
  border-color: var(--amber);
  color: var(--paper-light);
}
.tb-btn.danger:hover {
  background: var(--rust);
  border-color: var(--red-faded);
  color: var(--paper-light);
}
.tb-btn svg { width: 16px; height: 16px; flex-shrink: 0; }

/* Phase X — étape E : sélecteur de thème graphique
   Utilise --olive-dark (thématisé) en background pour suivre l'identité
   visuelle de chaque thème, et --amber/--amber-dark (constants) en accent UI.
   Caret custom SVG inline (couleur amber #c0892a, hard-coded car les data:url
   ne supportent pas les variables CSS — mais l'amber étant constant, c'est
   cohérent avec tous les thèmes). */
.tb-select {
  font-family: var(--f-condensed);
  font-weight: 700;
  letter-spacing: 1.5px;
  font-size: 12px;
  text-transform: uppercase;
  background-color: var(--olive-dark);
  color: var(--amber);
  border: 1px solid var(--amber-dark);
  padding: 0 32px 0 12px;
  height: 40px;
  cursor: pointer;
  transition: all .15s ease;
  white-space: nowrap;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 8'><path d='M1 1l5 5 5-5' fill='none' stroke='%23c0892a' stroke-width='2'/></svg>");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 10px 6px;
}
.tb-select:hover, .tb-select:focus-visible {
  background-color: var(--olive);
  border-color: var(--amber);
  outline: none;
}
.tb-select:active { transform: translateY(1px); }
/* Le menu déroulant natif est rendu par l'OS — on force au moins un fond
   lisible et une couleur de texte exploitable sur tous les systèmes. */
.tb-select option {
  background-color: var(--olive-dark);
  color: var(--paper);
}

.tb-spacer { flex: 1; }

.tb-classif {
  font-family: var(--f-stencil);
  font-size: 11px;
  letter-spacing: 3px;
  color: var(--red-faded);
  border: 1px solid var(--red-faded);
  padding: 4px 10px;
  white-space: nowrap;
}

.tb-version {
  font-size: 11px;
  opacity: 0.5;
  color: var(--amber);
  letter-spacing: 0.5px;
  align-self: center;
  margin-left: 8px;
  user-select: none;
}

/* ============ MAIN APP ============ */
.app {
  position: fixed;
  top: 56px; bottom: 0; left: 0; right: 0;
  display: grid;
  grid-template-columns: 460px 1fr;
  background: var(--olive-deep);
}

.app.preview-only {
  grid-template-columns: 1fr;
}
.app.preview-only .editor { display: none; }

/* ============ EDITOR ============ */
.editor {
  background:
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 2px,
      rgba(0,0,0,.04) 2px,
      rgba(0,0,0,.04) 3px
    ),
    linear-gradient(180deg, var(--olive-dark) 0%, var(--olive-deep) 100%);
  border-right: 2px solid var(--amber-dark);
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 16px 16px 80px 16px;
  color: var(--paper);
}

.editor::-webkit-scrollbar { width: 10px; }
.editor::-webkit-scrollbar-track { background: var(--olive-deep); }
.editor::-webkit-scrollbar-thumb { background: var(--khaki); border: 2px solid var(--olive-deep); }

/* SECTIONS */
.ed-section {
  margin-bottom: 14px;
  border: 1px solid var(--khaki);
  background: rgba(20, 24, 12, .5);
}

.ed-section > summary, .ed-section > .panel-header {
  cursor: pointer;
  padding: 12px 14px;
  background: linear-gradient(90deg, var(--olive) 0%, var(--olive-dark) 100%);
  font-family: var(--f-stencil);
  font-size: 13px;
  letter-spacing: 2px;
  color: var(--amber);
  list-style: none;
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--amber-dark);
  user-select: none;
  min-height: 48px;
}
.ed-section > summary::-webkit-details-marker { display: none; }
.ed-section > summary::after {
  content: '◄';
  font-size: 10px;
  color: var(--paper);
  transition: transform .2s;
}
.ed-section[open] > summary::after {
  transform: rotate(-90deg);
}
.ed-section > summary:hover { color: var(--paper-light); }

.ed-content {
  padding: 14px;
  display: flex; flex-direction: column; gap: 14px;
}

/* FIELDS */
.ed-field { display: flex; flex-direction: column; gap: 5px; }
.ed-field label {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--amber);
  display: flex; align-items: center; gap: 6px;
}
.ed-field label::before {
  content: '►';
  color: var(--rust);
  font-size: 8px;
}

.ed-field input[type=text],
.ed-field input[type=date],
.ed-field input[type=number],
.ed-field textarea,
.ed-field select {
  background: rgba(216, 201, 165, .92);
  border: 1px solid var(--khaki);
  border-left: 3px solid var(--amber-dark);
  font-family: var(--f-typewriter);
  font-size: 13px;
  color: var(--ink);
  padding: 10px 11px;
  min-height: 44px;
  transition: all .15s;
  resize: vertical;
  width: 100%;
}
.ed-field input:focus,
.ed-field textarea:focus,
.ed-field select:focus {
  outline: none;
  border-left-color: var(--red-stamp);
  background: var(--paper-light);
  box-shadow: 0 0 0 1px var(--amber);
}
.ed-field textarea { min-height: 70px; line-height: 1.4; }

.ed-field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

/* DYNAMIC LISTS */
.ed-list { display: flex; flex-direction: column; gap: 8px; }
.ed-list-item { display: flex; gap: 8px; }
.ed-list-item input,
.ed-list-item textarea { flex: 1; }

.ed-btn-icon {
  background: var(--rust);
  border: 1px solid var(--red-faded);
  color: var(--paper-light);
  font-family: var(--f-condensed);
  font-weight: 700;
  cursor: pointer;
  padding: 0 12px;
  transition: background .15s;
  font-size: 18px;
  line-height: 1;
  min-width: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ed-btn-icon:hover { background: var(--red-stamp); }
.ed-btn-icon:active { transform: translateY(1px); }

.ed-btn-add {
  background: transparent;
  border: 1px dashed var(--amber);
  color: var(--amber);
  font-family: var(--f-condensed);
  font-weight: 700;
  letter-spacing: 1.5px;
  padding: 12px;
  min-height: 44px;
  cursor: pointer;
  font-size: 12px;
  text-transform: uppercase;
  transition: all .15s;
}
.ed-btn-add:hover { background: var(--olive); color: var(--paper-light); }
.ed-btn-add:active { transform: translateY(1px); }

/* IMAGE UPLOAD */
.ed-img-zone {
  border: 1px dashed var(--khaki);
  background: rgba(0,0,0,.2);
  padding: 14px;
  text-align: center;
  cursor: pointer;
  font-family: var(--f-condensed);
  font-weight: 600;
  font-size: 11px;
  color: var(--khaki-light);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  transition: all .15s;
  position: relative;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ed-img-zone:hover, .ed-img-zone:focus-within {
  border-color: var(--amber);
  color: var(--amber);
}
.ed-img-zone.has-img {
  border-style: solid;
  border-color: var(--green-radar);
  color: var(--paper);
  padding: 0;
  min-height: 0;
}
.ed-img-zone.has-img img {
  width: 100%;
  height: auto;
  display: block;
  max-height: 280px;
  object-fit: contain;
  background: rgba(0,0,0,.15);
}
.ed-img-zone .img-rm {
  position: absolute;
  top: 6px; right: 6px;
  background: var(--rust);
  color: var(--paper-light);
  border: 1px solid var(--red-faded);
  width: 32px; height: 32px;
  cursor: pointer;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--f-condensed);
  font-size: 18px;
  line-height: 1;
  padding: 0;
}
.ed-img-zone .img-info {
  position: absolute;
  bottom: 6px; left: 6px;
  background: rgba(0,0,0,.7);
  color: var(--paper);
  font-family: var(--f-mono);
  font-size: 9px;
  letter-spacing: 1px;
  padding: 2px 6px;
}
.ed-img-zone input[type=file] { display: none; }

/* PHASE SELECTOR */
.phase-bar {
  display: grid;
  grid-template-columns: 44px 1fr 44px 44px 44px 44px;
  gap: 6px;
  padding: 10px;
  background: rgba(192, 137, 42, .12);
  border: 1px solid var(--amber-dark);
  margin-bottom: 14px;
  align-items: center;
}
.phase-bar button {
  height: 44px;
  background: var(--olive);
  border: 1px solid var(--khaki);
  color: var(--paper);
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  transition: all .15s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.phase-bar button:hover:not(:disabled) {
  background: var(--amber-dark);
  border-color: var(--amber);
}
.phase-bar button:active:not(:disabled) { transform: translateY(1px); }
.phase-bar button:disabled {
  opacity: .35;
  cursor: not-allowed;
}
.phase-bar button.danger { color: var(--red-faded); }
.phase-bar button.danger:hover:not(:disabled) {
  background: var(--rust);
  color: var(--paper-light);
  border-color: var(--red-faded);
}
.phase-indicator {
  text-align: center;
  font-family: var(--f-stencil);
  letter-spacing: 2px;
  color: var(--amber);
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.phase-indicator strong {
  color: var(--paper-light);
  font-size: 16px;
  font-weight: 700;
}

.phase-empty {
  padding: 30px 14px;
  text-align: center;
  color: var(--khaki-light);
  font-family: var(--f-typewriter);
  font-style: italic;
  border: 1px dashed var(--khaki);
}

/* Phase / comm-plan editor card (used inside list editors) */
.ed-phase-card {
  border: 1px solid var(--khaki);
  background: rgba(0,0,0,.2);
  padding: 14px 12px 12px 12px;
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
}
.ed-phase-card .phase-num {
  position: absolute;
  top: -10px; left: 12px;
  background: var(--amber-dark);
  color: var(--paper);
  font-family: var(--f-stencil);
  font-size: 11px;
  letter-spacing: 1px;
  padding: 2px 8px;
  border: 1px solid var(--amber);
}
.ed-phase-card .phase-rm {
  position: absolute;
  top: -10px; right: 8px;
  background: var(--rust);
  color: var(--paper-light);
  border: 1px solid var(--red-faded);
  cursor: pointer;
  padding: 2px 10px;
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 1px;
  text-transform: uppercase;
  height: 22px;
  min-width: 60px;
}
.ed-phase-card .phase-rm:hover { background: var(--red-stamp); }

.ed-help {
  font-family: var(--f-typewriter);
  font-size: 11px;
  color: var(--khaki-light);
  font-style: italic;
  padding: 6px 0;
  border-top: 1px dotted var(--khaki);
  margin-top: 4px;
}

/* ============ WING EDITOR (Phase 4) ============ */
.wing-fieldset {
  border: 1px solid var(--khaki);
  border-radius: 4px;
  padding: 12px;
  margin: 0 0 14px 0;
}
.wing-legend {
  font-family: var(--f-stencil);
  font-size: 11px;
  letter-spacing: .08em;
  color: var(--khaki-light);
  padding: 0 6px;
  text-transform: uppercase;
}
.wing-hint {
  font-family: var(--f-typewriter);
  font-size: 10px;
  color: var(--khaki);
  font-weight: normal;
  font-style: italic;
}
.wing-logo-zone {
  min-height: 80px;
}
/* Squadron cards */
.wing-sq-card {
  border: 1px solid var(--khaki);
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
  background: rgba(0,0,0,.15);
}
.wing-sq-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-family: var(--f-stencil);
  font-size: 12px;
  color: var(--khaki-light);
  letter-spacing: .06em;
}
.wing-sq-toggle {
  flex: 1;
  cursor: pointer;
  user-select: none;
}
.wing-sq-toggle::before {
  content: '▶ ';
  font-size: 9px;
  opacity: .7;
}
.wing-sq-card.open .wing-sq-toggle::before {
  content: '▼ ';
}
.wing-sq-body {
  display: none;
}
.wing-sq-card.open .wing-sq-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
/* Aircraft tags */
.wing-aircraft-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  align-items: center;
}
.wing-ac-tag {
  background: var(--olive);
  color: var(--paper-light);
  font-family: var(--f-typewriter);
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 3px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.wing-ac-tag button {
  background: none;
  border: none;
  color: var(--paper-light);
  cursor: pointer;
  padding: 0;
  font-size: 12px;
  line-height: 1;
  opacity: .7;
}
.wing-ac-tag button:hover { opacity: 1; }
.wing-ac-add-row {
  display: flex;
  gap: 6px;
  margin-top: 4px;
}
.wing-ac-add-row input {
  flex: 1;
}
.wing-ac-add-row button {
  white-space: nowrap;
}
/* Action buttons */
.wing-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 4px 0 10px 0;
}
.wing-action-btn {
  flex: 1;
  min-width: 120px;
  font-family: var(--f-stencil);
  font-size: 12px;
  letter-spacing: .05em;
  padding: 9px 10px;
  border-radius: 3px;
  border: 1px solid var(--khaki);
  background: rgba(0,0,0,.2);
  color: var(--paper-light);
  cursor: pointer;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: background .15s;
}
.wing-action-btn:hover { background: var(--olive); }
.wing-action-import input[type=file] { display: none; }
.wing-action-reset { border-color: var(--red-stamp); color: var(--red-stamp); }
.wing-action-reset:hover { background: var(--red-stamp); color: var(--paper-light); }
/* Size counter */
.wing-size-counter {
  font-family: var(--f-typewriter);
  font-size: 11px;
  color: var(--khaki);
  text-align: right;
  padding: 4px 2px 0;
  opacity: .75;
}
.wing-size-counter.warn { color: #e8b840; opacity: 1; }

/* id field invalid: spaces or slashes detected */
.wing-id-warning {
  border-color: #e8b840 !important;
  box-shadow: 0 0 0 2px rgba(232,184,64,.25) !important;
}
/* Logo zone busy during async compression */
.wing-logo-loading {
  opacity: .45;
  cursor: wait !important;
  pointer-events: none;
}

/* ============ PREVIEW ============ */
.preview-wrap {
  overflow: auto;
  background: var(--olive-deep);
  padding: 30px 20px 60px 20px;
  -webkit-overflow-scrolling: touch;
}
.preview-wrap::-webkit-scrollbar { width: 12px; }
.preview-wrap::-webkit-scrollbar-track { background: var(--olive-deep); }
.preview-wrap::-webkit-scrollbar-thumb { background: var(--khaki); border: 2px solid var(--olive-deep); }

/* PAGES */
.page {
  width: 794px;
  min-height: 1123px;
  margin: 0 auto 30px auto;
  background: var(--page-bg);
  background-image: var(--kraft-bg);
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: top left;
  color: var(--ink);
  position: relative;
  box-shadow: 0 8px 24px rgba(0,0,0,.5), 0 2px 4px rgba(0,0,0,.3);
  padding: 28px 36px 60px 36px;
  overflow: hidden;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page::before, .page::after {
  content: '';
  position: absolute;
  width: 22px; height: 22px;
  border: 2px solid var(--ink-faded);
  pointer-events: none;
}
.page::before { top: 8px; left: 8px; border-right: none; border-bottom: none; }
.page::after { bottom: 8px; right: 8px; border-left: none; border-top: none; }

/* PAGE HEADER */
.p-header {
  display: grid;
  grid-template-columns: 70px 1fr 70px;
  align-items: center;
  gap: 16px;
  padding-bottom: 12px;
  border-bottom: 3px double var(--ink-faded);
  margin-bottom: 18px;
}
.p-header img {
  width: 64px; height: 64px;
  object-fit: contain;
  filter: contrast(1.05);
}
.p-header .p-title { text-align: center; }
.p-header .p-title .p-classif {
  font-family: var(--f-stencil);
  letter-spacing: 6px;
  font-size: 11px;
  color: var(--red-stamp);
  border: 2px solid var(--red-stamp);
  padding: 2px 10px;
  display: inline-block;
  margin-bottom: 6px;
}
.p-header .p-title h1 {
  font-family: var(--f-stencil);
  font-size: 28px;
  letter-spacing: 4px;
  color: var(--ink);
  font-weight: 700;
}
.p-header .p-title .p-sub {
  font-family: var(--f-condensed);
  font-weight: 600;
  font-size: 11px;
  letter-spacing: 3px;
  color: var(--ink-faded);
  margin-top: 2px;
  text-transform: uppercase;
}

/* SECTION BANNER */
.p-section {
  background: var(--olive-dark);
  color: var(--paper-light);
  font-family: var(--f-stencil);
  font-size: 16px;
  letter-spacing: 5px;
  text-align: center;
  padding: 8px 12px;
  border-top: 2px solid var(--amber-dark);
  border-bottom: 2px solid var(--amber-dark);
  margin-bottom: 14px;
}
.p-section::before, .p-section::after {
  content: '◆';
  color: var(--amber);
  margin: 0 12px;
  font-size: 10px;
  vertical-align: middle;
}

.p-subsection {
  background: var(--khaki);
  color: var(--paper-light);
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 3px;
  text-align: center;
  padding: 5px 10px;
  margin: 14px 0 8px 0;
  border-left: 4px solid var(--amber-dark);
  border-right: 4px solid var(--amber-dark);
  text-transform: uppercase;
}

.p-body {
  font-family: var(--f-typewriter);
  font-size: 13px;
  line-height: 1.65;
  color: var(--ink);
}
.p-body p { margin-bottom: 10px; text-align: justify; }

/* BULLETS */
.p-bullets { list-style: none; padding-left: 4px; }
.p-bullets li {
  padding: 4px 0 4px 24px;
  position: relative;
  border-bottom: 1px dotted var(--paper-edge);
}
.p-bullets li:last-child { border-bottom: none; }
.p-bullets li::before {
  content: '✓';
  position: absolute;
  left: 4px; top: 4px;
  color: var(--olive);
  font-weight: 700;
  font-size: 14px;
}

.p-bullets-num { list-style: none; padding: 0; counter-reset: stepcount; }
.p-bullets-num li {
  padding: 3px 0 3px 32px;
  position: relative;
  counter-increment: stepcount;
}
.p-bullets-num li::before {
  content: counter(stepcount, decimal-leading-zero);
  position: absolute;
  left: 4px; top: 3px;
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  color: var(--rust);
  background: var(--paper-light);
  border: 1px solid var(--khaki);
  padding: 0 4px;
  letter-spacing: 1px;
}

/* IMAGE FRAME */
.p-imgframe {
  border: 2px solid var(--ink-faded);
  padding: 5px;
  background: rgba(0,0,0,.05);
  margin: 10px 0;
  position: relative;
}
.p-imgframe::before {
  content: attr(data-label);
  position: absolute;
  top: -10px; left: 10px;
  background: var(--paper);
  padding: 0 6px;
  font-family: var(--f-condensed);
  font-weight: 600;
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--ink-faded);
  text-transform: uppercase;
}
.p-imgframe img {
  display: block;
  max-width: 100%;
  width: auto;
  height: auto;
  max-height: 190mm;
  margin: 0 auto;   /* centrage horizontal */
}
.p-imgframe.empty {
  background:
    linear-gradient(135deg, transparent 49%, var(--khaki) 49%, var(--khaki) 51%, transparent 51%),
    linear-gradient(45deg, transparent 49%, var(--khaki) 49%, var(--khaki) 51%, transparent 51%);
  background-size: 40px 40px;
  background-color: rgba(0,0,0,.04);
  min-height: 280px;
  display: flex; align-items: center; justify-content: center;
}
.p-imgframe.empty::after {
  content: '◯ AUCUNE CARTE FOURNIE ◯';
  font-family: var(--f-stencil);
  letter-spacing: 4px;
  color: var(--khaki);
  font-size: 14px;
  background: var(--paper);
  padding: 8px 16px;
}

/* FOOTER */
.p-footer {
  position: absolute;
  bottom: 16px; left: 36px; right: 36px;
  display: flex; justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--ink-faded);
  padding-top: 6px;
  font-family: var(--f-condensed);
  font-weight: 600;
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--ink-faded);
  text-transform: uppercase;
}
.p-footer .p-classif-foot {
  color: var(--red-stamp);
  letter-spacing: 4px;
  font-family: var(--f-stencil);
}

/* THREAT CHIPS */
.threat-chip {
  display: inline-block;
  font-family: var(--f-stencil);
  font-size: 11px;
  letter-spacing: 3px;
  padding: 4px 12px;
  border: 2px solid;
  text-transform: uppercase;
  vertical-align: middle;
}
/* Faible — vert */
.threat-chip.t-faible  { color: #1a4d1a; border-color: #2d6e2d; background: #c8e6c9; }
/* Modéré — orange vif */
.threat-chip.t-modere  { color: #7a3a00; border-color: #d06000; background: #ffe0b2; }
/* Élevé  — rouge */
.threat-chip.t-eleve   { color: #fff;    border-color: #7b0000; background: #b71c1c; }

/* PHASE TITLE BLOCK */
.phase-title {
  font-family: var(--f-stencil);
  font-size: 17px;
  letter-spacing: 3px;
  color: var(--olive-dark);
  border-bottom: 1px solid var(--ink-faded);
  padding-bottom: 4px;
  margin-bottom: 8px;
  display: flex; align-items: center; flex-wrap: wrap; gap: 10px;
}
.phase-num-tag {
  background: var(--olive-dark);
  color: var(--amber);
  padding: 2px 8px;
  font-size: 12px;
  letter-spacing: 2px;
}

.phase-block {
  margin-bottom: 14px;
  padding: 8px 10px;
  background: rgba(255,255,255,.18);
  border-left: 3px solid var(--olive);
}
.phase-block-label {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--rust);
  text-transform: uppercase;
  margin-bottom: 4px;
}

.p-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.p-2col > div { min-width: 0; }

/* METAR */
.metar-line {
  font-family: var(--f-mono);
  font-size: 14px;
  letter-spacing: 1px;
  background: var(--olive-deep);
  color: #b3d99b;
  padding: 10px 14px;
  border-left: 4px solid var(--green-radar);
  border-right: 4px solid var(--green-radar);
  margin: 4px 0;
  word-break: break-all;
}
.metar-line::before { content: '> '; color: var(--amber); }

/* RADIO */

.txt-small { font-size: 11px; color: var(--ink-faded); }

/* ============ SUB-TASKS in preview ============ */
.p-subtasks {
  list-style: none;
  padding-left: 20px;
  margin-top: 4px;
  counter-reset: subtask;
}
.p-subtasks li {
  padding: 2px 0 2px 22px;
  position: relative;
  border-bottom: none;
  font-size: 12px;
  color: var(--ink-faded);
  counter-increment: subtask;
}
.p-subtasks li::before {
  content: counter(subtask, lower-alpha) ')';
  position: absolute;
  left: 0;
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  color: var(--olive);
  letter-spacing: 1px;
}

/* ============ REORDER buttons in editor lists ============ */
.ed-list-item { align-items: flex-start; }
.ed-list-move {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex-shrink: 0;
}
.ed-btn-move {
  background: var(--olive-dark);
  border: 1px solid var(--khaki);
  color: var(--khaki-light);
  font-size: 12px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .12s;
}
.ed-btn-move:hover:not(:disabled) {
  background: var(--amber-dark);
  color: var(--paper);
  border-color: var(--amber);
}
.ed-btn-move:disabled { opacity: .3; cursor: not-allowed; }
.ed-btn-move:active:not(:disabled) { transform: translateY(1px); }

/* Sub-task items in editor */
.ed-subtask-wrap {
  margin-top: 6px;
  padding-left: 12px;
  border-left: 2px solid var(--olive-dark);
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.ed-subtask-row {
  display: flex;
  gap: 6px;
}
.ed-subtask-row input { flex: 1; font-size: 12px; }
.ed-btn-subtask-add {
  font-family: var(--f-condensed);
  font-weight: 600;
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  background: transparent;
  border: 1px dashed var(--olive);
  color: var(--olive);
  cursor: pointer;
  padding: 5px 10px;
  margin-top: 4px;
  transition: all .12s;
}
.ed-btn-subtask-add:hover { background: var(--olive-dark); color: var(--paper); }

/* Phase bar with reorder buttons */
.phase-bar {
  display: grid;
  grid-template-columns: 44px 1fr 44px 44px 44px 44px 44px 44px;
  gap: 6px;
}

.empty-placeholder {
  font-family: var(--f-typewriter);
  font-style: italic;
  color: var(--khaki);
  padding: 10px 0;
  border: 1px dashed var(--khaki);
  text-align: center;
  margin: 6px 0;
  font-size: 12px;
}

/* ============ RADIO SUMMARY (page 3) ============ */
.radio-summary {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--f-typewriter);
  font-size: 12px;
  margin: 4px 0;
}
.radio-summary tr { border-bottom: 1px dotted var(--paper-edge); }
.radio-summary tr:last-child { border-bottom: none; }
.radio-summary th {
  text-align: left;
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 1.5px;
  color: var(--rust);
  text-transform: uppercase;
  padding: 4px 8px 4px 4px;
  white-space: nowrap;
  width: 1%;
}
.radio-summary td {
  padding: 4px 4px;
  text-align: right;
}
.radio-summary .radio-freq {
  font-family: var(--f-mono);
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--ink);
}
.radio-summary .radio-mod {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 10px;
  letter-spacing: 1.5px;
  color: var(--olive);
  margin-left: 6px;
  display: inline-block;
  padding: 1px 5px;
  background: rgba(74, 82, 48, .15);
  border: 1px solid var(--paper-edge);
}

/* ============ RADIO TABLE (annexe per aircraft) ============ */
.radio-block {
  margin-bottom: 12px;
}
.radio-block-name {
  font-family: var(--f-stencil);
  font-size: 14px;
  letter-spacing: 3px;
  color: var(--olive-dark);
  background: var(--paper-light);
  padding: 4px 10px;
  border-left: 3px solid var(--rust);
  border-bottom: 1px solid var(--paper-edge);
}
.radio-channel-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--f-mono);
  font-size: 11px;
  margin-top: 2px;
}
.radio-channel-table tr { border-bottom: 1px dotted var(--paper-edge); }
.radio-channel-table tr:last-child { border-bottom: none; }
.radio-channel-table td {
  padding: 3px 6px;
  vertical-align: middle;
}
.radio-channel-table .ch-num {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--rust);
  background: var(--paper-light);
  width: 1%;
  white-space: nowrap;
  text-align: center;
}
.radio-channel-table .ch-freq {
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--ink);
  width: 1%;
  white-space: nowrap;
}
.radio-channel-table .ch-mod {
  width: 1%;
  white-space: nowrap;
  font-family: var(--f-condensed);
  font-weight: 600;
  font-size: 10px;
  color: var(--olive);
  letter-spacing: 1px;
}
.radio-channel-table .ch-label {
  font-family: var(--f-typewriter);
  font-size: 11px;
  color: var(--ink-faded);
  letter-spacing: 0.5px;
}

/* ============ GUEST SQUADRON badge (no logo) ============ */
.squadron-logo-guest {
  width: 38px; height: 38px;
  flex-shrink: 0;
  background: var(--olive-dark);
  border: 2px solid var(--khaki);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--f-stencil);
  font-size: 10px;
  letter-spacing: 1px;
  color: var(--amber);
}
.squadron-grid .squadron-logo-guest {
  width: 32px; height: 32px;
  font-size: 8px;
}

/* Extended squadron chip with sub-group */
.squadron-chip .sq-sub {
  padding: 5px 10px;
  color: var(--olive-dark);
  font-style: italic;
  border-right: 1px solid var(--paper-edge);
  font-family: var(--f-typewriter);
  font-weight: 400;
  font-size: 11px;
  letter-spacing: 0.5px;
  text-transform: none;
}

/* ============ EDITOR — canal custom toggle ============ */
.ed-channel-row {
  display: grid;
  grid-template-columns: 44px 56px 1fr 44px;
  gap: 5px;
  align-items: start;
  margin-bottom: 4px;
}
.ed-channel-row.custom-mode {
  grid-template-columns: 44px 56px 1fr 1fr 58px 44px;
}
.ed-ch-toggle {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  background: var(--olive);
  color: var(--paper-light);
  border: 1px solid var(--khaki);
  cursor: pointer;
  min-height: 44px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .15s;
  line-height: 1.1;
  text-align: center;
  padding: 2px 3px;
}
.ed-ch-toggle:hover { background: var(--amber-dark); border-color: var(--amber); }
.ed-ch-toggle:active { transform: translateY(1px); }
.ed-ch-toggle.is-custom {
  background: var(--rust);
  color: var(--paper-light);
  border-color: var(--red-faded);
}
.ed-ch-toggle.is-custom:hover { background: var(--red-stamp); }

/* Radio table rows for custom freqs (dim the ch-label) */
.radio-channel-table .ch-custom-label {
  font-family: var(--f-typewriter);
  font-size: 11px;
  color: var(--ink-faded);
  font-style: italic;
}

/* Guest squadron fields in phase editor */
.ed-guest-fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  background: rgba(122, 58, 32, .08);
  border: 1px dashed var(--rust);
  margin-top: 2px;
}
.ed-guest-fields label::before { color: var(--red-stamp); }

@media (max-width: 600px) {
  .ed-channel-row.custom-mode {
    grid-template-columns: 44px 52px 1fr 50px 44px;
  }
}
.ed-radio-item-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr 70px 44px;
  gap: 6px;
  margin-bottom: 6px;
}
.ed-radio-item-row input,
.ed-radio-item-row select {
  min-width: 0;
}

.ed-radio-block {
  border: 1px dashed var(--khaki);
  padding: 8px;
  margin-bottom: 8px;
  background: rgba(0,0,0,.12);
}
.ed-radio-block-head {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
}
.ed-radio-block-head input {
  flex: 1;
  background: rgba(216, 201, 165, .92) !important;
  border-left-color: var(--amber) !important;
  font-weight: 700;
  letter-spacing: 1px;
}
.ed-channels-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 6px;
}
.ed-channel-row input,
.ed-channel-row select { min-width: 0; }

.ed-btn-add-sm {
  padding: 6px 10px;
  min-height: 36px;
  font-size: 10px;
}

/* Mobile: tighter rows */
@media (max-width: 600px) {
  .ed-radio-item-row {
    grid-template-columns: 1fr 80px 60px 40px;
  }
}
.menace-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
  margin: 6px 0;
}
.menace-cell {
  background: rgba(122, 58, 32, .08);
  border: 1px solid var(--paper-edge);
  border-left: 3px solid var(--rust);
  padding: 5px 10px;
  font-size: 12px;
}
.menace-cell strong {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--rust);
  text-transform: uppercase;
  display: block;
  margin-bottom: 2px;
}

/* SQUADRON CHIP (on phase pages, just under section title) */
.squadron-chip {
  display: inline-flex;
  align-items: center;
  gap: 0;
  border: 2px solid var(--olive-dark);
  background: var(--paper-light);
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin: 0 0 8px 0;
  overflow: hidden;
}
.squadron-chip .sq-id {
  background: var(--olive-dark);
  color: var(--amber);
  padding: 5px 10px;
  letter-spacing: 3px;
}
.squadron-chip .sq-cs {
  padding: 5px 10px;
  color: var(--rust);
  border-right: 1px solid var(--paper-edge);
}
.squadron-chip .sq-ac {
  padding: 5px 10px;
  color: var(--ink-faded);
  font-family: var(--f-mono);
  font-weight: 500;
  font-size: 11px;
  letter-spacing: 1px;
  text-transform: none;
}

/* SQUADRON GRID on Mission Overview page */
.squadron-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 6px 0;
}
/* All cells always the same width — 3 per row, regardless of total count.
   Formula: (100% - 2 gaps) / 3  →  (100% - 16px) / 3 */
.squadron-cell {
  flex: 0 0 calc(33.333% - 5.334px);
  min-width: 0;
}
.squadron-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(74, 82, 48, .12);
  border: 1px solid var(--paper-edge);
  border-left: 3px solid var(--olive);
  padding: 6px 10px;
  font-size: 12px;
  min-width: 0;
}
.squadron-cell .squadron-logo-sm {
  width: 38px;
  height: 38px;
  object-fit: contain;
  flex-shrink: 0;
}
.squadron-cell .squadron-info { flex: 1; min-width: 0; overflow: hidden; }
.squadron-cell .squadron-info strong {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 1.5px;
  color: var(--olive-dark);
  text-transform: uppercase;
  display: block;
  margin-bottom: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.squadron-cell .squadron-aircraft {
  font-family: var(--f-mono);
  font-size: 10px;
  color: var(--ink-faded);
  letter-spacing: 0.5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.squadron-cell .squadron-phases {
  font-family: var(--f-condensed);
  font-weight: 600;
  font-size: 10px;
  letter-spacing: 1.5px;
  color: var(--rust);
  text-transform: uppercase;
  margin-top: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
/* All cells are compact (always 3-col) */
.squadron-grid .squadron-cell {
  padding: 6px 8px;
  gap: 8px;
}
.squadron-grid .squadron-cell .squadron-logo-sm {
  width: 32px;
  height: 32px;
}

/* ============ IMAGE PAGES (dedicated) ============ */
.p-img-page-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
/* 2 images empilées — hauteur réduite pour tenir sur la page */
.p-img-page-grid.stacked-two .p-img-block img {
  max-height: 88mm;
}
.p-img-block {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.p-img-block-title {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--rust);
  border-bottom: 1px solid var(--paper-edge);
  padding-bottom: 4px;
}
.p-img-block img {
  /* Le cadre s'adapte à l'image (pas l'inverse) — centré horizontalement */
  display: block;
  max-width: 100%;
  width: auto;
  height: auto;
  max-height: 190mm;
  margin: 0 auto;
  border: 1px solid var(--paper-edge);
}
.p-img-block-caption {
  font-family: var(--f-typewriter);
  font-size: 11px;
  color: var(--ink-faded);
  font-style: italic;
  line-height: 1.3;
  border-top: 1px dotted var(--paper-edge);
  padding-top: 4px;
}

/* ============ EDITOR — phase images list ============ */
.ed-img-list { display: flex; flex-direction: column; gap: 14px; }
.ed-img-card {
  border: 1px solid var(--khaki);
  background: rgba(0,0,0,.15);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
}
.ed-img-card-num {
  position: absolute;
  top: -10px; left: 10px;
  background: var(--olive);
  color: var(--paper);
  font-family: var(--f-stencil);
  font-size: 10px;
  letter-spacing: 1px;
  padding: 2px 8px;
  border: 1px solid var(--khaki);
}
.ed-img-card-rm {
  position: absolute;
  top: -10px; right: 8px;
  background: var(--rust);
  color: var(--paper-light);
  border: 1px solid var(--red-faded);
  cursor: pointer;
  padding: 2px 10px;
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  text-transform: uppercase;
}
.ed-img-card-rm:hover { background: var(--red-stamp); }

/* STAMPS */
.stamp-classif {
  transform: rotate(-9deg);
  border: 4px solid var(--red-stamp);
  color: var(--red-stamp);
  font-family: var(--f-stencil);
  font-size: 18px;
  letter-spacing: 4px;
  padding: 6px 16px;
  opacity: .55;
  text-align: center;
  background: rgba(255,255,255,.05);
  order: 2;
}
.stamp-classif::before, .stamp-classif::after {
  content: '';
  display: block;
  height: 2px;
  background: var(--red-stamp);
  margin: 4px 0;
}

.stamp-receipt {
  transform: rotate(-4deg);
  border: 2px solid var(--ink-faded);
  color: var(--ink-faded);
  font-family: var(--f-typewriter);
  font-size: 10px;
  letter-spacing: 1.5px;
  padding: 6px 12px;
  opacity: .65;
  text-transform: uppercase;
  text-align: center;
  background: rgba(255,255,255,.18);
  line-height: 1.3;
  order: 1;
}

/* ============================================
   STAMPS — Phase X étape D : variantes thématiques
   Overrides CSS uniquement, le DOM .stamp-classif reste inchangé.
   Le texte (state.meta.classification) demeure dynamique.
   ============================================ */

/* --- cw-soviet : étoile à 5 branches en arrière-plan, texte ocre crème
       Plan B3 — sceau quasi-carré (width 180px) pour préserver l'aspect-ratio
       de l'étoile (1:1) et garantir les 5 pointes visibles quel que soit
       le texte. white-space normal autorise le wrap sur 2 lignes pour les
       classifications longues. paint-order + text-stroke pour la lisibilité
       quand le texte déborde marginalement de la zone rouge centrale.
       Variante A — sceau centré horizontalement (display: block + margin auto)
       pour une composition équilibrée au lieu d'aligné à gauche en flow normal. --- */
body[data-theme="cw-soviet"] .stamp-classif {
  display: block;
  margin: 24px auto 8px auto;
  border: 3px solid var(--red-stamp);
  width: 180px;
  color: #e8d690;
  -webkit-text-stroke: 1.5px #1a1610;
  paint-order: stroke fill;
  font-weight: 400;
  letter-spacing: 1px;
  font-size: 14px;
  line-height: 1.2;
  opacity: .9;
  transform: rotate(-6deg);
  padding: 70px 24px;
  white-space: normal;
  text-align: center;
  background-color: transparent;
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cG9seWdvbiBwb2ludHM9IjUwLDIgNjEuNzYsMzMuODIgOTUuNjUsMzUuMTcgNjkuMDIsNTYuMTggNzguMjEsODguODMgNTAsNzAgMjEuNzksODguODMgMzAuOTgsNTYuMTggNC4zNSwzNS4xNyAzOC4yNCwzMy44MiIgZmlsbD0iIzg0MWUxZSIvPjwvc3ZnPg==');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
body[data-theme="cw-soviet"] .stamp-classif::before,
body[data-theme="cw-soviet"] .stamp-classif::after {
  display: none;
}

/* --- modern-nato + modern-east : carré digital plat, sans rotation, pas vintage --- */
body[data-theme="modern-nato"] .stamp-classif,
body[data-theme="modern-east"] .stamp-classif {
  border: 1.5px solid var(--red-stamp);
  border-radius: 4px;
  transform: rotate(0deg);
  opacity: 1;
  font-family: var(--f-typewriter);
  font-weight: 400;
  font-size: 13px;
  letter-spacing: 2px;
  padding: 8px 16px 8px 30px;
  background: rgba(255,255,255,.45);
  position: relative;
}
/* Pastille indicatrice ronde — réutilise le pseudo-élément ::before
   (qui faisait la barre horizontale en cw-nato). */
body[data-theme="modern-nato"] .stamp-classif::before,
body[data-theme="modern-east"] .stamp-classif::before {
  content: '';
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--red-stamp);
  margin: 0;
}
/* Cacher la barre horizontale du bas en modern-nato. */
body[data-theme="modern-nato"] .stamp-classif::after {
  display: none;
}

/* --- modern-east : étiquette ID mini bleu-noir au coin inférieur droit
       Réutilise ::after (qui faisait la barre du bas en cw-nato). --- */
body[data-theme="modern-east"] .stamp-classif {
  padding-bottom: 14px;
}
body[data-theme="modern-east"] .stamp-classif::after {
  content: 'MZ-7';
  display: block;
  position: absolute;
  bottom: 1px;
  right: 6px;
  background: transparent;
  color: #1a2030;  /* bleu-noir hors palette de thème (accent dédié) */
  font-family: var(--f-typewriter);
  font-weight: 400;
  font-size: 7px;
  letter-spacing: 1px;
  margin: 0;
  height: auto;
}

.doc-meta {
  position: absolute;
  top: 12px; left: 50%;
  transform: translateX(-50%);
  font-family: var(--f-mono);
  font-size: 9px;
  letter-spacing: 2px;
  color: var(--ink-faded);
  text-transform: uppercase;
}

/* ============ ROSTER — single unified <table> per pair of groups ============
   Architecture: ONE <table> = ONE rendering pipeline = stable in both screen & PDF.
   Identical CSS for screen and print (no @media print overrides for roster). */
.roster-tables {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.roster-mega {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  table-layout: fixed;
}
/* Column widths: always 4 columns, each pair gets 50% */
.rmt-col-name { width: 32%; }
.rmt-col-cs   { width: 18%; }

/* Group header row (colspan="2" for each group) */
.rmt-row-group .rmt-group-head {
  text-align: left;
  padding: 6px 10px 5px 12px;
  border-left: 4px solid var(--rust);
  border-bottom: 1px solid var(--paper-edge);
  vertical-align: top;
  /* No background — uses border-left + page kraft for distinction */
}
.rmt-row-group .rmt-group-head + .rmt-group-head {
  /* Visual gap between left and right group in the same row */
  padding-left: 22px;
}
.rmt-group-name {
  display: block;
  font-family: var(--f-stencil);
  font-weight: 400;
  font-size: 13px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--olive-dark);
  margin-bottom: 4px;
}
.rmt-group-aircraft {
  display: inline-block;
  font-family: var(--f-mono);
  font-size: 10px;
  letter-spacing: 1.5px;
  color: var(--rust);
  font-weight: normal;
  padding: 1px 5px;
  border: 1px solid var(--rust);
}

/* Column header row */
.rmt-row-cols th {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--olive-dark);
  padding: 5px 10px;
  text-align: left;
  border-bottom: 2px solid var(--olive);
}

/* Data cells */
.roster-mega tbody td {
  font-family: var(--f-typewriter);
  font-size: 12px;
  padding: 5px 10px;
  border-bottom: 1px dotted var(--paper-edge);
  vertical-align: middle;
  overflow: hidden;
  text-overflow: ellipsis;
}
.roster-mega tbody tr:last-child td { border-bottom: none; }
.roster-mega .rmt-callsign {
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 1.5px;
  color: var(--rust);
}

/* Vertical separator between left and right groups */
.rmt-sep {
  border-left: 1px dashed var(--paper-edge);
  padding-left: 22px;
}

.ed-label-hint {
  font-weight: 400;
  font-size: 10px;
  letter-spacing: 0.5px;
  color: var(--khaki);
  text-transform: none;
  opacity: 0.8;
}
.roster-aircraft-hint {
  font-family: var(--f-mono);
  font-size: 11px;
  color: var(--amber);
  letter-spacing: 1px;
}

.roster-pilot-row {
  display: grid;
  grid-template-columns: 2fr 1.5fr 44px;
  gap: 6px;
  margin-bottom: 5px;
}
.roster-pilot-row input { min-width: 0; }

/* ============ TAB BAR — active tab roster ============ */
.tab-bar {
  display: none;
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(180deg, var(--olive-dark) 0%, var(--olive-deep) 100%);
  border-top: 2px solid var(--amber-dark);
  padding: 6px 4px;
  padding-bottom: max(6px, env(safe-area-inset-bottom));
  z-index: 999;
  gap: 2px;
}
.tab-bar button {
  flex: 1;
  background: transparent;
  border: 1px solid transparent;
  color: var(--khaki-light);
  font-family: var(--f-condensed);
  font-weight: 700;
  font-size: 9px;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 6px 2px;
  min-height: 54px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  transition: all .15s;
}
.tab-bar button .tab-ico {
  font-size: 16px;
  line-height: 1;
  font-family: var(--f-stencil);
  font-weight: 700;
}
.tab-bar button.current {
  background: var(--olive);
  color: var(--amber);
  border-color: var(--amber-dark);
}
.tab-bar button:active { transform: translateY(1px); }

/* ============ TOAST ============ */
.toast {
  position: fixed;
  bottom: 20px; left: 50%;
  transform: translateX(-50%) translateY(100px);
  background: var(--olive-dark);
  border: 1px solid var(--amber);
  color: var(--paper);
  font-family: var(--f-condensed);
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  font-size: 12px;
  padding: 10px 20px;
  z-index: 2000;
  opacity: 0;
  transition: all .3s ease;
  pointer-events: none;
  box-shadow: 0 4px 16px rgba(0,0,0,.6);
}
.toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
  pointer-events: auto;
}

/* ============ RESPONSIVE — TABLET / MOBILE ============ */
@media (max-width: 1100px) {
  /* Hide some toolbar buttons text */
  .tb-btn .tb-btn-label { display: none; }
  .tb-btn { padding: 0 10px; }
  .tb-classif { display: none; }
  .tb-brand { font-size: 13px; padding-right: 10px; }
  .tb-brand-sub { display: none; }

  .app {
    grid-template-columns: 1fr;
    bottom: 68px;
  }
  .app .editor, .app .preview-wrap {
    display: none;
  }
  /* Show only the active panel zone */
  body[data-active-tab="preview"] .preview-wrap { display: block; }
  body:not([data-active-tab="preview"]) .editor { display: block; }

  /* Hide non-active editor sections */
  body:not([data-active-tab="preview"]) .ed-section { display: none; }
  body[data-active-tab="meta"] .ed-section[data-section="meta"],
  body[data-active-tab="cover"] .ed-section[data-section="cover"],
  body[data-active-tab="sitac"] .ed-section[data-section="sitac"],
  body[data-active-tab="mission"] .ed-section[data-section="mission"],
  body[data-active-tab="radio"] .ed-section[data-section="radio"],
  body[data-active-tab="phases"] .ed-section[data-section="phases"],
  body[data-active-tab="roster"] .ed-section[data-section="roster"],
  body[data-active-tab="annexes"] .ed-section[data-section="annexes"],
  body[data-active-tab="wing"] .ed-section[data-section="wing"] {
    display: block;
    border: none;
  }

  /* Active section: hide summary, force content visible */
  body[data-active-tab] .ed-section > summary { display: none; }
  body[data-active-tab] .ed-section > .ed-content {
    display: flex !important;
    padding: 0;
    padding-top: 8px;
  }

  /* Show panel header instead */
  .panel-mobile-header {
    display: flex !important;
    background: linear-gradient(90deg, var(--olive) 0%, var(--olive-dark) 100%);
    padding: 12px 14px;
    font-family: var(--f-stencil);
    font-size: 14px;
    letter-spacing: 2px;
    color: var(--amber);
    border-bottom: 1px solid var(--amber-dark);
    margin: -16px -16px 12px -16px;
  }

  .tab-bar { display: flex; }

  /* Preview adapts: scale to fit width */
  .preview-wrap { padding: 16px 8px 30px 8px; }
  .page {
    width: 100%;
    max-width: 794px;
    transform-origin: top center;
    /* JS will apply scale */
    padding: 22px 24px 50px 24px;
    min-height: auto;
  }
}
.panel-mobile-header { display: none; }

/* PHONE */
@media (max-width: 600px) {
  .tb-brand { font-size: 11px; letter-spacing: 1px; padding-right: 8px; margin-right: 2px; }
  .tb-brand::before { width: 6px; height: 6px; }
  .tb-btn { padding: 0 8px; min-width: 40px; height: 38px; }
  .tb-btn svg { width: 14px; height: 14px; }
  .tab-bar button { font-size: 9px; min-height: 50px; }
  .tab-bar button .tab-ico { font-size: 14px; }
  .editor { padding: 12px 12px 24px 12px; }
  .ed-field-row { grid-template-columns: 1fr; }
  .phase-bar { grid-template-columns: 40px 1fr 40px 40px 40px 40px; }
  .tb-version { display: none; }
}

/* ============ PRINT ============ */
@media print {
  body { background: white; overflow: visible; }
  .toolbar, .editor, .tab-bar { display: none !important; }
  .app { position: static; display: block; bottom: auto; }
  .preview-wrap {
    position: static; padding: 0; overflow: visible;
    background: white; display: block !important;
  }
  .page {
    /* Exact A4 — no overflow onto next page */
    width: 210mm;
    height: 297mm;
    min-height: 0 !important;
    max-height: 297mm;
    overflow: hidden;
    margin: 0;
    padding: 12mm 14mm 20mm 14mm;
    box-shadow: none;
    page-break-after: always;
    break-after: page;
    transform: none !important;
    /* SVG kraft texture — couvre exactement la page A4 (par thème via --kraft-bg) */
    background-color: var(--page-bg);
    background-image: var(--kraft-bg);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    background-position: top left;
    background-attachment: scroll;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    color-adjust: exact;
    position: relative;
    z-index: auto;
  }
  /* Contenu toujours au-dessus du fond raster */
  .page > * {
    position: relative;
    z-index: 1;
  }
  .page:last-child { page-break-after: auto; break-after: auto; }

  /* Roster: identical layout in screen and print (same single <table>),
     so no print-specific overrides needed for roster anymore. */

  /* Keep footer anchored to bottom in print */
  .p-footer {
    position: absolute;
    bottom: 8mm; left: 14mm; right: 14mm;
    padding-top: 4px;
  }
  /* Simplify other CSS backgrounds that can cause artifacts */
  .p-bullets li::before,
  .p-bullets-num li::before { background: var(--paper); }
  .radio-block-name { background: var(--paper-light); }

  @page {
    size: A4 portrait;
    margin: 0;
  }
}
"""

CSS = CSS.replace('__STARDOS_400__', A['STARDOS_400'])
CSS = CSS.replace('__STARDOS_700__', A['STARDOS_700'])
CSS = CSS.replace('__SPECIAL_ELITE__', A['SPECIAL_ELITE'])
CSS = CSS.replace('__ROBOTO_MONO_400__', A['ROBOTO_MONO_400'])

# Write CSS to a separate file for now; we'll combine later
with open('/home/claude/briefing.css', 'w') as f:
    f.write(CSS)

print(f"CSS written: {len(CSS):,} bytes")
