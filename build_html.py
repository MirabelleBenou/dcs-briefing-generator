#!/usr/bin/env python3
"""Build the v2 DCS World Briefing Generator HTML."""

import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

APP_VERSION = "2.1.0"

with open(os.path.join(HERE, 'assets.json')) as f:
    A = json.load(f)

with open(os.path.join(HERE, 'briefing.css')) as f:
    CSS = f.read()

HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
<meta name="theme-color" content="#1a1e10">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<title>MY WING // GÉNÉRATEUR DE BRIEFING</title>
<style>
__CSS__
</style>
<!-- html2canvas v1.4.1 — embarqué pour export PNG kneeboard (étape B) -->
<script>__LIB_HTML2CANVAS__</script>
<!-- JSZip v3.10.1 — embarqué pour export ZIP multi-pages (étape B) -->
<script>__LIB_JSZIP__</script>
</head>
<body data-theme="cw-nato">

<!-- ===== TOOLBAR ===== -->
<header class="toolbar" role="toolbar" aria-label="Actions principales">
  <div class="tb-brand"><span class="tb-brand-main">MY WING</span> <span class="tb-brand-sub">░ BRIEFING</span></div>
  <button class="tb-btn" id="btn-save" title="Exporter le briefing en JSON">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
    <span class="tb-btn-label">Sauver</span>
  </button>
  <button class="tb-btn" id="btn-load" title="Charger un briefing JSON">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
    <span class="tb-btn-label">Charger</span>
  </button>
  <input type="file" id="file-load" accept=".json,application/json" hidden>
  <button class="tb-btn" id="btn-print" title="Exporter en PDF ou PNG (kneeboard DCS)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
    <span class="tb-btn-label">Exporter</span>
  </button>
  <button class="tb-btn danger" id="btn-reset" title="Réinitialiser au briefing par défaut">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
    <span class="tb-btn-label">Reset</span>
  </button>
  <select class="tb-select" id="theme-select" title="Thème graphique">
    <option value="cw-nato">Cold War OTAN</option>
    <option value="cw-soviet">Cold War Soviétique</option>
    <option value="modern-nato">OTAN moderne</option>
    <option value="modern-east">Bloc Est moderne</option>
  </select>
  <div class="tb-spacer"></div>
  <div class="tb-classif">CLASSIFIED // FOR EYES ONLY</div>
  <span class="tb-version">v__APP_VERSION__</span>
</header>

<!-- ===== EXPORT MODAL ===== -->
<div class="export-modal" id="export-modal" hidden role="dialog" aria-labelledby="export-modal-title" aria-modal="true">
  <div class="export-modal-backdrop" id="export-modal-backdrop"></div>
  <div class="export-modal-panel" role="document">
    <button class="export-modal-close" id="export-modal-close" aria-label="Fermer">×</button>
    <h2 id="export-modal-title">Exporter le briefing</h2>
    <p class="export-modal-subtitle">Choisissez le format de sortie</p>
    <div class="export-modal-choices">
      <button class="export-choice" id="export-choice-pdf" type="button">
        <div class="export-choice-icon">🖨</div>
        <div class="export-choice-label">PDF</div>
        <div class="export-choice-desc">Impression système · Toutes les pages</div>
      </button>
      <button class="export-choice" id="export-choice-png" type="button">
        <div class="export-choice-icon">🖼</div>
        <div class="export-choice-label">PNG</div>
        <div class="export-choice-desc">Kneeboard DCS · 794×1123, A4</div>
      </button>
    </div>
    <!-- Le panneau PNG (sélecteur de pages) apparaît ici en step 2 — implémenté étape B -->
    <div class="export-png-config" id="export-png-config" hidden>
      <h3>Pages à exporter</h3>
      <div class="export-png-actions-top">
        <button type="button" class="export-png-toggle" id="export-png-all">Tout cocher</button>
        <button type="button" class="export-png-toggle" id="export-png-none">Tout décocher</button>
      </div>
      <div class="export-png-list" id="export-png-list">
        <!-- checkboxes par page injectées dynamiquement -->
      </div>
      <div class="export-png-actions-bottom">
        <button type="button" class="export-png-back" id="export-png-back">← Retour</button>
        <button type="button" class="export-png-go" id="export-png-go">Exporter <span id="export-png-count"></span></button>
      </div>
    </div>
  </div>
</div>

<!-- ===== APP ===== -->
<div class="app" id="app">

  <!-- ============ EDITOR ============ -->
  <aside class="editor" id="editor">

    <!-- 00 META -->
    <details class="ed-section" data-section="meta" open>
      <summary>00 ░ MÉTADONNÉES</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">00 ░ MÉTADONNÉES</div>
        <div class="ed-field-row">
          <div class="ed-field"><label>Opération</label><input data-bind="meta.operation" type="text" placeholder="FOOTHOLD"></div>
          <div class="ed-field"><label>Mission code</label><input data-bind="meta.mission" type="text" placeholder="M3"></div>
        </div>
        <div class="ed-field-row">
          <div class="ed-field"><label>Date mission</label><input data-bind="meta.date" type="date"></div>
          <div class="ed-field"><label>Classification</label>
            <select data-bind="meta.classification">
              <option>CONFIDENTIEL DÉFENSE</option>
              <option>SECRET DÉFENSE</option>
              <option>TRÈS SECRET</option>
              <option>NON CLASSIFIÉ</option>
              <option>NATO RESTRICTED</option>
              <option>NATO SECRET</option>
            </select>
          </div>
        </div>
        <div class="ed-field"><label>Référence document</label><input data-bind="meta.docRef" type="text" placeholder="KHR26-FH-M3-1989"></div>
        <div class="ed-help">Métadonnées présentes dans tous les pieds de page.</div>
      </div>
    </details>

    <!-- 01 COVER -->
    <details class="ed-section" data-section="cover">
      <summary>01 ░ OPÉRATION (COUVERTURE)</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">01 ░ OPÉRATION</div>
        <div class="ed-field"><label>Titre opération</label><input data-bind="cover.title" type="text" placeholder="OPERATION FOOTHOLD"></div>
        <div class="ed-field"><label>Récit / Contexte</label><textarea data-bind="cover.narrative" rows="6"></textarea></div>
        <div class="ed-field">
          <label>Carte d'opération (image)</label>
          <label class="ed-img-zone" data-img-bind="cover.mapImage">
            <input type="file" accept="image/*">
            <span class="img-text">▲ TOUCHER POUR CHARGER UNE CARTE ▲</span>
          </label>
        </div>
      </div>
    </details>

    <!-- 02 SITAC -->
    <details class="ed-section" data-section="sitac">
      <summary>02 ░ SITAC</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">02 ░ SITAC</div>
        <div class="ed-field"><label>Date SITAC (affichée)</label><input data-bind="sitac.date" type="text" placeholder="22-03-1989"></div>
        <div class="ed-field">
          <label>Points de situation</label>
          <div class="ed-list" data-list="sitac.points"></div>
          <button type="button" class="ed-btn-add" data-add="sitac.points">+ Ajouter un point</button>
        </div>
        <div class="ed-field"><label>METAR</label><input data-bind="sitac.metar" type="text" placeholder="LCRA 221000Z 18002KT 9999 SCT082 20/15 Q1013"></div>
        <div class="ed-field">
          <label>Carte SITAC (image)</label>
          <label class="ed-img-zone" data-img-bind="sitac.mapImage">
            <input type="file" accept="image/*">
            <span class="img-text">▲ TOUCHER POUR CHARGER UNE CARTE ▲</span>
          </label>
        </div>
      </div>
    </details>

    <!-- 03 MISSION -->
    <details class="ed-section" data-section="mission">
      <summary>03 ░ APERÇU MISSION</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">03 ░ APERÇU MISSION</div>
        <div class="ed-field">
          <label>Objectifs principaux</label>
          <div class="ed-list" data-list="mission.objectives"></div>
          <button type="button" class="ed-btn-add" data-add="mission.objectives">+ Ajouter un objectif</button>
        </div>
        <div class="ed-field">
          <label>FARP & Aéroports</label>
          <div class="ed-list" data-list="mission.farp"></div>
          <button type="button" class="ed-btn-add" data-add="mission.farp">+ Ajouter une base</button>
        </div>
        <div class="ed-field-row">
          <div class="ed-field"><label>Menaces — Chars</label><input data-bind="mission.threats.tanks" type="text"></div>
          <div class="ed-field"><label>Menaces — APC</label><input data-bind="mission.threats.apc" type="text"></div>
        </div>
        <div class="ed-field-row">
          <div class="ed-field"><label>Menaces — AAA</label><input data-bind="mission.threats.aaa" type="text"></div>
          <div class="ed-field"><label>Menaces — SAM</label><input data-bind="mission.threats.sam" type="text"></div>
        </div>
        <div class="ed-field"><label>Note menaces (libre)</label><textarea data-bind="mission.threats.note" rows="2"></textarea></div>
      </div>
    </details>

    <!-- 04 RADIO PLAN -->
    <details class="ed-section" data-section="radio" open>
      <summary>04 ░ PLAN RADIO</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">04 ░ PLAN RADIO</div>
        <div class="ed-field">
          <label>Items radio (max 6) — affichés sur la page 3</label>
          <div id="radio-items-list"></div>
          <button type="button" class="ed-btn-add" id="radio-item-add">+ Ajouter un item</button>
        </div>
        <div class="ed-help">Définissez ici les fréquences communes (ATC, MISSION, Groupes...). Vous les assignerez ensuite aux canaux radio par appareil ci-dessous.</div>
        <div class="ed-field" style="margin-top:8px;">
          <label>Plans radio par appareil</label>
          <div id="radio-aircraft-list"></div>
          <button type="button" class="ed-btn-add" id="radio-aircraft-add">+ Ajouter un appareil</button>
        </div>
        <div class="ed-help">Pour chaque appareil, configurez les radios et leurs canaux. Si une image est fournie, elle remplace la table générée.</div>
      </div>
    </details>

    <!-- 05 PHASES -->
    <details class="ed-section" data-section="phases" open>
      <summary>05 ░ MISSIONS</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">05 ░ MISSIONS</div>
        <div class="phase-bar">
          <button type="button" id="phase-prev" title="Mission précédente">◄</button>
          <div class="phase-indicator" id="phase-indicator">—</div>
          <button type="button" id="phase-next" title="Mission suivante">►</button>
          <button type="button" id="phase-add" title="Ajouter une mission">+</button>
          <button type="button" id="phase-dup" title="Dupliquer cette mission">⎘</button>
          <button type="button" id="phase-up" title="Monter la mission">↑</button>
          <button type="button" id="phase-down" title="Descendre la mission">↓</button>
          <button type="button" class="danger" id="phase-rm" title="Supprimer cette mission">×</button>
        </div>
        <div id="phase-editor"></div>
      </div>
    </details>

    <!-- 07 ÉQUIPAGE -->
    <details class="ed-section" data-section="roster">
      <summary>07 ░ ÉQUIPAGE</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">07 ░ ÉQUIPAGE</div>
        <div class="ed-help" style="margin-bottom:10px;">
          Définissez les pilotes par groupe ou sous-groupe. Une page d'ordre de bataille sera générée après l'aperçu mission si au moins un pilote est renseigné.
        </div>
        <div id="roster-groups-list"></div>
        <button type="button" class="ed-btn-add" id="roster-group-add">+ Ajouter un groupe</button>
      </div>
    </details>

    <!-- 08 CHARTS -->
    <details class="ed-section" data-section="charts">
      <summary>08 ░ CHARTS</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">08 ░ CHARTS</div>
        <div id="charts-list"></div>
        <button type="button" class="ed-btn-add" id="chart-add">+ Ajouter une chart</button>
      </div>
    </details>

    <!-- 09 ANNEXES -->
    <details class="ed-section" data-section="annexes">
      <summary>09 ░ ANNEXES</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">09 ░ ANNEXES</div>
        <div id="annexes-list"></div>
        <button type="button" class="ed-btn-add" id="annexe-add">+ Ajouter une annexe</button>
      </div>
    </details>

    <!-- 10 WING -->
    <details class="ed-section" data-section="wing">
      <summary>10 ░ CONFIGURATION WING</summary>
      <div class="ed-content">
        <div class="panel-mobile-header">10 ░ CONFIG WING</div>

        <!-- ── Identité du wing ── -->
        <fieldset class="wing-fieldset">
          <legend class="wing-legend">Identité du wing</legend>

          <div class="ed-field-row">
            <div class="ed-field">
              <label>Nom court <span class="wing-hint">(toolbar, branding)</span></label>
              <input type="text" id="wing-shortName" maxlength="40" placeholder="MY WING">
            </div>
            <div class="ed-field">
              <label>Identifiant <span class="wing-hint">(sans espace ni /)</span></label>
              <input type="text" id="wing-id" maxlength="32" placeholder="MY-WING">
            </div>
          </div>

          <div class="ed-field">
            <label>Nom complet</label>
            <input type="text" id="wing-fullName" maxlength="120" placeholder="Mon Wing Virtuel">
          </div>

          <div class="ed-field-row">
            <div class="ed-field">
              <label>Titre de l'application</label>
              <input type="text" id="wing-appTitle" maxlength="60" placeholder="GÉNÉRATEUR DE BRIEFING">
            </div>
            <div class="ed-field">
              <label>Tampon HQ <span class="wing-hint">(couverture)</span></label>
              <input type="text" id="wing-hqStamp" maxlength="60" placeholder="HQ ░ MY WING">
            </div>
          </div>

          <div class="ed-field">
            <label>Logo wing principal</label>
            <label class="ed-img-zone wing-logo-zone" id="wing-logo-zone">
              <input type="file" accept="image/*" id="wing-logo-input">
              <span class="img-text">▲ TOUCHER POUR CHARGER UN LOGO ▲</span>
            </label>
          </div>
        </fieldset>

        <!-- ── Liste des escadrons ── -->
        <fieldset class="wing-fieldset">
          <legend class="wing-legend">Escadrons</legend>
          <div id="wing-squadrons-list"></div>
          <button type="button" class="ed-btn-add" id="wing-sq-add">+ Ajouter un escadron</button>
        </fieldset>

        <!-- ── Actions ── -->
        <div class="wing-actions">
          <label class="wing-action-btn wing-action-import" title="Importer un fichier wing_config.json">
            <input type="file" accept=".json" id="wing-import-input">
            📥 Importer config
          </label>
          <button type="button" class="wing-action-btn wing-action-export" id="wing-export-btn">
            📤 Exporter config
          </button>
          <button type="button" class="wing-action-btn wing-action-reset" id="wing-reset-btn">
            ♻ Réinitialiser
          </button>
        </div>

        <!-- ── Compteur taille ── -->
        <div class="wing-size-counter" id="wing-size-counter">Taille config : —</div>

      </div>
    </details>

    <div class="ed-help" data-wing-label style="text-align:center; padding:12px 4px;">
      ◆ MY WING ◆<br>
      Sauvegarde locale automatique<br>
      Export JSON pour conserver vos templates
    </div>
  </aside>

  <!-- ============ PREVIEW ============ -->
  <main class="preview-wrap" id="preview-wrap">
    <div id="preview"></div>
  </main>

</div>

<!-- ============ MOBILE TAB BAR ============ -->
<nav class="tab-bar" id="tab-bar" role="tablist" aria-label="Sections du briefing">
  <button type="button" data-tab="meta" role="tab"><span class="tab-ico">⚙</span>Méta</button>
  <button type="button" data-tab="cover" role="tab"><span class="tab-ico">◉</span>Couv.</button>
  <button type="button" data-tab="sitac" role="tab"><span class="tab-ico">▣</span>SITAC</button>
  <button type="button" data-tab="mission" role="tab"><span class="tab-ico">✈</span>Mission</button>
  <button type="button" data-tab="radio" role="tab"><span class="tab-ico">📻</span>Radio</button>
  <button type="button" data-tab="phases" role="tab"><span class="tab-ico">⊕</span>Missions</button>
  <button type="button" data-tab="roster" role="tab"><span class="tab-ico">👤</span>Équipage</button>
  <button type="button" data-tab="charts" role="tab"><span class="tab-ico">🗺</span>Charts</button>
  <button type="button" data-tab="annexes" role="tab"><span class="tab-ico">📎</span>Annexes</button>
  <button type="button" data-tab="wing" role="tab"><span class="tab-ico">🛡</span>Wing</button>
  <button type="button" data-tab="preview" role="tab"><span class="tab-ico">◈</span>Aperçu</button>
</nav>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<!-- ============ EMBEDDED WING CONFIG (generic default) ============ -->
<script>
/* DEFAULT_WING_CONFIG is generated by build_html.py.
   It contains the wing branding + squadrons + base64-encoded logos.
   The 4th VEAW config is distributed separately as wing_config_4th-veaw.json.
   See `wing_config.json` schema in DOCS for the full format. */
const DEFAULT_WING_CONFIG = JSON.parse(__DEFAULT_WING_CONFIG__);
</script>

<!-- ============ APPLICATION ============ -->
<script>
'use strict';

/* =====================================================
   DCS WORLD BRIEFING GENERATOR v2
   Tablet-ready, offline-first
   ===================================================== */

const STORAGE_KEY = 'khr26_briefing_state_v2';
const KEY_WING     = 'wing_config_v1';
const KEY_THEME    = 'theme_v1';
const MOBILE_BREAKPOINT = 1100;
const IMG_MAX_WIDTH = 1600;
const IMG_JPEG_QUALITY = 0.82;

/* ============= WING CONFIG (runtime, mutable) =============
   wingConfig is the single source of truth for wing branding and
   squadron data. At startup it points to DEFAULT_WING_CONFIG (generic);
   the user can load any wing via JSON import or localStorage persistence.
   Helpers (getSquadron, getAllAircraft) ALWAYS read wingConfig.squadrons
   dynamically — never capture a frozen copy. */
let wingConfig = DEFAULT_WING_CONFIG;

function getSquadron(id) { return wingConfig.squadrons.find(s => s.id === id) || null; }

/* All distinct aircraft types across the current wing.
   Function (not constant) so it reflects wingConfig changes at runtime. */
function getAllAircraft() {
  const set = new Set();
  wingConfig.squadrons.forEach(s => s.aircraft.forEach(a => set.add(a)));
  return Array.from(set);
}

const DEFAULTS = {
  meta: {
    operation: 'FOOTHOLD',
    mission: 'M3',
    date: '1989-03-22',
    classification: 'CONFIDENTIEL DÉFENSE',
    docRef: 'VEAW-FH-M3-1989'
  },
  cover: {
    title: 'OPERATION FOOTHOLD',
    narrative: "Les forces soviétiques sont à l'origine du déclenchement d'une guerre civile en Syrie et ont assisté les troupes rebelles pour réussir un coup d'État. Une fois le gouvernement tombé, les forces dissidentes ont envahi l'île de Chypre et capturé la quasi-totalité de l'île, sauf la base OTAN d'AKROTIRI.\n\nLes forces de l'OTAN opèrent un déploiement majeur afin d'assister le gouvernement légitime chypriote à reprendre le contrôle total de l'île. Il n'est pas exclu une opération aéro-navale majeure pour « libérer » la Syrie.",
    mapImage: ''
  },
  sitac: {
    date: '22-03-1989',
    points: [
      "La majorité de l'île reste aux mains de l'ennemi",
      "L'aéroport de PAPHOS a été capturé et ses défenses renforcées",
      "La FARP POLIS a été capturée mais ses défenses sont fragiles",
      "L'adversaire utilise l'aéroport d'ERKAN pour ses contre-offensives (CAP/CAS/SEAD)",
      "Un site de missiles SILKWORM empêche la flotte OTAN de se rapprocher",
      "Le HQ a renforcé POLIS et AKROTIRI avec une unité SAM ROLAND chacune"
    ],
    metar: 'LCRA 221000Z 18002KT 9999 SCT082 20/15 Q1013',
    mapImage: ''
  },
  mission: {
    objectives: [
      "Apporter du ravitaillement à POLIS",
      "Renforcer les défenses de POLIS — Défendre la FARP",
      "Reconnaître et capturer la zone de KARAVOSTASI",
      "Missions secondaires possibles (CSAR, S&D)"
    ],
    farp: [
      "AKROTIRI – Piste en service : 10",
      "PAPHOS – Piste en service : 11"
    ],
    threats: {
      tanks: 'T-55 à T-80',
      apc: 'BRDM-2, BMP-1, BMP-2, BTR-80',
      aaa: 'ZU-57, ZU-23, ZSU-24, S-60, KS-19',
      sam: 'Manpads, SA-8, SA-9, SA-13, Avenger',
      note: 'Pas de SAM longue portée sur Chypre'
    }
  },
  radioPlan: {
    items: [
      { id: 'atc',     label: 'ATC',     frequency: '270.00', modulation: 'AM' },
      { id: 'mission', label: 'MISSION', frequency: '265.00', modulation: 'AM' },
      { id: 'grp1',    label: 'Groupe 1', frequency: '127.50', modulation: 'AM' },
      { id: 'grp2',    label: 'Groupe 2', frequency: '135.00', modulation: 'AM' },
      { id: 'fm1',     label: 'Tactique FM', frequency: '21.50', modulation: 'FM' }
    ],
    aircraftPlans: [
      {
        aircraft: 'Mi-24P',
        radios: [
          {
            name: 'R-863',
            channels: [
              { channel: 0, mode: 'item', itemId: 'grp1' },
              { channel: 1, mode: 'item', itemId: 'grp2' },
              { channel: 3, mode: 'item', itemId: 'mission' },
              { channel: 7, mode: 'item', itemId: 'atc' }
            ]
          },
          {
            name: 'R-828',
            channels: [
              { channel: 0, mode: 'item', itemId: 'fm1' }
            ]
          }
        ],
        image: ''
      },
      {
        aircraft: 'Mi-8',
        radios: [
          {
            name: 'R-863',
            channels: [
              { channel: 4, mode: 'item', itemId: 'mission' },
              { channel: 8, mode: 'item', itemId: 'atc' }
            ]
          },
          {
            name: 'R-828',
            channels: [
              { channel: 1, mode: 'item', itemId: 'fm1' }
            ]
          }
        ],
        image: ''
      }
    ]
  },
  phases: [
    {
      title: 'Ravitaillement POLIS',
      objective: "Ravitailler POLIS en armement pour les Mi-24P",
      execution: [
        {text: "TO PAPHOS — Ravitaillement à POLIS pour Mission #2", subtasks: []},
        {text: "Caisses ATAKA + Roquettes", subtasks: []}
      ],
      flightPlan: 'CAP 352° / Distance 34 Km',
      threatLevel: 'Faible', notes: '', images: [],
      squadron: 'KHR-26', aircraft: 'Mi-8', subgroup: 'ANTON'
    },
    {
      title: 'Défense POLIS — Mi-24P',
      objective: "Les renseignements font état d'un convoi blindé au départ de KARAVOSTASI pour reprendre POLIS",
      execution: [
        {text: "TO POLIS", subtasks: []},
        {text: "Suivre le chemin côtier de POLIS jusque KARAVOSTASI", subtasks: []}
      ],
      flightPlan: "Chemin côtier jusqu'à l'IP Mission #3",
      threatLevel: 'Élevé', notes: 'Route estimée du convoi : voir carte phase 2', images: [],
      squadron: 'KHR-26', aircraft: 'Mi-24P', subgroup: 'CAESAR'
    },
    {
      title: 'RECO + ASSAUT KARAVOSTASI',
      objective: "Préparer la capture de la zone par les troupes aéroportées. Destruction des défenses SAM/AAA et des éléments blindés",
      execution: [
        {text: "TO POLIS — Retour selon SITAC", subtasks: []},
        {text: "Rassemblement à l'IP", subtasks: []},
        {text: "Cibles prioritaires : SAM / AAA", subtasks: ["SA-13", "SA-9", "Manpads"]},
        {text: "Cibles secondaires : APC / MBT", subtasks: []}
      ],
      flightPlan: 'IP : 59° / 32 Km — TGT : 118° / 9 Km',
      threatLevel: 'Élevé', notes: "Repère : petite île + rivière à 8/9 Km de KARAVOSTASI. Axe d'assaut le long de la côte.",
      images: [], squadron: 'KHR-26', aircraft: 'Mi-24P', subgroup: ''
    }
  ],
  charts: [
    { name: 'AKROTIRI (LCRA) — Piste en service : 10', img: '' },
    { name: 'PAPHOS (LCPH) — Piste en service : 11', img: '' }
  ],
  annexes: [],
  roster: {
    groups: []   // { missionKey: 'KHR-26||CAESAR||Mi-24P', pilots: [{name,aircraft,callsign}] }
  }
};

let state;
let currentPhaseIdx = 0;
let activeTab = 'meta';

/* ============= STATE / PERSISTENCE ============= */
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      state = mergeDeep(structuredClone(DEFAULTS), parsed);
      if (Array.isArray(state.phases)) {
        state.phases.forEach(ph => {
          ph.execution = normalizeExecution(ph.execution);
          normalizePhaseImages(ph);
          ph.threatLevel = normalizeThreatLevel(ph.threatLevel);
        });
      }
      normalizeCharts(state);
      normalizeAnnexes(state);
      return;
    }
  } catch(e) { console.warn('Storage load failed:', e); }
  state = structuredClone(DEFAULTS);
}

function persistState() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  catch(e) { /* localStorage may be unavailable or full */ }
}

/* ============= WING CONFIG PERSISTENCE ============= */

/* Validates a candidate wing config object.
   Returns { ok: true } or { ok: false, errors: string[] }.
   Called both at import and at localStorage load to guard against corruption. */
function validateWingConfig(obj) {
  const errors = [];
  if (!obj || typeof obj !== 'object') return { ok: false, errors: ['Objet invalide'] };
  if (obj.configSchemaVersion !== 1)
    errors.push('configSchemaVersion doit être 1');
  if (!obj.wing || typeof obj.wing !== 'object') {
    errors.push('Champ wing manquant');
  } else {
    if (!obj.wing.shortName)
      errors.push('wing.shortName manquant');
    if (!obj.wing.logo || !String(obj.wing.logo).startsWith('data:image/'))
      errors.push('wing.logo doit être une data URL image valide (data:image/…)');
  }
  if (!Array.isArray(obj.squadrons)) {
    errors.push('squadrons doit être un tableau');
  } else {
    obj.squadrons.forEach((sq, i) => {
      if (!sq.id)                      errors.push('squadrons[' + i + '].id manquant');
      if (!sq.callsign)                errors.push('squadrons[' + i + '].callsign manquant');
      if (!Array.isArray(sq.aircraft)) errors.push('squadrons[' + i + '].aircraft doit être un tableau');
    });
  }
  return errors.length === 0 ? { ok: true } : { ok: false, errors };
}

/* Reads wing config from localStorage.
   Returns DEFAULT_WING_CONFIG (deep-cloned) if absent or invalid. */
function loadWingConfig() {
  try {
    const raw = localStorage.getItem(KEY_WING);
    if (raw) {
      const parsed = JSON.parse(raw);
      const check = validateWingConfig(parsed);
      if (check.ok) return parsed;
      console.warn('[Wing] Config localStorage invalide — utilisation du défaut :', check.errors);
    }
  } catch(e) { console.warn('[Wing] Lecture localStorage échouée :', e); }
  return structuredClone(DEFAULT_WING_CONFIG);
}

/* Debounced write of wingConfig to localStorage (200 ms).
   Called by the wing editor UI after every user change.
   Not called automatically — only the editor triggers persistence. */
let _wingPersistTimer = null;
function persistWingConfig() {
  if (_wingPersistTimer) clearTimeout(_wingPersistTimer);
  _wingPersistTimer = setTimeout(() => {
    try {
      localStorage.setItem(KEY_WING, JSON.stringify(wingConfig));
    } catch(e) {
      if (e.name === 'QuotaExceededError') {
        showToast('⚠ Espace de stockage saturé — exportez votre wing puis réinitialisez');
      } else {
        console.warn('[Wing] Erreur persistance :', e);
      }
    }
  }, 200);
}

function mergeDeep(target, source) {
  for (const k of Object.keys(source || {})) {
    if (source[k] && typeof source[k] === 'object' && !Array.isArray(source[k])) {
      target[k] = mergeDeep(target[k] || {}, source[k]);
    } else {
      target[k] = source[k];
    }
  }
  return target;
}

function getByPath(obj, path) {
  return path.split('.').reduce((o, k) => o == null ? undefined : o[k], obj);
}
function setByPath(obj, path, val) {
  const keys = path.split('.');
  let o = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    if (o[keys[i]] == null) o[keys[i]] = {};
    o = o[keys[i]];
  }
  o[keys[keys.length - 1]] = val;
}

/* ============= IMAGE COMPRESSION ============= */
function compressImageFile(file) {
  return new Promise((resolve, reject) => {
    if (!file.type.startsWith('image/')) {
      reject(new Error('Le fichier doit être une image.'));
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        try {
          let { width, height } = img;
          if (width > IMG_MAX_WIDTH) {
            height = Math.round(height * IMG_MAX_WIDTH / width);
            width = IMG_MAX_WIDTH;
          }
          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, width, height);
          ctx.drawImage(img, 0, 0, width, height);
          const dataUrl = canvas.toDataURL('image/jpeg', IMG_JPEG_QUALITY);
          resolve({ dataUrl, width, height });
        } catch (e) { reject(e); }
      };
      img.onerror = () => reject(new Error('Image illisible.'));
      img.src = reader.result;
    };
    reader.onerror = () => reject(new Error('Lecture du fichier impossible.'));
    reader.readAsDataURL(file);
  });
}

/* ============= EDITOR RENDERING ============= */
function renderEditorBindings() {
  document.querySelectorAll('[data-bind]').forEach(input => {
    const v = getByPath(state, input.dataset.bind);
    if (v != null) input.value = v;
  });

  document.querySelectorAll('[data-img-bind]').forEach(zone => {
    refreshImgZone(zone);
  });

  document.querySelectorAll('[data-list]').forEach(container => {
    renderList(container);
  });

  renderPhaseEditor();
  renderRadioPlan();
  renderRoster();
  renderCharts();
  renderAnnexes();   // nouveau
  renderWingEditor();  // populate wing editor inputs and squadron list
}

/* Returns all unique squadron+subgroup+aircraft combos from missions */
function getMissionGroups() {
  const seen = new Map();
  (state.phases || []).forEach(ph => {
    const info = getPhaseSquadronInfo(ph);
    if (!info) return;
    const key = `${info.id}||${info.subgroup}||${info.aircraft}`;
    if (!seen.has(key)) {
      seen.set(key, {
        key,
        id: info.id,
        callsign: info.callsign,
        aircraft: info.aircraft,
        subgroup: info.subgroup,
        isGuest: info.isGuest
      });
    }
  });
  return Array.from(seen.values());
}

/* Compute human-readable label from a missionGroup object or missionKey string.
   - shortLabel : for callsign prefix   (e.g. "Anton", "Duff", "Wolf")
   - label      : group name            (e.g. "KHR-26 ░ ANTON", "WOLF ░ WOLF 1")
   - fullLabel  : with aircraft         (e.g. "KHR-26 ░ ANTON — Mi-8")
   
   Both standard and guest use the same logic:
     label = id [░ subgroup_or_callsign]
   For guests, id = guest squadron name (e.g. "WOLF"), callsign = same.
   Subgroup optional for both types.
*/
function getRosterLabelParts(keyOrGroup) {
  const g = (typeof keyOrGroup === 'string')
    ? getMissionGroups().find(x => x.key === keyOrGroup)
    : keyOrGroup;
  if (!g) return { shortLabel: keyOrGroup || '—', label: keyOrGroup || '—', fullLabel: keyOrGroup || '—' };

  // Unified logic: id + optional (subgroup or callsign)
  // For guests:   id = guest_name, callsign = guest_name → show subgroup if distinct
  // For standard: id = squadron_id, callsign = group_name (FRANKEN), subgroup replaces callsign
  let identifier;
  if (g.isGuest) {
    // Guest: subgroup if different from id (e.g. "WOLF 1" when id = "WOLF")
    identifier = (g.subgroup && g.subgroup !== g.id) ? g.subgroup : null;
  } else {
    // Standard: subgroup replaces callsign
    identifier = g.subgroup || (g.callsign !== g.id ? g.callsign : null);
  }
  const label = g.id + (identifier ? ' ░ ' + identifier : '');

  // Short label for auto-callsign: subgroup if defined, else id
  const shortLabel = identifier || g.id;
  const fullLabel = label + (g.aircraft ? ' — ' + g.aircraft : '');

  return { shortLabel, label, fullLabel };
}

function getRosterLabel(keyOrGroup) {
  return getRosterLabelParts(keyOrGroup).label;
}
function getRosterFullLabel(keyOrGroup) {
  return getRosterLabelParts(keyOrGroup).fullLabel;
}
function getRosterShortLabel(keyOrGroup) {
  return getRosterLabelParts(keyOrGroup).shortLabel;
}

/* ============= ROSTER (ÉQUIPAGE) EDITOR ============= */
function renderRoster() {
  const list = document.getElementById('roster-groups-list');
  const addBtn = document.getElementById('roster-group-add');
  if (!list) return;
  if (!state.roster) state.roster = { groups: [] };

  const missionGroups = getMissionGroups();
  const usedKeys = new Set(state.roster.groups.map(g => g.missionKey));
  const available = missionGroups.filter(g => !usedKeys.has(g.key));
  if (addBtn) addBtn.disabled = available.length === 0;

  list.innerHTML = '';

  if (missionGroups.length === 0) {
    const warn = document.createElement('div');
    warn.className = 'phase-empty';
    warn.innerHTML = '⚠ Aucune mission définie. Renseignez des missions avec des escadrons pour créer des groupes d\'équipage.';
    list.appendChild(warn);
    return;
  }

  if (state.roster.groups.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'phase-empty';
    empty.textContent = 'Aucun groupe. Toucher « + Ajouter un groupe ».';
    list.appendChild(empty);
    return;
  }

  state.roster.groups.forEach((grp, gi) => {
    const parts = getRosterLabelParts(grp.missionKey);

    const card = document.createElement('div');
    card.className = 'ed-phase-card';

    // SELECT options — all mission groups, disable already-used ones (except self)
    const opts = getMissionGroups().map(g => {
      const isUsedElsewhere = usedKeys.has(g.key) && g.key !== grp.missionKey;
      const p = getRosterLabelParts(g);
      return `<option value="${escapeAttr(g.key)}" ${isUsedElsewhere ? 'disabled' : ''} ${g.key === grp.missionKey ? 'selected' : ''}>
        ${escapeHtml(p.fullLabel)}
      </option>`;
    }).join('');

    card.innerHTML = `
      <div class="phase-num">GROUPE ${gi + 1}</div>
      <button type="button" class="phase-rm" data-grp-rm="${gi}">Suppr.</button>
      <div class="ed-field" style="margin-top:8px;">
        <label>Groupe / sous-groupe (depuis les missions)</label>
        <select class="roster-grp-select">
          <option value="">— Sélectionner un groupe —</option>
          ${opts}
        </select>
      </div>
      <div class="ed-field">
        <label>Pilotes</label>
        <div class="roster-pilots-list"></div>
        <button type="button" class="ed-btn-add" data-pilot-add="${gi}">+ Ajouter un pilote</button>
      </div>
    `;
    list.appendChild(card);

    card.querySelector('.roster-grp-select').addEventListener('change', e => {
      state.roster.groups[gi].missionKey = e.target.value;
      renderRoster(); schedulePreview();
    });

    card.querySelector(`[data-grp-rm="${gi}"]`).addEventListener('click', () => {
      if (!confirm('Supprimer ce groupe ?')) return;
      state.roster.groups.splice(gi, 1);
      renderRoster(); schedulePreview();
    });

    renderPilots(card.querySelector('.roster-pilots-list'), gi);

    card.querySelector(`[data-pilot-add="${gi}"]`).addEventListener('click', () => {
      // Auto-generate callsign: shortLabel + " 1-" + (n+1)
      const n = state.roster.groups[gi].pilots.length;
      const prefix = parts.shortLabel;
      const autoCallsign = `${prefix} 1-${n + 1}`;
      state.roster.groups[gi].pilots.push({ name: '', callsign: autoCallsign });
      renderPilots(card.querySelector('.roster-pilots-list'), gi);
      schedulePreview();
    });
  });
}

function renderPilots(container, gi) {
  if (!container) return;
  const pilots = state.roster.groups[gi].pilots;
  container.innerHTML = '';

  if (pilots.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'phase-empty';
    empty.style.fontSize = '11px';
    empty.textContent = 'Aucun pilote.';
    container.appendChild(empty);
    return;
  }

  pilots.forEach((pilot, pi) => {
    const row = document.createElement('div');
    row.className = 'roster-pilot-row';
    row.innerHTML = `
      <input type="text" class="rp-name"    placeholder="Nom / indicatif pilote" value="${escapeAttr(pilot.name || '')}">
      <input type="text" class="rp-callsign" placeholder="Callsign"              value="${escapeAttr(pilot.callsign || '')}">
      <button type="button" class="ed-btn-icon" data-pilot-rm="${pi}">×</button>
    `;
    container.appendChild(row);

    row.querySelector('.rp-name').addEventListener('input', e => {
      state.roster.groups[gi].pilots[pi].name = e.target.value; schedulePreview();
    });
    row.querySelector('.rp-callsign').addEventListener('input', e => {
      state.roster.groups[gi].pilots[pi].callsign = e.target.value; schedulePreview();
    });
    row.querySelector(`[data-pilot-rm="${pi}"]`).addEventListener('click', () => {
      state.roster.groups[gi].pilots.splice(pi, 1);
      renderPilots(container, gi); schedulePreview();
    });
  });
}

/* ============= RADIO PLAN EDITOR ============= */
const RADIO_ITEMS_MAX = 6;
const RADIO_AIRCRAFT_MAX = 6;
const RADIO_RADIOS_MAX = 3;
const RADIO_CHANNELS_MAX = 12;

function genId(prefix) {
  return prefix + '_' + Math.random().toString(36).slice(2, 8);
}

function ensureRadioPlanShape() {
  if (!state.radioPlan) state.radioPlan = { items: [], aircraftPlans: [] };
  if (!Array.isArray(state.radioPlan.items)) state.radioPlan.items = [];
  if (!Array.isArray(state.radioPlan.aircraftPlans)) state.radioPlan.aircraftPlans = [];
  state.radioPlan.items.forEach(it => { if (!it.id) it.id = genId('it'); });
}

function renderRadioPlan() {
  ensureRadioPlanShape();
  renderRadioItems();
  renderRadioAircrafts();
}

function renderRadioItems() {
  const list = document.getElementById('radio-items-list');
  if (!list) return;
  list.innerHTML = '';
  const items = state.radioPlan.items;
  const addBtn = document.getElementById('radio-item-add');
  if (addBtn) addBtn.disabled = items.length >= RADIO_ITEMS_MAX;

  items.forEach((it, i) => {
    const row = document.createElement('div');
    row.className = 'ed-radio-item-row';
    row.innerHTML = `
      <input type="text" data-ri-label placeholder="Libellé (ex: ATC)">
      <input type="text" data-ri-freq placeholder="Fréq.">
      <select data-ri-mod>
        <option value="AM">AM</option>
        <option value="FM">FM</option>
      </select>
      <button type="button" class="ed-btn-icon" data-ri-rm aria-label="Supprimer">×</button>
    `;
    row.querySelector('[data-ri-label]').value = it.label || '';
    row.querySelector('[data-ri-freq]').value = it.frequency || '';
    row.querySelector('[data-ri-mod]').value = it.modulation || 'AM';

    row.querySelector('[data-ri-label]').addEventListener('input', e => {
      items[i].label = e.target.value;
      schedulePreview();
    });
    row.querySelector('[data-ri-freq]').addEventListener('input', e => {
      items[i].frequency = e.target.value;
      schedulePreview();
    });
    row.querySelector('[data-ri-mod]').addEventListener('change', e => {
      items[i].modulation = e.target.value;
      schedulePreview();
    });
    row.querySelector('[data-ri-rm]').addEventListener('click', () => {
      const removedId = items[i].id;
      items.splice(i, 1);
      // Clean up references in aircraftPlans
      state.radioPlan.aircraftPlans.forEach(ap => {
        (ap.radios || []).forEach(r => {
          (r.channels || []).forEach(ch => {
            if (ch.itemId === removedId) ch.itemId = '';
          });
        });
      });
      renderRadioPlan();
      schedulePreview();
    });
    list.appendChild(row);
  });

  if (items.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'phase-empty';
    empty.textContent = 'Aucun item radio. Touchez « + Ajouter un item ».';
    list.appendChild(empty);
  }
}

function renderRadioAircrafts() {
  const list = document.getElementById('radio-aircraft-list');
  if (!list) return;
  list.innerHTML = '';
  const plans = state.radioPlan.aircraftPlans;
  const addBtn = document.getElementById('radio-aircraft-add');
  if (addBtn) addBtn.disabled = plans.length >= RADIO_AIRCRAFT_MAX;

  if (plans.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'phase-empty';
    empty.textContent = 'Aucun appareil configuré. Touchez « + Ajouter un appareil ».';
    list.appendChild(empty);
    return;
  }

  plans.forEach((ap, ai) => {
    const card = document.createElement('div');
    card.className = 'ed-phase-card';
    card.innerHTML = `
      <div class="phase-num">APPAREIL ${ai + 1}</div>
      <button type="button" class="phase-rm" data-ap-rm="${ai}">Suppr.</button>
      <div class="ed-field"><label>Type d'appareil</label>
        <select data-ap-aircraft="${ai}">
          ${getAllAircraft().map(a => `<option value="${escapeAttr(a)}">${escapeHtml(a)}</option>`).join('')}
          <option value="__custom__">— Autre (libre) —</option>
        </select>
      </div>
      <div class="ed-field" data-ap-custom-wrap="${ai}" style="display:none;">
        <label>Nom personnalisé</label>
        <input type="text" data-ap-custom="${ai}">
      </div>
      <div class="ed-field">
        <label>Image radio (optionnelle — remplace la table)</label>
        <label class="ed-img-zone" data-img-bind="radioPlan.aircraftPlans.${ai}.image">
          <input type="file" accept="image/*">
          <span class="img-text">▲ CHARGER IMAGE ▲</span>
        </label>
      </div>
      <div class="ed-field" data-radios-wrap="${ai}">
        <label>Radios &amp; canaux</label>
        <div data-radios-list="${ai}"></div>
        <button type="button" class="ed-btn-add" data-radio-add="${ai}">+ Ajouter une radio</button>
      </div>
    `;
    list.appendChild(card);

    // Set aircraft selector
    const acSel = card.querySelector(`[data-ap-aircraft="${ai}"]`);
    const isCustom = !getAllAircraft().includes(ap.aircraft) && ap.aircraft;
    if (isCustom) {
      acSel.value = '__custom__';
      const wrap = card.querySelector(`[data-ap-custom-wrap="${ai}"]`);
      const cust = card.querySelector(`[data-ap-custom="${ai}"]`);
      wrap.style.display = '';
      cust.value = ap.aircraft;
    } else if (ap.aircraft) {
      acSel.value = ap.aircraft;
    }

    acSel.addEventListener('change', () => {
      const wrap = card.querySelector(`[data-ap-custom-wrap="${ai}"]`);
      if (acSel.value === '__custom__') {
        wrap.style.display = '';
        const cust = card.querySelector(`[data-ap-custom="${ai}"]`);
        plans[ai].aircraft = cust.value || '';
      } else {
        wrap.style.display = 'none';
        plans[ai].aircraft = acSel.value;
      }
      schedulePreview();
    });
    card.querySelector(`[data-ap-custom="${ai}"]`).addEventListener('input', e => {
      plans[ai].aircraft = e.target.value;
      schedulePreview();
    });

    card.querySelector(`[data-ap-rm="${ai}"]`).addEventListener('click', () => {
      if (!confirm(`Supprimer la configuration radio de l'appareil ${ai + 1} ?`)) return;
      plans.splice(ai, 1);
      renderRadioAircrafts();
      schedulePreview();
    });

    // If image set, dim radios area and add note
    const radiosWrap = card.querySelector(`[data-radios-wrap="${ai}"]`);
    if (ap.image) {
      radiosWrap.style.opacity = '0.5';
      const note = document.createElement('div');
      note.className = 'ed-help';
      note.style.color = 'var(--amber)';
      note.textContent = '⚠ Image fournie : la table sera remplacée par l\'image dans le briefing.';
      radiosWrap.insertBefore(note, radiosWrap.firstChild);
    }

    // Render radios
    renderAircraftRadios(card.querySelector(`[data-radios-list="${ai}"]`), ai);

    card.querySelector(`[data-radio-add="${ai}"]`).addEventListener('click', () => {
      if (!plans[ai].radios) plans[ai].radios = [];
      if (plans[ai].radios.length >= RADIO_RADIOS_MAX) return;
      plans[ai].radios.push({ name: 'R-???', channels: [] });
      renderRadioAircrafts();
      schedulePreview();
    });

    refreshImgZone(card.querySelector(`[data-img-bind="radioPlan.aircraftPlans.${ai}.image"]`));
  });
}

function renderAircraftRadios(container, ai) {
  const ap = state.radioPlan.aircraftPlans[ai];
  container.innerHTML = '';
  (ap.radios || []).forEach((r, ri) => {
    const block = document.createElement('div');
    block.className = 'ed-radio-block';
    block.innerHTML = `
      <div class="ed-radio-block-head">
        <input type="text" data-r-name placeholder="Nom radio (R-863, UHF, ...)">
        <button type="button" class="ed-btn-icon" data-r-rm aria-label="Supprimer radio">×</button>
      </div>
      <div data-channels-list class="ed-channels-list"></div>
      <button type="button" class="ed-btn-add ed-btn-add-sm" data-channel-add>+ Canal</button>
    `;
    block.querySelector('[data-r-name]').value = r.name || '';
    block.querySelector('[data-r-name]').addEventListener('input', e => {
      r.name = e.target.value;
      schedulePreview();
    });
    block.querySelector('[data-r-rm]').addEventListener('click', () => {
      ap.radios.splice(ri, 1);
      renderRadioAircrafts();
      schedulePreview();
    });

    const chList = block.querySelector('[data-channels-list]');
    renderChannels(chList, ai, ri);

    block.querySelector('[data-channel-add]').addEventListener('click', () => {
      if (!r.channels) r.channels = [];
      if (r.channels.length >= RADIO_CHANNELS_MAX) return;
      r.channels.push({ channel: r.channels.length, itemId: '' });
      renderChannels(chList, ai, ri);
      schedulePreview();
    });
    container.appendChild(block);
  });
}

function renderChannels(container, ai, ri) {
  const r = state.radioPlan.aircraftPlans[ai].radios[ri];
  container.innerHTML = '';
  const items = state.radioPlan.items;

  (r.channels || []).forEach((ch, ci) => {
    // Normalize legacy channels without mode field
    if (!ch.mode) ch.mode = 'item';
    const isCustom = ch.mode === 'custom';

    const row = document.createElement('div');
    row.className = 'ed-channel-row' + (isCustom ? ' custom-mode' : '');

    // Toggle button (tablet-friendly, always first cell)
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'ed-ch-toggle' + (isCustom ? ' is-custom' : '');
    toggleBtn.textContent = isCustom ? 'FR' : 'IT';
    toggleBtn.title = isCustom ? 'Fréquence libre — tap pour passer en Item global' : 'Item global — tap pour passer en Fréquence libre';
    toggleBtn.addEventListener('click', () => {
      if (ch.mode === 'custom') {
        ch.mode = 'item';
        delete ch.label; delete ch.frequency; delete ch.modulation;
        if (!ch.itemId) ch.itemId = '';
      } else {
        ch.mode = 'custom';
        ch.label = ''; ch.frequency = ''; ch.modulation = 'AM';
        ch.itemId = '';
      }
      renderChannels(container, ai, ri);
      schedulePreview();
    });
    row.appendChild(toggleBtn);

    // Channel number input
    const chNumInput = document.createElement('input');
    chNumInput.type = 'number';
    chNumInput.placeholder = 'Ch.';
    chNumInput.min = '0';
    chNumInput.value = ch.channel ?? '';
    chNumInput.addEventListener('input', e => {
      const v = e.target.value;
      ch.channel = v === '' ? '' : parseInt(v, 10);
      schedulePreview();
    });
    row.appendChild(chNumInput);

    if (isCustom) {
      // Label input
      const labelInput = document.createElement('input');
      labelInput.type = 'text';
      labelInput.placeholder = 'Libellé';
      labelInput.value = ch.label || '';
      labelInput.addEventListener('input', e => { ch.label = e.target.value; schedulePreview(); });
      row.appendChild(labelInput);

      // Frequency input
      const freqInput = document.createElement('input');
      freqInput.type = 'text';
      freqInput.placeholder = 'Fréq.';
      freqInput.value = ch.frequency || '';
      freqInput.addEventListener('input', e => { ch.frequency = e.target.value; schedulePreview(); });
      row.appendChild(freqInput);

      // Modulation select
      const modSel = document.createElement('select');
      modSel.innerHTML = '<option value="AM">AM</option><option value="FM">FM</option>';
      modSel.value = ch.modulation || 'AM';
      modSel.addEventListener('change', e => { ch.modulation = e.target.value; schedulePreview(); });
      row.appendChild(modSel);
    } else {
      // Item select
      const opts = ['<option value="">— Item —</option>']
        .concat(items.map(it => `<option value="${escapeAttr(it.id)}">${escapeHtml(it.label || '?')}</option>`))
        .join('');
      const itemSel = document.createElement('select');
      itemSel.innerHTML = opts;
      itemSel.value = ch.itemId || '';
      itemSel.addEventListener('change', e => { ch.itemId = e.target.value; schedulePreview(); });
      row.appendChild(itemSel);
    }

    // Delete button
    const rmBtn = document.createElement('button');
    rmBtn.type = 'button';
    rmBtn.className = 'ed-btn-icon';
    rmBtn.setAttribute('aria-label', 'Supprimer canal');
    rmBtn.textContent = '×';
    rmBtn.addEventListener('click', () => {
      r.channels.splice(ci, 1);
      renderChannels(container, ai, ri);
      schedulePreview();
    });
    row.appendChild(rmBtn);

    container.appendChild(row);
  });
}

function renderList(container) {
  const path = container.dataset.list;
  const items = getByPath(state, path) || [];
  container.innerHTML = '';
  items.forEach((val, i) => {
    const row = document.createElement('div');
    row.className = 'ed-list-item';
    const isLong = (val || '').length > 60;
    if (isLong) {
      row.innerHTML = `<textarea rows="2"></textarea><button type="button" class="ed-btn-icon" aria-label="Supprimer">×</button>`;
      row.querySelector('textarea').value = val;
    } else {
      row.innerHTML = `<input type="text"><button type="button" class="ed-btn-icon" aria-label="Supprimer">×</button>`;
      row.querySelector('input').value = val;
    }
    const inp = row.querySelector('input,textarea');
    inp.addEventListener('input', () => {
      const arr = getByPath(state, path);
      arr[i] = inp.value;
      schedulePreview();
    });
    row.querySelector('button').addEventListener('click', () => {
      const arr = getByPath(state, path);
      arr.splice(i, 1);
      renderList(container);
      schedulePreview();
    });
    container.appendChild(row);
  });
}

/* PHASE EDITOR (single-phase view with selector) */
function renderPhaseEditor() {
  const container = document.getElementById('phase-editor');
  const indicator = document.getElementById('phase-indicator');
  const total = state.phases.length;

  // clamp index
  if (currentPhaseIdx >= total) currentPhaseIdx = Math.max(0, total - 1);
  if (currentPhaseIdx < 0) currentPhaseIdx = 0;

  // disable nav buttons when applicable
  document.getElementById('phase-prev').disabled = currentPhaseIdx === 0 || total === 0;
  document.getElementById('phase-next').disabled = currentPhaseIdx >= total - 1 || total === 0;
  document.getElementById('phase-rm').disabled = total === 0;
  document.getElementById('phase-dup').disabled = total === 0;
  document.getElementById('phase-up').disabled = currentPhaseIdx === 0 || total === 0;
  document.getElementById('phase-down').disabled = currentPhaseIdx >= total - 1 || total === 0;

  if (total === 0) {
    indicator.innerHTML = `<strong>0</strong> / 0`;
    container.innerHTML = `<div class="phase-empty">Aucune mission définie.<br>Touchez <strong>+</strong> pour ajouter une mission.</div>`;
    return;
  }

  indicator.innerHTML = `Mission <strong>${currentPhaseIdx + 1}</strong> / ${total}`;

  const ph = state.phases[currentPhaseIdx];
  const i = currentPhaseIdx;

  // Build squadron options — known + guest option
  const sqOptions = ['<option value="">— Aucun escadron —</option>']
    .concat(wingConfig.squadrons.map(s => {
      const aircraftLabel = s.aircraft.length === 1 ? s.aircraft[0] : s.aircraft.join(' / ');
      return `<option value="${s.id}">${escapeHtml(s.id)} ${escapeHtml(s.callsign)} — ${escapeHtml(aircraftLabel)}</option>`;
    }))
    .concat(['<option value="__guest__">— Escadron invité... —</option>'])
    .join('');

  const isGuest = ph.squadron === '__guest__';
  const selectedSq = isGuest ? null : getSquadron(ph.squadron);
  const showAircraftSelector = !isGuest && selectedSq && selectedSq.aircraft.length > 1;

  let aircraftSelectorHtml = '';
  if (showAircraftSelector) {
    const acOpts = selectedSq.aircraft.map(a => `<option value="${escapeAttr(a)}">${escapeHtml(a)}</option>`).join('');
    aircraftSelectorHtml = `
      <div class="ed-field"><label>Appareil utilisé</label>
        <select id="pf-aircraft">${acOpts}</select>
      </div>`;
  }

  // Guest fields
  const guestData = ph.guestSquadron || { name: '', subgroup: '', aircraft: '' };
  const guestFieldsHtml = isGuest ? `
    <div class="ed-guest-fields">
      <div class="ed-field"><label>Nom de l'escadron</label>
        <input id="pf-guest-name" type="text" value="${escapeAttr(guestData.name)}" placeholder="Ex: WOLF">
      </div>
      <div class="ed-field"><label>Nom du groupe</label>
        <input id="pf-guest-sub" type="text" value="${escapeAttr(guestData.subgroup)}" placeholder="Ex: WOLF 1 (optionnel)">
      </div>
      <div class="ed-field"><label>Type d'appareil</label>
        <input id="pf-guest-aircraft" type="text" value="${escapeAttr(guestData.aircraft)}" placeholder="Ex: F-16CM">
      </div>
    </div>` : '';

  container.innerHTML = `
    <div class="ed-field"><label>Titre de la mission</label><input id="pf-title" type="text" value="${escapeAttr(ph.title || '')}"></div>
    <div class="ed-field"><label>Escadron affecté</label>
      <select id="pf-squadron">${sqOptions}</select>
    </div>
    ${guestFieldsHtml}
    ${aircraftSelectorHtml}
    <div class="ed-field"><label>Sous-groupe <span class="ed-label-hint">(optionnel)</span></label>
      <input id="pf-subgroup" type="text" value="${escapeAttr(ph.subgroup || '')}" placeholder="Ex: ANTON, CAESAR, WOLF 2...">
    </div>
    <div class="ed-field"><label>Objectif</label><textarea id="pf-objective" rows="3">${escapeHtml(ph.objective || '')}</textarea></div>
    <div class="ed-field">
      <label>Étapes d'exécution</label>
      <div class="ed-list" id="phase-exec-list"></div>
      <button type="button" class="ed-btn-add" id="phase-exec-add">+ Ajouter une étape</button>
    </div>
    <div class="ed-field-row">
      <div class="ed-field"><label>Plan de vol</label><input id="pf-flightPlan" type="text" value="${escapeAttr(ph.flightPlan || '')}"></div>
      <div class="ed-field"><label>Niveau de menace</label>
        <select id="pf-threatLevel">
          <option>Faible</option><option>Modéré</option><option>Élevé</option>
        </select>
      </div>
    </div>
    <div class="ed-field"><label>Notes / repères tactiques</label><textarea id="pf-notes" rows="3">${escapeHtml(ph.notes || '')}</textarea></div>
    <div class="ed-field">
      <label>Images de mission (pages dédiées, 2 par page)</label>
      <div class="ed-img-list" id="phase-images-list"></div>
      <button type="button" class="ed-btn-add" id="phase-img-add">+ Ajouter une image</button>
    </div>
  `;

  // Set select values
  container.querySelector('#pf-threatLevel').value = ph.threatLevel || 'Faible';
  container.querySelector('#pf-squadron').value = ph.squadron || '';
  if (showAircraftSelector) {
    container.querySelector('#pf-aircraft').value = ph.aircraft || selectedSq.aircraft[0];
  }

  // Bind text/textarea fields
  ['title', 'objective', 'flightPlan', 'threatLevel', 'notes'].forEach(field => {
    const el = container.querySelector(`#pf-${field}`);
    if (!el) return;
    el.addEventListener('input', () => { state.phases[i][field] = el.value; schedulePreview(); });
    if (el.tagName === 'SELECT') {
      el.addEventListener('change', () => { state.phases[i][field] = el.value; schedulePreview(); });
    }
  });

  // Subgroup
  const subgroupEl = container.querySelector('#pf-subgroup');
  subgroupEl.addEventListener('input', () => { state.phases[i].subgroup = subgroupEl.value; schedulePreview(); renderRoster(); });

  // Guest fields
  if (isGuest) {
    if (!state.phases[i].guestSquadron) state.phases[i].guestSquadron = { name: '', subgroup: '', aircraft: '' };
    container.querySelector('#pf-guest-name').addEventListener('input', e => {
      state.phases[i].guestSquadron.name = e.target.value; schedulePreview(); renderRoster();
    });
    container.querySelector('#pf-guest-sub').addEventListener('input', e => {
      state.phases[i].guestSquadron.subgroup = e.target.value; schedulePreview(); renderRoster();
    });
    container.querySelector('#pf-guest-aircraft').addEventListener('input', e => {
      state.phases[i].guestSquadron.aircraft = e.target.value; schedulePreview(); renderRoster();
    });
  }

  // Squadron selector re-render on change
  container.querySelector('#pf-squadron').addEventListener('change', e => {
    const newSqId = e.target.value;
    state.phases[i].squadron = newSqId;
    if (newSqId === '__guest__') {
      if (!state.phases[i].guestSquadron) state.phases[i].guestSquadron = { name: '', subgroup: '', aircraft: '' };
      state.phases[i].aircraft = '';
    } else {
      const newSq = getSquadron(newSqId);
      if (!newSq) state.phases[i].aircraft = '';
      else if (newSq.aircraft.length === 1) state.phases[i].aircraft = newSq.aircraft[0];
      else if (!newSq.aircraft.includes(state.phases[i].aircraft)) state.phases[i].aircraft = newSq.aircraft[0];
    }
    renderPhaseEditor(); schedulePreview(); renderRoster();
  });

  // Aircraft selector (multi-aircraft squadrons only)
  const acSel = container.querySelector('#pf-aircraft');
  if (acSel) {
    acSel.addEventListener('change', e => { state.phases[i].aircraft = e.target.value; schedulePreview(); renderRoster(); });
  }

  // Exec list
  const execList = container.querySelector('#phase-exec-list');
  renderPhaseExec(execList, i);
  container.querySelector('#phase-exec-add').addEventListener('click', () => {
    state.phases[i].execution = normalizeExecution(state.phases[i].execution);
    state.phases[i].execution.push({ text: '', subtasks: [] });
    renderPhaseExec(execList, i); schedulePreview();
  });

  // Images list
  normalizePhaseImages(state.phases[i]);
  renderPhaseImages(container.querySelector('#phase-images-list'), i);
  container.querySelector('#phase-img-add').addEventListener('click', () => {
    state.phases[i].images.push({ title: '', data: '', caption: '' });
    renderPhaseImages(container.querySelector('#phase-images-list'), i);
    schedulePreview();
  });
}

/* ============= PHASE IMAGES EDITOR ============= */
function renderPhaseImages(listEl, phaseIdx) {
  if (!listEl) return;
  // Always read directly from state — never capture a reference that could be invalidated
  // by normalizePhaseImages or any other array replacement elsewhere
  const imgs = state.phases[phaseIdx].images;
  listEl.innerHTML = '';

  if (imgs.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'phase-empty';
    empty.textContent = 'Aucune image. Toucher « + Ajouter une image ».';
    listEl.appendChild(empty);
    return;
  }

  imgs.forEach((img, k) => {
    const card = document.createElement('div');
    card.className = 'ed-img-card';
    // Use distinct class names instead of shared data-k attribute to avoid querySelector ambiguity
    card.innerHTML = `
      <div class="ed-img-card-num">IMAGE ${k + 1}</div>
      <button type="button" class="ed-img-card-rm" data-card-rm="${k}">Suppr.</button>
      <div class="ed-field" style="margin-top:8px;">
        <label>Titre / tâche associée</label>
        <input type="text" class="img-title-inp" value="${escapeAttr(img.title)}" placeholder="Ex: Route d'approche — Attaque ERCAN">
      </div>
      <div class="ed-field">
        <label>Image</label>
        <label class="ed-img-zone ${img.data ? 'has-img' : ''}" data-phase-img-zone="${phaseIdx}-${k}">
          <input type="file" accept="image/*">
          ${img.data
            ? `<img src="${img.data}" alt="Image ${k + 1}">`
            : '<span class="img-text">▲ TOUCHER POUR CHARGER ▲</span>'}
          ${img.data ? `<button type="button" class="img-rm">×</button>` : ''}
        </label>
      </div>
      <div class="ed-field">
        <label>Commentaire / légende</label>
        <textarea class="img-caption-inp" rows="2" placeholder="Commentaire optionnel affiché sous l'image">${escapeHtml(img.caption)}</textarea>
      </div>
    `;
    listEl.appendChild(card);

    // ALL event handlers reference state.phases[phaseIdx].images[k] directly.
    // Closing over `phaseIdx` and `k` (primitives) is safe — they don't get invalidated.
    // Closing over `imgs[k]` (object reference) would be unsafe.

    // Title — direct state access
    const titleInp = card.querySelector('.img-title-inp');
    titleInp.addEventListener('input', () => {
      state.phases[phaseIdx].images[k].title = titleInp.value;
      schedulePreview();
    });

    // Caption — direct state access
    const captionInp = card.querySelector('.img-caption-inp');
    captionInp.addEventListener('input', () => {
      state.phases[phaseIdx].images[k].caption = captionInp.value;
      schedulePreview();
    });

    // Remove entire card (Suppr. button)
    card.querySelector(`[data-card-rm="${k}"]`).addEventListener('click', () => {
      state.phases[phaseIdx].images.splice(k, 1);
      renderPhaseImages(listEl, phaseIdx);
      schedulePreview();
    });

    // Image upload
    const zone = card.querySelector(`[data-phase-img-zone="${phaseIdx}-${k}"]`);
    const fileInput = zone.querySelector('input[type=file]');
    fileInput.addEventListener('change', async e => {
      const f = e.target.files[0];
      if (!f) return;
      try {
        const { dataUrl } = await compressImageFile(f);
        state.phases[phaseIdx].images[k].data = dataUrl;
        renderPhaseImages(listEl, phaseIdx);
        schedulePreview();
      } catch (err) {
        showToast('Erreur : ' + err.message);
      }
      e.target.value = '';
    });

    // Remove image data only (× button — keeps card)
    const rmImg = zone.querySelector('.img-rm');
    if (rmImg) {
      rmImg.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        state.phases[phaseIdx].images[k].data = '';
        renderPhaseImages(listEl, phaseIdx);
        schedulePreview();
      });
    }
  });
}

/* Normalize threatLevel to canonical 3-value set */
function normalizeThreatLevel(lvl) {
  const k = (lvl || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  if (k.includes('elev') || k.includes('danger') || k.includes('important')) return 'Élevé';
  if (k.includes('moder')) return 'Modéré';
  return 'Faible';
}

/* Normalize phase images: migrate legacy mapImage → images[] */
function normalizePhaseImages(ph) {
  if (!Array.isArray(ph.images)) ph.images = [];
  // Migrate legacy single mapImage field
  if (ph.mapImage && ph.images.length === 0) {
    ph.images = [{ title: 'Carte phase', data: ph.mapImage, caption: '' }];
  }
  // Ensure each entry has all fields
  ph.images = ph.images.map(img => ({
    title: img.title || '',
    data: img.data || img.mapImage || '',
    caption: img.caption || ''
  }));
  delete ph.mapImage; // clean up legacy field
}
/* Normalize charts: migrate legacy annexes.chart1Name/chart1Img/chart2Name/chart2Img to charts[] */
function normalizeCharts(state) {
  if (!Array.isArray(state.charts)) state.charts = [];
  // Migration legacy : ancien objet annexes avec chart1Name/chart1Img/chart2Name/chart2Img
  if (state.annexes && !Array.isArray(state.annexes)) {
    const legacy = state.annexes;
    if (legacy.chart1Name || legacy.chart1Img) {
      state.charts.push({ name: legacy.chart1Name || '', img: legacy.chart1Img || '' });
    }
    if (legacy.chart2Name || legacy.chart2Img) {
      state.charts.push({ name: legacy.chart2Name || '', img: legacy.chart2Img || '' });
    }
    state.annexes = []; // tableau vide pour Chat H2 à venir
  }
  // Si annexes n'existait pas du tout
  if (!Array.isArray(state.annexes)) state.annexes = [];
  // Normalisation des entrées
  state.charts = state.charts.map(c => ({ name: c.name || '', img: c.img || '' }));
}
// Normalize annexes: ensure shape {title, img, caption} for each entry
function normalizeAnnexes(state) {
  if (!Array.isArray(state.annexes)) state.annexes = [];
  state.annexes = state.annexes.map(a => ({
    title: a.title || '',
    img: a.img || '',
    caption: a.caption || ''
  }));
}
function normalizeExecution(exec) {
  if (!Array.isArray(exec)) return [];
  return exec.map(s => {
    if (typeof s === 'string') return { text: s, subtasks: [] };
    return { text: s.text || '', subtasks: Array.isArray(s.subtasks) ? s.subtasks : [] };
  });
}

function renderCharts() {
  const listEl = document.getElementById('charts-list');
  if (!listEl) return;
  const charts = state.charts;
  listEl.innerHTML = '';

  if (charts.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'phase-empty';
    empty.textContent = 'Aucune chart. Toucher \u00ab\u00a0+ Ajouter une chart\u00a0\u00bb.';
    listEl.appendChild(empty);
    return;
  }

  charts.forEach((chart, k) => {
    const card = document.createElement('div');
    card.className = 'ed-img-card';
    card.innerHTML = `
      <div class="ed-img-card-num">CHART ${k + 1}</div>
      <button type="button" class="ed-img-card-rm" data-chart-rm="${k}">Suppr.</button>
      <div class="ed-field" style="margin-top:8px;">
        <label>Nom de l\u2019a\u00e9roport / chart</label>
        <input type="text" class="chart-name-inp" value="${escapeAttr(chart.name)}" placeholder="Ex: AKROTIRI (LCRA) \u2014 Piste 10">
      </div>
      <div class="ed-field">
        <label>Image</label>
        <label class="ed-img-zone ${chart.img ? 'has-img' : ''}" data-chart-img-zone="${k}">
          <input type="file" accept="image/*">
          ${chart.img
            ? `<img src="${chart.img}" alt="Chart ${k + 1}">`
            : '<span class="img-text">\u25b2 TOUCHER POUR CHARGER \u25b2</span>'}
          ${chart.img ? `<button type="button" class="img-rm">\u00d7</button>` : ''}
        </label>
      </div>
    `;
    listEl.appendChild(card);
  });

  // Bindings — calque sur renderPhaseImages
  listEl.querySelectorAll('.chart-name-inp').forEach((inp, k) => {
    inp.addEventListener('input', () => {
      state.charts[k].name = inp.value;
      schedulePreview();
    });
  });

  listEl.querySelectorAll('[data-chart-rm]').forEach(btn => {
    btn.addEventListener('click', () => {
      const k = parseInt(btn.dataset.chartRm, 10);
      state.charts.splice(k, 1);
      renderCharts();
      schedulePreview();
    });
  });

  listEl.querySelectorAll('[data-chart-img-zone]').forEach(zone => {
    const k = parseInt(zone.dataset.chartImgZone, 10);
    const fileInp = zone.querySelector('input[type="file"]');
    fileInp.addEventListener('change', () => {
      const f = fileInp.files[0];
      if (!f) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        state.charts[k].img = e.target.result;
        renderCharts();
        schedulePreview();
      };
      reader.readAsDataURL(f);
    });
    const rmImg = zone.querySelector('.img-rm');
    if (rmImg) {
      rmImg.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        state.charts[k].img = '';
        renderCharts();
        schedulePreview();
      });
    }
  });
}

function renderAnnexes() {
  const listEl = document.getElementById('annexes-list');
  if (!listEl) return;
  const annexes = state.annexes;
  listEl.innerHTML = '';

  if (annexes.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'phase-empty';
    empty.textContent = 'Aucune annexe. Toucher \u00ab\u00a0+ Ajouter une annexe\u00a0\u00bb.';
    listEl.appendChild(empty);
    return;
  }

  annexes.forEach((annexe, k) => {
    const card = document.createElement('div');
    card.className = 'ed-img-card';
    card.innerHTML = `
      <div class="ed-img-card-num">ANNEXE ${k + 1}</div>
      <button type="button" class="ed-img-card-rm" data-annexe-rm="${k}">Suppr.</button>
      <div class="ed-field" style="margin-top:8px;">
        <label>Titre</label>
        <input type="text" class="annexe-title-inp" value="${escapeAttr(annexe.title)}" placeholder="Ex: Notes additionnelles">
      </div>
      <div class="ed-field">
        <label>Image</label>
        <label class="ed-img-zone ${annexe.img ? 'has-img' : ''}" data-annexe-img-zone="${k}">
          <input type="file" accept="image/*">
          ${annexe.img
            ? `<img src="${annexe.img}" alt="Annexe ${k + 1}">`
            : '<span class="img-text">\u25b2 TOUCHER POUR CHARGER \u25b2</span>'}
          ${annexe.img ? `<button type="button" class="img-rm">\u00d7</button>` : ''}
        </label>
      </div>
      <div class="ed-field">
        <label>Commentaire / l\u00e9gende</label>
        <textarea class="annexe-caption-inp" rows="2" placeholder="Commentaire optionnel affich\u00e9 sous l'image">${escapeHtml(annexe.caption)}</textarea>
      </div>
    `;
    listEl.appendChild(card);
  });

  // Bindings — calque strict sur renderCharts avec ajout du caption
  listEl.querySelectorAll('.annexe-title-inp').forEach((inp, k) => {
    inp.addEventListener('input', () => {
      state.annexes[k].title = inp.value;
      schedulePreview();
    });
  });

  listEl.querySelectorAll('.annexe-caption-inp').forEach((ta, k) => {
    ta.addEventListener('input', () => {
      state.annexes[k].caption = ta.value;
      schedulePreview();
    });
  });

  listEl.querySelectorAll('[data-annexe-rm]').forEach(btn => {
    btn.addEventListener('click', () => {
      const k = parseInt(btn.dataset.annexeRm, 10);
      state.annexes.splice(k, 1);
      renderAnnexes();
      schedulePreview();
    });
  });

  listEl.querySelectorAll('[data-annexe-img-zone]').forEach(zone => {
    const k = parseInt(zone.dataset.annexeImgZone, 10);
    const fileInp = zone.querySelector('input[type="file"]');
    fileInp.addEventListener('change', () => {
      const f = fileInp.files[0];
      if (!f) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        state.annexes[k].img = e.target.result;
        renderAnnexes();
        schedulePreview();
      };
      reader.readAsDataURL(f);
    });
    const rmImg = zone.querySelector('.img-rm');
    if (rmImg) {
      rmImg.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        state.annexes[k].img = '';
        renderAnnexes();
        schedulePreview();
      });
    }
  });
}

function renderPhaseExec(container, phaseIdx) {
  const ph = state.phases[phaseIdx];
  // Normalize on first encounter
  ph.execution = normalizeExecution(ph.execution);
  const steps = ph.execution;
  container.innerHTML = '';

  steps.forEach((step, j) => {
    const wrap = document.createElement('div');
    wrap.style.marginBottom = '8px';

    // Step row: [move up] [move down] [input] [remove]
    const row = document.createElement('div');
    row.className = 'ed-list-item';
    row.style.alignItems = 'center';

    // Move buttons
    const moveDiv = document.createElement('div');
    moveDiv.className = 'ed-list-move';

    const upBtn = document.createElement('button');
    upBtn.type = 'button'; upBtn.className = 'ed-btn-move';
    upBtn.textContent = '▲'; upBtn.disabled = j === 0;
    upBtn.addEventListener('click', () => {
      if (j === 0) return;
      [steps[j-1], steps[j]] = [steps[j], steps[j-1]];
      renderPhaseExec(container, phaseIdx); schedulePreview();
    });

    const dnBtn = document.createElement('button');
    dnBtn.type = 'button'; dnBtn.className = 'ed-btn-move';
    dnBtn.textContent = '▼'; dnBtn.disabled = j === steps.length - 1;
    dnBtn.addEventListener('click', () => {
      if (j === steps.length - 1) return;
      [steps[j], steps[j+1]] = [steps[j+1], steps[j]];
      renderPhaseExec(container, phaseIdx); schedulePreview();
    });
    moveDiv.append(upBtn, dnBtn);

    const inp = document.createElement('input');
    inp.type = 'text';
    inp.value = step.text || '';
    inp.addEventListener('input', () => { steps[j].text = inp.value; schedulePreview(); });

    const rmBtn = document.createElement('button');
    rmBtn.type = 'button'; rmBtn.className = 'ed-btn-icon';
    rmBtn.textContent = '×';
    rmBtn.addEventListener('click', () => {
      steps.splice(j, 1);
      renderPhaseExec(container, phaseIdx); schedulePreview();
    });

    row.append(moveDiv, inp, rmBtn);
    wrap.appendChild(row);

    // Sub-tasks section
    const subWrap = document.createElement('div');
    subWrap.className = 'ed-subtask-wrap';

    (step.subtasks || []).forEach((sub, k) => {
      const subRow = document.createElement('div');
      subRow.className = 'ed-subtask-row';
      const subInp = document.createElement('input');
      subInp.type = 'text'; subInp.value = sub;
      subInp.placeholder = `Sous-tâche ${String.fromCharCode(97 + k)}`;
      subInp.addEventListener('input', () => { steps[j].subtasks[k] = subInp.value; schedulePreview(); });
      const subRm = document.createElement('button');
      subRm.type = 'button'; subRm.className = 'ed-btn-icon'; subRm.textContent = '×';
      subRm.style.minWidth = '32px'; subRm.style.minHeight = '36px';
      subRm.addEventListener('click', () => {
        steps[j].subtasks.splice(k, 1);
        renderPhaseExec(container, phaseIdx); schedulePreview();
      });
      subRow.append(subInp, subRm);
      subWrap.appendChild(subRow);
    });

    const addSubBtn = document.createElement('button');
    addSubBtn.type = 'button'; addSubBtn.className = 'ed-btn-subtask-add';
    addSubBtn.textContent = '+ Sous-tâche';
    addSubBtn.addEventListener('click', () => {
      steps[j].subtasks.push('');
      renderPhaseExec(container, phaseIdx); schedulePreview();
    });
    subWrap.appendChild(addSubBtn);
    wrap.appendChild(subWrap);
    container.appendChild(wrap);
  });
}

function refreshImgZone(zone) {
  if (!zone) return;
  const path = zone.dataset.imgBind;
  const url = getByPath(state, path);
  zone.classList.toggle('has-img', !!url);
  if (url) {
    zone.innerHTML = `<input type="file" accept="image/*"><img src="${url}" alt="Image chargée"><button type="button" class="img-rm" aria-label="Retirer l'image">×</button>`;
  } else {
    zone.innerHTML = `<input type="file" accept="image/*"><span class="img-text">▲ TOUCHER POUR CHARGER ▲</span>`;
  }
  bindImgZoneEvents(zone);
}

function bindImgZoneEvents(zone) {
  const path = zone.dataset.imgBind;
  const fileInput = zone.querySelector('input[type=file]');
  fileInput.addEventListener('change', async e => {
    const f = e.target.files[0];
    if (!f) return;
    showToast('Compression image...');
    try {
      const { dataUrl } = await compressImageFile(f);
      setByPath(state, path, dataUrl);
      refreshImgZone(zone);
      schedulePreview();
      showToast('Image chargée ✓');
    } catch (err) {
      showToast('Erreur : ' + err.message);
    }
    e.target.value = '';
  });
  const rm = zone.querySelector('.img-rm');
  if (rm) {
    rm.addEventListener('click', e => {
      e.preventDefault();
      e.stopPropagation();
      setByPath(state, path, '');
      refreshImgZone(zone);
      schedulePreview();
    });
  }
}

/* ============= EDITOR EVENTS ============= */
function bindEditorEvents() {
  // Simple bindings
  document.querySelectorAll('[data-bind]').forEach(input => {
    input.addEventListener('input', () => {
      setByPath(state, input.dataset.bind, input.value);
      schedulePreview();
    });
  });

  // List add buttons
  document.querySelectorAll('[data-add]').forEach(btn => {
    btn.addEventListener('click', () => {
      const path = btn.dataset.add;
      getByPath(state, path).push('');
      renderList(document.querySelector(`[data-list="${path}"]`));
      schedulePreview();
    });
  });

  // Phase nav
  document.getElementById('phase-prev').addEventListener('click', () => {
    if (currentPhaseIdx > 0) { currentPhaseIdx--; renderPhaseEditor(); }
  });
  document.getElementById('phase-next').addEventListener('click', () => {
    if (currentPhaseIdx < state.phases.length - 1) { currentPhaseIdx++; renderPhaseEditor(); }
  });
  document.getElementById('phase-add').addEventListener('click', () => {
    state.phases.push({
      title: 'Nouvelle mission', objective: '', execution: [],
      flightPlan: '', threatLevel: 'Faible', notes: '', images: [],
      squadron: '', aircraft: '', subgroup: '',
      guestSquadron: { name: '', subgroup: '', aircraft: '' }
    });
    currentPhaseIdx = state.phases.length - 1;
    renderPhaseEditor(); renderRoster(); schedulePreview();
  });
  document.getElementById('phase-dup').addEventListener('click', () => {
    if (state.phases.length === 0) return;
    const cloned = JSON.parse(JSON.stringify(state.phases[currentPhaseIdx]));
    cloned.title = cloned.title + ' (copie)';
    state.phases.splice(currentPhaseIdx + 1, 0, cloned);
    currentPhaseIdx++;
    renderPhaseEditor(); renderRoster(); schedulePreview();
  });

  document.getElementById('phase-up').addEventListener('click', () => {
    if (currentPhaseIdx === 0 || state.phases.length < 2) return;
    [state.phases[currentPhaseIdx-1], state.phases[currentPhaseIdx]] =
      [state.phases[currentPhaseIdx], state.phases[currentPhaseIdx-1]];
    currentPhaseIdx--;
    renderPhaseEditor(); renderRoster(); schedulePreview();
  });

  document.getElementById('phase-down').addEventListener('click', () => {
    if (currentPhaseIdx >= state.phases.length - 1) return;
    [state.phases[currentPhaseIdx], state.phases[currentPhaseIdx+1]] =
      [state.phases[currentPhaseIdx+1], state.phases[currentPhaseIdx]];
    currentPhaseIdx++;
    renderPhaseEditor(); renderRoster(); schedulePreview();
  });
  document.getElementById('phase-rm').addEventListener('click', () => {
    if (state.phases.length === 0) return;
    if (!confirm(`Supprimer la mission ${currentPhaseIdx + 1} ?`)) return;
    state.phases.splice(currentPhaseIdx, 1);
    if (currentPhaseIdx >= state.phases.length) currentPhaseIdx = Math.max(0, state.phases.length - 1);
    renderPhaseEditor(); renderRoster();
    schedulePreview();
  });

  // Roster: add group (picks first available mission group)
  document.getElementById('roster-group-add').addEventListener('click', () => {
    if (!state.roster) state.roster = { groups: [] };
    const usedKeys = new Set(state.roster.groups.map(g => g.missionKey));
    const available = getMissionGroups().filter(g => !usedKeys.has(g.key));
    if (available.length === 0) return;
    // Auto-select first available
    state.roster.groups.push({ missionKey: available[0].key, pilots: [] });
    renderRoster(); schedulePreview();
  });
  document.getElementById('radio-item-add').addEventListener('click', () => {
    ensureRadioPlanShape();
    if (state.radioPlan.items.length >= RADIO_ITEMS_MAX) return;
    state.radioPlan.items.push({
      id: genId('it'),
      label: '',
      frequency: '',
      modulation: 'AM'
    });
    renderRadioPlan();
    schedulePreview();
  });

  // Radio plan: add aircraft button
  document.getElementById('radio-aircraft-add').addEventListener('click', () => {
    ensureRadioPlanShape();
    if (state.radioPlan.aircraftPlans.length >= RADIO_AIRCRAFT_MAX) return;
    state.radioPlan.aircraftPlans.push({
      aircraft: getAllAircraft()[0] || '',
      radios: [],
      image: ''
    });
    renderRadioAircrafts();
    schedulePreview();
  });
  document.getElementById('chart-add').addEventListener('click', () => {
    state.charts.push({ name: '', img: '' });
    renderCharts();
    schedulePreview();
  });
  document.getElementById('annexe-add').addEventListener('click', () => {
    state.annexes.push({ title: '', img: '', caption: '' });
    renderAnnexes();
    schedulePreview();
  });
  bindWingEditorEvents();  // wire wing editor (called once at init)
}

/* ============= PREVIEW ============= */
let previewTimer = null;
function schedulePreview() {
  if (previewTimer) cancelAnimationFrame(previewTimer);
  previewTimer = requestAnimationFrame(() => {
    renderPreview();
    persistState();
  });
}

function pageHeader(opts) {
  opts = opts || {};
  // Default right logo to wing logo for consistency on pages without a squadron logo
  const rightLogo = opts.rightLogo || wingConfig.wing.logo;
  const rightAlt = opts.rightAlt || wingConfig.wing.shortName;
  // FIX Bug B (complément) : <img> → <div background-image> pour les logos du header
  // car object-fit:contain est mal géré par html2canvas (issues #1322, #2425).
  // background-size:contain est correctement rendu.
  return `
    <header class="p-header">
      <div class="p-header-logo" role="img" aria-label="${escapeAttr(wingConfig.wing.shortName)}" style="background-image:url('${wingConfig.wing.logo}')"></div>
      <div class="p-title">
        <div class="p-classif">${escapeHtml(state.meta.classification)}</div>
        <h1>${escapeHtml(wingConfig.wing.shortName)} ░ BRIEFING</h1>
        <div class="p-sub">OPÉRATION ${escapeHtml(state.meta.operation)} • MISSION ${escapeHtml(state.meta.mission)}</div>
      </div>
      <div class="p-header-logo" role="img" aria-label="${escapeAttr(rightAlt)}" style="background-image:url('${rightLogo}')"></div>
    </header>
  `;
}

function pageFooter(pageNum, totalPages) {
  return `
    <footer class="p-footer">
      <span>${escapeHtml(state.meta.docRef)}</span>
      <span class="p-classif-foot">${escapeHtml(state.meta.classification)}</span>
      <span>PAGE ${pageNum.toString().padStart(2, '0')} / ${totalPages.toString().padStart(2, '0')}</span>
    </footer>
  `;
}

function imgFrame(label, url) {
  if (url) return `<div class="p-imgframe" data-label="${escapeAttr(label)}"><img src="${url}" alt="${escapeAttr(label)}"></div>`;
  return `<div class="p-imgframe empty" data-label="${escapeAttr(label)}"></div>`;
}

function pageMeta() {
  const d = formatMissionDate(state.meta.date);
  return `<div class="doc-meta">DOC ▸ ${escapeHtml(state.meta.docRef)} ▸ ${escapeHtml(d)}</div>`;
}

function formatMissionDate(d) {
  if (!d) return '';
  try {
    const dt = new Date(d);
    if (isNaN(dt)) return d;
    return dt.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  } catch { return d; }
}

/* ============= RADIO RENDER HELPERS ============= */
function renderRadioSummary() {
  ensureRadioPlanShape();
  const items = (state.radioPlan.items || []).filter(it => it.label || it.frequency);
  if (items.length === 0) {
    return '<div class="empty-placeholder">Aucun item radio défini</div>';
  }
  return `<table class="radio-summary">
    ${items.map(it => `
      <tr>
        <th>${escapeHtml(it.label || '—')}</th>
        <td><span class="radio-freq">${escapeHtml(it.frequency || '—')}</span><span class="radio-mod">${escapeHtml(it.modulation || '')}</span></td>
      </tr>
    `).join('')}
  </table>`;
}

function renderRadioTable(ap) {
  ensureRadioPlanShape();
  const itemsById = {};
  state.radioPlan.items.forEach(it => { itemsById[it.id] = it; });
  const radios = (ap.radios || []).filter(r => r.name || (r.channels && r.channels.length));
  if (radios.length === 0) {
    return '<div class="empty-placeholder">Aucune radio configurée pour cet appareil</div>';
  }
  return radios.map(r => {
    const channels = (r.channels || []).filter(ch =>
      ch.channel !== '' && ch.channel !== null && ch.channel !== undefined &&
      (ch.mode === 'custom' ? (ch.frequency || ch.label) : ch.itemId)
    );
    if (channels.length === 0) {
      return `<div class="radio-block">
        <div class="radio-block-name">${escapeHtml(r.name || '—')}</div>
        <div class="empty-placeholder" style="margin:4px 0;">Aucun canal</div>
      </div>`;
    }
    return `<div class="radio-block">
      <div class="radio-block-name">${escapeHtml(r.name || '—')}</div>
      <table class="radio-channel-table">
        ${channels.map(ch => {
          if (ch.mode === 'custom') {
            return `<tr>
              <td class="ch-num">CH ${escapeHtml(String(ch.channel ?? ''))}</td>
              <td class="ch-freq">${escapeHtml(ch.frequency || '—')}</td>
              <td class="ch-mod">${escapeHtml(ch.modulation || '')}</td>
              <td class="ch-custom-label">${escapeHtml(ch.label || '')}</td>
            </tr>`;
          }
          const it = itemsById[ch.itemId];
          if (it) {
            return `<tr>
              <td class="ch-num">CH ${escapeHtml(String(ch.channel ?? ''))}</td>
              <td class="ch-freq">${escapeHtml(it.frequency || '—')}</td>
              <td class="ch-mod">${escapeHtml(it.modulation || '')}</td>
              <td class="ch-label">${escapeHtml(it.label || '')}</td>
            </tr>`;
          }
          return `<tr>
            <td class="ch-num">CH ${escapeHtml(String(ch.channel ?? ''))}</td>
            <td class="ch-freq" colspan="3" style="font-style:italic; color:var(--khaki);">— non assigné —</td>
          </tr>`;
        }).join('')}
      </table>
    </div>`;
  }).join('');
}

/* Return a unified info object regardless of whether phase uses known or guest squadron */
function getPhaseSquadronInfo(ph) {
  if (!ph.squadron) return null;
  if (ph.squadron === '__guest__') {
    const g = ph.guestSquadron || {};
    if (!g.name && !g.aircraft) return null;
    // The guest squadron name IS the squadron identifier (replaces "INVITÉ")
    const guestName = g.name || 'INVITÉ';
    return {
      id: guestName,          // guest name = squadron id (e.g. "WOLF")
      callsign: guestName,    // same — no separate callsign for guests
      aircraft: g.aircraft || '?',
      subgroup: ph.subgroup || g.subgroup || '',
      logo: null,
      isGuest: true
    };
  }
  const sq = getSquadron(ph.squadron);
  if (!sq) return null;
  return {
    id: sq.id,
    callsign: sq.callsign,
    aircraft: ph.aircraft || sq.aircraft[0],
    subgroup: ph.subgroup || '',
    logo: sq.logo,
    isGuest: false
  };
}

function buildPages() {
  const pages = [];

  // PAGE 1 — COVER
  pages.push({
    body: `
      <div class="p-section">OPÉRATION ${escapeHtml(state.meta.operation)}</div>
      ${imgFrame('CARTE THÉÂTRE', state.cover.mapImage)}
      <div class="p-body" style="margin-top:14px;">
        ${(state.cover.narrative || '').split('\n').map(p => p.trim() ? `<p>${escapeHtml(p)}</p>` : '').join('')}
      </div>
      <div class="stamp-classif">${escapeHtml(state.meta.classification)}</div>
      <div class="stamp-receipt">REÇU LE<br>${escapeHtml(formatMissionDate(state.meta.date))}<br>${escapeHtml(wingConfig.wing.hqStamp || 'HQ ░ ' + wingConfig.wing.shortName)}</div>
    `
  });

  // PAGE 2 — SITAC
  pages.push({
    body: `
      <div class="p-section">SITAC ░ ${escapeHtml(state.sitac.date || '—')}</div>
      ${imgFrame('SITUATION TACTIQUE', state.sitac.mapImage)}
      <div class="p-subsection">Points de Situation</div>
      <ul class="p-bullets">
        ${(state.sitac.points || []).filter(p=>p).map(p => `<li>${escapeHtml(p)}</li>`).join('') || '<li class="empty-placeholder">Aucun point renseigné</li>'}
      </ul>
      <div class="p-subsection">METAR</div>
      <div class="metar-line">${escapeHtml(state.sitac.metar || '— METAR NON RENSEIGNÉ —')}</div>
    `
  });

  // PAGE 3 — MISSION OVERVIEW (with engaged squadrons incl. guests)
  const engagedMap = new Map();
  state.phases.forEach((ph, idx) => {
    const info = getPhaseSquadronInfo(ph);
    if (!info) return;
    const key = `${info.id}|${info.aircraft}|${info.subgroup}`;
    if (!engagedMap.has(key)) engagedMap.set(key, { info, phases: [] });
    engagedMap.get(key).phases.push(idx + 1);
  });
  const engagedList = Array.from(engagedMap.values());

  pages.push({
    body: `
      <div class="p-section">APERÇU MISSION</div>

      <div class="p-subsection">Objectifs</div>
      <ul class="p-bullets">
        ${(state.mission.objectives || []).filter(o=>o).map(o => `<li>${escapeHtml(o)}</li>`).join('')}
      </ul>

      ${engagedList.length ? `
        <div class="p-subsection">Escadrons Engagés</div>
        <div class="squadron-grid">
          ${engagedList.map(e => {
            const info = e.info;
            // FIX Bug B : remplacer <img> par <div> background-image pour contourner
            // le bug html2canvas avec object-fit:contain (issues #1322, #2425).
            // background-size:contain est correctement rendu, contrairement à object-fit.
            const logoHtml = info.logo
              ? `<div class="squadron-logo-sm" role="img" aria-label="${escapeAttr(info.id)}" style="background-image:url('${info.logo}')"></div>`
              : `<div class="squadron-logo-guest">INV.</div>`;
            // If sub-group defined → show it as the primary name (replaces callsign)
            const primaryName = info.subgroup ? info.subgroup : info.callsign;
            return `
              <div class="squadron-cell">
                ${logoHtml}
                <div class="squadron-info">
                  <strong>${escapeHtml(info.id)} ░ ${escapeHtml(primaryName)}</strong>
                  <div class="squadron-aircraft">${escapeHtml(info.aircraft)}</div>
                  <div class="squadron-phases">Mission${e.phases.length > 1 ? 's' : ''} ${e.phases.join(', ')}</div>
                </div>
              </div>`;
          }).join('')}
        </div>
      ` : ''}

      <div class="p-2col" style="margin-top:14px;">
        <div>
          <div class="p-subsection">FARP & Aéroports</div>
          <ul class="p-bullets">
            ${(state.mission.farp || []).filter(f=>f).map(f => `<li>${escapeHtml(f)}</li>`).join('')}
          </ul>
        </div>
        <div>
          <div class="p-subsection">Plan Radio</div>
          ${renderRadioSummary()}
        </div>
      </div>

      <div class="p-subsection">Menaces Identifiées</div>
      <div class="menace-grid">
        <div class="menace-cell"><strong>◣ Chars / MBT</strong>${escapeHtml(state.mission.threats.tanks || '—')}</div>
        <div class="menace-cell"><strong>◣ APC / VBL</strong>${escapeHtml(state.mission.threats.apc || '—')}</div>
        <div class="menace-cell"><strong>◣ AAA</strong>${escapeHtml(state.mission.threats.aaa || '—')}</div>
        <div class="menace-cell"><strong>◣ SAM</strong>${escapeHtml(state.mission.threats.sam || '—')}</div>
      </div>
      ${state.mission.threats.note ? `<div class="txt-small" style="margin-top:6px;font-style:italic;">▲ ${escapeHtml(state.mission.threats.note)}</div>` : ''}
    `
  });

  // PAGE ÉQUIPAGE — optionnelle, UN SEUL <table> par paire de groupes pour stabilité
  // Architecture choisie pour éviter le bug Skia/PDF où plusieurs <table> avec backgrounds
  // sur la même page créent des paint layers qui se réordonnent de façon non-déterministe.
  // Un seul <table> = un seul rendering pipeline = comportement déterministe en print.
  if (state.roster && state.roster.groups && state.roster.groups.length > 0) {
    const activeGroups = state.roster.groups.filter(g => g.pilots && g.pilots.some(p => p.name || p.callsign));
    if (activeGroups.length > 0) {
      // Render the colspan="2" cell for one group's header (name + aircraft badge)
      const renderGroupHead = g => {
        if (!g) return '<th colspan="2" class="rmt-empty"></th>';
        const parts = getRosterLabelParts(g.missionKey);
        const info = getMissionGroups().find(x => x.key === g.missionKey);
        return `<th colspan="2" class="rmt-group-head">
          <span class="rmt-group-name">${escapeHtml(parts.label)}</span>
          ${info && info.aircraft ? `<span class="rmt-group-aircraft">${escapeHtml(info.aircraft)}</span>` : ''}
        </th>`;
      };

      // Render one mega-table for a pair (or single group on left, empty right)
      // ALWAYS 4 columns to keep consistent layout regardless of group count
      const renderPair = (left, right) => {
        const lp = left.pilots.filter(p => p.name || p.callsign);
        const rp = right ? right.pilots.filter(p => p.name || p.callsign) : [];
        const rows = Math.max(lp.length, rp.length);

        const dataRows = [];
        for (let k = 0; k < rows; k++) {
          const a = lp[k];
          const b = rp[k];
          dataRows.push(`<tr>
            <td class="rmt-name">${a ? escapeHtml(a.name || '—') : ''}</td>
            <td class="rmt-callsign">${a ? escapeHtml(a.callsign || '—') : ''}</td>
            <td class="rmt-name rmt-sep">${b ? escapeHtml(b.name || '—') : ''}</td>
            <td class="rmt-callsign">${b ? escapeHtml(b.callsign || '—') : ''}</td>
          </tr>`);
        }

        return `
          <table class="roster-mega">
            <colgroup>
              <col class="rmt-col-name"><col class="rmt-col-cs">
              <col class="rmt-col-name"><col class="rmt-col-cs">
            </colgroup>
            <thead>
              <tr class="rmt-row-group">
                ${renderGroupHead(left)}
                ${renderGroupHead(right)}
              </tr>
              <tr class="rmt-row-cols">
                <th>NOM / INDICATIF</th><th>CALLSIGN</th>
                <th class="rmt-sep">NOM / INDICATIF</th><th>CALLSIGN</th>
              </tr>
            </thead>
            <tbody>
              ${dataRows.join('')}
            </tbody>
          </table>
        `;
      };

      // Build all mega-tables (one per pair)
      let body = '<div class="p-section">ÉQUIPAGE ░ ORDRE DE BATAILLE</div>';
      body += '<div class="roster-tables">';
      for (let i = 0; i < activeGroups.length; i += 2) {
        body += renderPair(activeGroups[i], activeGroups[i + 1]);
      }
      body += '</div>';
      pages.push({ body });
    }
  }

  // PHASES — with squadron logo and sub-group chip
  state.phases.forEach((ph, i) => {
    const tcls = threatClass(ph.threatLevel);
    const info = getPhaseSquadronInfo(ph);

    const phaseRightLogo = (info && info.logo) ? info.logo : wingConfig.wing.logo;
    const phaseRightAlt = (info && info.logo) ? info.id : wingConfig.wing.shortName;

    let squadronChip = '';
    if (info) {
      // If sub-group is defined, show it instead of the callsign (cleaner, less redundant)
      const nameToShow = info.subgroup ? info.subgroup : info.callsign;
      const subHtml = info.subgroup
        ? `<span class="sq-sub">${escapeHtml(info.subgroup)}</span>` : '';
      // Only show callsign in chip when there IS a subgroup (as context) — but per request,
      // when subgroup defined → replace callsign entirely
      squadronChip = `
        <div class="squadron-chip">
          <span class="sq-id">${escapeHtml(info.id)}</span>
          <span class="sq-cs">${escapeHtml(nameToShow)}</span>
          <span class="sq-ac">${escapeHtml(info.aircraft)}</span>
        </div>`;
    }

    pages.push({
      rightLogo: phaseRightLogo,
      rightAlt: phaseRightAlt,
      body: `
        <div class="p-section">MISSION ${i + 1} ░ ${escapeHtml((ph.title || '').toUpperCase())}</div>

        ${squadronChip}

        <div class="phase-title">
          <span class="phase-num-tag">M${i + 1}</span>
          <span style="flex:1;">${escapeHtml(ph.title || '—')}</span>
          <span class="threat-chip ${tcls}">⚠ ${escapeHtml(ph.threatLevel || '—')}</span>
        </div>

        <div class="phase-block">
          <div class="phase-block-label">◆ Objectif</div>
          <div>${escapeHtml(ph.objective || '—')}</div>
        </div>

        <div class="phase-block">
          <div class="phase-block-label">◆ Exécution</div>
          ${(() => {
            const steps = normalizeExecution(ph.execution);
            const nonEmpty = steps.filter(s => s.text);
            if (!nonEmpty.length) return '<div class="empty-placeholder">Aucune étape</div>';
            return `<ol class="p-bullets-num">${nonEmpty.map(s => {
              const subs = (s.subtasks || []).filter(st => st);
              const subsHtml = subs.length
                ? `<ul class="p-subtasks">${subs.map(st => `<li>${escapeHtml(st)}</li>`).join('')}</ul>`
                : '';
              return `<li>${escapeHtml(s.text)}${subsHtml}</li>`;
            }).join('')}</ol>`;
          })()}
        </div>

        <div class="phase-block">
          <div class="phase-block-label">◆ Plan de Vol</div>
          <div style="font-family:var(--f-mono); letter-spacing:1px;">${escapeHtml(ph.flightPlan || '—')}</div>
        </div>

        ${ph.notes ? `
          <div class="phase-block">
            <div class="phase-block-label">◆ Notes Tactiques</div>
            <div>${escapeHtml(ph.notes)}</div>
          </div>` : ''}
      `
    });

    // Dedicated image pages for this phase (2 per page)
    // NOTE: do NOT call normalizePhaseImages here — it replaces ph.images with a new
    // array, breaking the closures captured by event listeners in renderPhaseImages.
    // Normalization is done once on load (loadState / loadJsonFile).
    const phImgs = (ph.images || []).filter(img => img.data);
    const phRightLogo = (info && info.logo) ? info.logo : wingConfig.wing.logo;
    const phRightAlt = (info && info.logo) ? info.id : wingConfig.wing.shortName;
    const phaseLabel = `MISSION ${i + 1}`;

    for (let j = 0; j < phImgs.length; j += 2) {
      const img1 = phImgs[j];
      const img2 = phImgs[j + 1];
      const hasTwo = !!img2;
      pages.push({
        rightLogo: phRightLogo,
        rightAlt: phRightAlt,
        body: `
          <div class="p-section">${escapeHtml(phaseLabel)} ░ ${escapeHtml((ph.title || '').toUpperCase())} ░ DOCUMENTS</div>
          <div class="p-img-page-grid ${hasTwo ? 'stacked-two' : 'stacked-one'}">
            <div class="p-img-block">
              ${img1.title ? `<div class="p-img-block-title">${escapeHtml(img1.title)}</div>` : ''}
              <img src="${img1.data}" alt="${escapeAttr(img1.title || 'Image')}">
              ${img1.caption ? `<div class="p-img-block-caption">${escapeHtml(img1.caption)}</div>` : ''}
            </div>
            ${hasTwo ? `
              <div class="p-img-block">
                ${img2.title ? `<div class="p-img-block-title">${escapeHtml(img2.title)}</div>` : ''}
                <img src="${img2.data}" alt="${escapeAttr(img2.title || 'Image')}">
                ${img2.caption ? `<div class="p-img-block-caption">${escapeHtml(img2.caption)}</div>` : ''}
              </div>
            ` : ''}
          </div>
        `
      });
    }
  });

  // ANNEXES — RADIO PLAN grouped by squadron (one page per squadron)
  ensureRadioPlanShape();
  const aircraftPlans = (state.radioPlan.aircraftPlans || []).filter(ap =>
    ap.aircraft && ((ap.radios && ap.radios.length) || ap.image)
  );

  if (aircraftPlans.length > 0) {
    // Helper: find which squadron operates a given aircraft type
    function findSquadronForAircraft(aircraftName) {
      if (!aircraftName) return null;
      const name = aircraftName.toLowerCase();
      return wingConfig.squadrons.find(sq =>
        sq.aircraft.some(a => {
          const al = a.toLowerCase();
          return al.includes(name) || name.includes(al);
        })
      ) || null;
    }

    // --- Priority 1: collect guest squadrons from phases ---
    // Build a map: aircraft (lowercase) → guest info { name, aircraft }
    // Deduplicated by guest name — last one wins per name (shouldn't matter).
    const guestAircraftMap = new Map(); // aircraft.toLowerCase() → { name }
    (state.phases || []).forEach(ph => {
      if (ph.squadron === '__guest__' && ph.guestSquadron && ph.guestSquadron.aircraft) {
        const key = ph.guestSquadron.aircraft.toLowerCase();
        if (!guestAircraftMap.has(key)) {
          guestAircraftMap.set(key, { name: ph.guestSquadron.name || ph.guestSquadron.aircraft });
        }
      }
    });

    // Helper: find if an aircraft name matches a guest squadron
    function findGuestForAircraft(aircraftName) {
      if (!aircraftName || guestAircraftMap.size === 0) return null;
      const name = aircraftName.toLowerCase();
      // Exact match first, then substring (same logic as findSquadronForAircraft)
      for (const [key, guest] of guestAircraftMap) {
        if (key === name || key.includes(name) || name.includes(key)) return guest;
      }
      return null;
    }

    // Group aircraft plans by squadron (preserve order: first appearance)
    const guestGroupMap = new Map(); // guestName → { name, plans[] }
    const sqGroupMap = new Map();    // squadronId → { squadron, plans[] }
    const ungroupedPlans = [];

    aircraftPlans.forEach(ap => {
      // Priority 1 — guest squadron
      const guest = findGuestForAircraft(ap.aircraft);
      if (guest) {
        if (!guestGroupMap.has(guest.name)) guestGroupMap.set(guest.name, { name: guest.name, plans: [] });
        guestGroupMap.get(guest.name).plans.push(ap);
        return;
      }
      // Priority 2 — wing squadron
      const sq = findSquadronForAircraft(ap.aircraft);
      if (sq) {
        if (!sqGroupMap.has(sq.id)) sqGroupMap.set(sq.id, { squadron: sq, plans: [] });
        sqGroupMap.get(sq.id).plans.push(ap);
      } else {
        // Priority 3 — ungrouped
        ungroupedPlans.push(ap);
      }
    });

    // Helper: render one radio annexe page (shared by guest + wing groups)
    function renderRadioAnnexePage(titleLabel, logoSrc, logoAlt, plans) {
      const bodyContent = plans.length === 1
        ? `
          <div class="p-subsection">${escapeHtml(plans[0].aircraft)}</div>
          ${plans[0].image ? imgFrame(plans[0].aircraft + ' — RADIO', plans[0].image) : renderRadioTable(plans[0])}
        `
        : `
          <div class="p-2col">
            ${plans.map(ap => `
              <div>
                <div class="p-subsection">${escapeHtml(ap.aircraft)}</div>
                ${ap.image ? imgFrame(ap.aircraft + ' — RADIO', ap.image) : renderRadioTable(ap)}
              </div>
            `).join('')}
          </div>
        `;
      pages.push({
        rightLogo: logoSrc,
        rightAlt: logoAlt,
        body: `
          <div class="p-section">ANNEXE ░ PLAN RADIO ░ ${escapeHtml(titleLabel)}</div>
          ${bodyContent}
        `
      });
    }

    // One page per guest squadron group (Priority 1)
    guestGroupMap.forEach(({ name, plans }) => {
      // No dedicated logo for guests — fall back to wing logo (consistent with other logo-less pages)
      renderRadioAnnexePage(name, wingConfig.wing.logo, name, plans);
    });

    // One page per wing squadron group (Priority 2)
    sqGroupMap.forEach(({ squadron, plans }) => {
      renderRadioAnnexePage(squadron.id, squadron.logo, squadron.id, plans);
    });

    // Ungrouped plans (custom aircraft not matching any squadron) → one extra page
    if (ungroupedPlans.length > 0) {
      for (let i = 0; i < ungroupedPlans.length; i += 2) {
        const ap1 = ungroupedPlans[i];
        const ap2 = ungroupedPlans[i + 1];
        pages.push({
          body: `
            <div class="p-section">ANNEXE ░ PLAN RADIO</div>
            <div class="p-2col">
              <div>
                <div class="p-subsection">${escapeHtml(ap1.aircraft || 'APPAREIL')}</div>
                ${ap1.image ? imgFrame(ap1.aircraft + ' — RADIO', ap1.image) : renderRadioTable(ap1)}
              </div>
              <div>
                ${ap2 ? `
                  <div class="p-subsection">${escapeHtml(ap2.aircraft || 'APPAREIL')}</div>
                  ${ap2.image ? imgFrame(ap2.aircraft + ' — RADIO', ap2.image) : renderRadioTable(ap2)}
                ` : ''}
              </div>
            </div>
          `
        });
      }
    }
  }

  // CHARTS — une page par chart non vide
  state.charts.forEach((chart, idx) => {
    if (chart.img || chart.name) {
      pages.push({
        body: `
          <div class="p-section">CHART ░ AÉROPORT ${idx + 1}</div>
          <div class="p-subsection">${escapeHtml(chart.name || 'AÉROPORT')}</div>
          ${imgFrame('CHART OPS', chart.img)}
        `
      });
    }
  });

  // ANNEXES — une page par annexe non vide
  state.annexes.forEach((annexe, idx) => {
    if (annexe.img || annexe.title || annexe.caption) {
      pages.push({
        body: `
          <div class="p-section">ANNEXE ░ ${escapeHtml(annexe.title || ('DOCUMENT ' + (idx + 1)))}</div>
          ${imgFrame('ANNEXE', annexe.img)}
          ${annexe.caption ? `<div class="p-annexe-caption">${escapeHtml(annexe.caption)}</div>` : ''}
        `
      });
    }
  });

  return pages;
}

function threatClass(lvl) {
  const k = (lvl || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  // Legacy values (Important, Danger) → Élevé
  if (k.includes('danger') || k.includes('important')) return 't-eleve';
  if (k.includes('elev') || k.includes('élev')) return 't-eleve';
  if (k.includes('moder') || k.includes('modér')) return 't-modere';
  return 't-faible';
}

function renderPreview() {
  const pages = buildPages();
  const total = pages.length;
  const html = pages.map((p, i) => `
    <article class="page">
      ${pageMeta()}
      ${pageHeader({ rightLogo: p.rightLogo, rightAlt: p.rightAlt })}
      <div style="padding-bottom:28px;">${p.body}</div>
      ${pageFooter(i + 1, total)}
    </article>
  `).join('');
  document.getElementById('preview').innerHTML = html;
  applyPreviewScale();
}

/* Auto-scale preview to fit on small screens */
function applyPreviewScale() {
  const wrap = document.getElementById('preview-wrap');
  const pages = document.querySelectorAll('.page');
  if (!pages.length) return;
  if (window.innerWidth > MOBILE_BREAKPOINT) {
    pages.forEach(p => { p.style.transform = ''; p.style.marginBottom = ''; });
    return;
  }
  // mobile: scale to fit width minus padding
  const available = wrap.clientWidth - 16;
  const pageWidth = 794;
  if (available >= pageWidth) {
    pages.forEach(p => { p.style.transform = ''; p.style.marginBottom = ''; });
    return;
  }
  const scale = available / pageWidth;
  pages.forEach(p => {
    p.style.transform = `scale(${scale})`;
    p.style.transformOrigin = 'top left';
    // reserve scaled height
    const naturalH = p.offsetHeight;
    p.style.marginBottom = `${30 - (naturalH * (1 - scale))}px`;
  });
}

/* ============= UTILITY ============= */
function escapeHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
function escapeAttr(str) { return escapeHtml(str); }

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(showToast._h);
  showToast._h = setTimeout(() => t.classList.remove('show'), 2200);
}

/* ============= ACTIONS ============= */
function downloadJson() {
  const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
  const op = (state.meta.operation || 'op').toLowerCase().replace(/\s+/g, '_');
  const ms = (state.meta.mission || 'm').toLowerCase().replace(/\s+/g, '_');
  const fname = `briefing_${op}_${ms}_${Date.now()}.json`;

  // Try Web Share API first (better on Android)
  if (navigator.share && navigator.canShare) {
    try {
      const file = new File([blob], fname, { type: 'application/json' });
      if (navigator.canShare({ files: [file] })) {
        navigator.share({ files: [file], title: 'Briefing ' + wingConfig.wing.id, text: fname }).catch(() => {
          fallbackDownload(blob, fname);
        });
        return;
      }
    } catch (e) {}
  }
  fallbackDownload(blob, fname);
}

function fallbackDownload(blob, fname, toastMsg) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fname;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  showToast(toastMsg || 'Briefing exporté ✓');
}

function loadJsonFile(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = JSON.parse(reader.result);
      state = mergeDeep(structuredClone(DEFAULTS), parsed);
      if (Array.isArray(state.phases)) {
        state.phases.forEach(ph => {
          ph.execution = normalizeExecution(ph.execution);
          normalizePhaseImages(ph);
          ph.threatLevel = normalizeThreatLevel(ph.threatLevel);
        });
      }
      currentPhaseIdx = 0;
      renderEditorBindings();
      schedulePreview();
      // 5.2 — Warn about squadron IDs referenced by this briefing but absent from current wing
      if (Array.isArray(state.phases)) {
        const knownIds = new Set((wingConfig.squadrons || []).map(sq => sq.id));
        const missingIds = [...new Set(
          state.phases
            .map(ph => ph.squadron)
            .filter(id => id && id !== '__guest__' && !knownIds.has(id))
        )];
        if (missingIds.length > 0) {
          const MAX_SHOWN = 3;
          const shown = missingIds.slice(0, MAX_SHOWN).join(', ');
          const extra = missingIds.length > MAX_SHOWN ? ` (+${missingIds.length - MAX_SHOWN} autres)` : '';
          showToast(
            `⚠ Ce briefing référence ${missingIds.length} escadron(s) absent(s) du wing courant : ${shown}${extra}. ` +
            `Importez un wing compatible ou modifiez les missions concernées.`
          );
        } else {
          showToast('Briefing chargé ✓');
        }
      } else {
        showToast('Briefing chargé ✓');
      }
    } catch (e) {
      showToast('⚠ Fichier JSON invalide : ' + e.message);
    }
  };
  reader.onerror = () => showToast('⚠ Lecture impossible');
  reader.readAsText(file);
}

function resetAll() {
  if (!confirm('Réinitialiser tout le briefing ?')) return;
  state = structuredClone(DEFAULTS);
  currentPhaseIdx = 0;
  renderEditorBindings();
  schedulePreview();
  persistState();
  showToast('Briefing réinitialisé ✓');
}

/* ============= WING EDITOR ============= */

/* --- Logo compression: 256×256 max, JPEG 0.85 ---
   Separate from compressImageFile (1600px/0.82) — logos need smaller footprint. */
const LOGO_MAX_SIZE = 256;

function compressLogoFile(file) {
  return new Promise((resolve, reject) => {
    if (!file.type.startsWith('image/')) {
      reject(new Error('Le fichier doit être une image.')); return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        try {
          let { width, height } = img;
          // Scale down keeping aspect ratio, capped at LOGO_MAX_SIZE on longest side
          if (width > LOGO_MAX_SIZE || height > LOGO_MAX_SIZE) {
            if (width >= height) {
              height = Math.round(height * LOGO_MAX_SIZE / width);
              width  = LOGO_MAX_SIZE;
            } else {
              width  = Math.round(width * LOGO_MAX_SIZE / height);
              height = LOGO_MAX_SIZE;
            }
          }
          const canvas = document.createElement('canvas');
          canvas.width = width; canvas.height = height;
          const ctx = canvas.getContext('2d');
          // No background fill — preserve alpha channel for kraft texture blending
          ctx.drawImage(img, 0, 0, width, height);
          resolve({ dataUrl: canvas.toDataURL('image/png'), width, height });
        } catch (e) { reject(e); }
      };
      img.onerror = () => reject(new Error('Image illisible.'));
      img.src = reader.result;
    };
    reader.onerror = () => reject(new Error('Lecture du fichier impossible.'));
    reader.readAsDataURL(file);
  });
}

/* --- Size counter ---
   Displays compressed JSON byte count. Warn threshold: 3 500 Ko (leaves ~1.5 MB for briefing state). */
function updateWingSizeCounter() {
  const el = document.getElementById('wing-size-counter');
  if (!el) return;
  const kb = Math.round(JSON.stringify(wingConfig).length / 1024);
  el.textContent = 'Taille config : ' + kb + ' Ko';
  el.classList.toggle('warn', kb > 3500);
}

/* --- Wing main logo zone ---
   Manages #wing-logo-zone independently from state-based refreshImgZone().
   Removing the wing logo reverts to DEFAULT_WING_CONFIG.wing.logo (logo can't be empty). */
function refreshWingLogoZone() {
  const zone = document.getElementById('wing-logo-zone');
  if (!zone) return;
  // Security (§5.3): validate data URL before injecting into src; never trust wingConfig blindly
  const raw = wingConfig.wing.logo;
  const url  = (raw && raw.startsWith('data:image/')) ? raw : '';
  zone.classList.toggle('has-img', !!url);
  zone.classList.remove('wing-logo-loading');  // always clear loading state on (re)render

  if (url) {
    zone.innerHTML = '<input type="file" accept="image/*" id="wing-logo-input">' +
      '<img src="' + escapeAttr(url) + '" alt="Logo wing">' +
      '<button type="button" class="img-rm" aria-label="Réinitialiser le logo">×</button>' +
      '<span class="img-info">Cliquer pour remplacer</span>';
  } else {
    zone.innerHTML = '<input type="file" accept="image/*" id="wing-logo-input">' +
      '<span class="img-text">▲ TOUCHER POUR CHARGER UN LOGO ▲</span>';
  }

  // Bind file picker
  const inp = zone.querySelector('#wing-logo-input');
  inp.addEventListener('change', async e => {
    const f = e.target.files[0]; if (!f) return;
    zone.classList.add('wing-logo-loading');
    showToast('Compression logo...');
    try {
      const { dataUrl } = await compressLogoFile(f);
      wingConfig.wing.logo = dataUrl;
      persistWingConfig(); applyWingBranding(); schedulePreview();
      refreshWingLogoZone(); updateWingSizeCounter();  // rebuilds zone, removes loading class
      showToast('Logo wing chargé ✓');
    } catch (err) {
      zone.classList.remove('wing-logo-loading');  // restore zone on error — no stuck state
      showToast('⚠ Logo invalide : ' + err.message);
    }
    e.target.value = '';
  });

  // × reverts to default logo (wing logo can't be blank — validator requires data:image/)
  const rm = zone.querySelector('.img-rm');
  if (rm) {
    rm.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      wingConfig.wing.logo = DEFAULT_WING_CONFIG.wing.logo;
      persistWingConfig(); applyWingBranding(); schedulePreview();
      refreshWingLogoZone(); updateWingSizeCounter();
      showToast('Logo réinitialisé ✓');
    });
  }
}

/* --- Squadron logo zone ---
   sqIdx (number) captured in closure — NEVER the squadron object itself.
   Empty logo is allowed on squadrons; PDF renderer falls back to wing logo. */
function refreshSqLogoZone(zone, sqIdx) {
  if (!zone) return;
  // SAFETY: always read through index, not captured object reference
  const raw = wingConfig.squadrons[sqIdx] ? wingConfig.squadrons[sqIdx].logo : '';
  // Security (§5.3): validate data URL before injecting into src
  const url  = (raw && raw.startsWith('data:image/')) ? raw : '';
  zone.classList.toggle('has-img', !!url);
  zone.classList.remove('wing-logo-loading');  // clear loading state on (re)render

  if (url) {
    zone.innerHTML = '<input type="file" accept="image/*">' +
      '<img src="' + escapeAttr(url) + '" alt="Logo escadron">' +
      '<button type="button" class="img-rm" aria-label="Retirer le logo">×</button>';
  } else {
    zone.innerHTML = '<input type="file" accept="image/*">' +
      '<span class="img-text">▲ LOGO ESCADRON ▲</span>';
  }

  const inp = zone.querySelector('input[type=file]');
  inp.addEventListener('change', async e => {
    const f = e.target.files[0]; if (!f) return;
    if (!wingConfig.squadrons[sqIdx]) return;   // guard: squadron removed before async resolves
    zone.classList.add('wing-logo-loading');
    showToast('Compression logo...');
    try {
      const { dataUrl } = await compressLogoFile(f);
      wingConfig.squadrons[sqIdx].logo = dataUrl;   // sqIdx (number) — safe
      persistWingConfig(); applyWingBranding(); schedulePreview();
      refreshSqLogoZone(zone, sqIdx); updateWingSizeCounter();  // rebuilds zone, removes loading
      showToast('Logo escadron chargé ✓');
    } catch (err) {
      zone.classList.remove('wing-logo-loading');  // restore zone on error — no stuck state
      showToast('⚠ Logo invalide : ' + err.message);
    }
    e.target.value = '';
  });

  const rm = zone.querySelector('.img-rm');
  if (rm) {
    rm.addEventListener('click', ev => {
      ev.preventDefault(); ev.stopPropagation();
      if (!wingConfig.squadrons[sqIdx]) return;
      wingConfig.squadrons[sqIdx].logo = '';   // sqIdx (number)
      persistWingConfig(); applyWingBranding(); schedulePreview();
      refreshSqLogoZone(zone, sqIdx); updateWingSizeCounter();
    });
  }
}

/* --- Aircraft tag row for one squadron ---
   sqIdx (number) and acIdx (number) are BOTH captured as primitives in every listener.
   NEVER capture the aircraft string or the squadron object. */
function renderSqAircraftTags(container, sqIdx) {
  if (!container || !wingConfig.squadrons[sqIdx]) return;
  container.innerHTML = '';

  // Existing tags
  // Iterate by index — closure captures acIdx (number), not the string value
  wingConfig.squadrons[sqIdx].aircraft.forEach((_, acIdx) => {
    const tag = document.createElement('span');
    tag.className = 'wing-ac-tag';

    const label = document.createElement('span');
    label.textContent = wingConfig.squadrons[sqIdx].aircraft[acIdx];  // read through index

    const rmBtn = document.createElement('button');
    rmBtn.type = 'button';
    rmBtn.setAttribute('aria-label', 'Supprimer appareil');
    rmBtn.textContent = '×';
    rmBtn.addEventListener('click', () => {
      if (!wingConfig.squadrons[sqIdx]) return;
      wingConfig.squadrons[sqIdx].aircraft.splice(acIdx, 1);  // acIdx (number) — safe
      persistWingConfig(); schedulePreview(); updateWingSizeCounter();
      renderSqAircraftTags(container, sqIdx);  // re-render tags only, no full list rebuild
    });

    tag.appendChild(label);
    tag.appendChild(rmBtn);
    container.appendChild(tag);
  });

  // Add-new row
  const addRow = document.createElement('div');
  addRow.className = 'wing-ac-add-row';

  const addInp = document.createElement('input');
  addInp.type = 'text';
  addInp.placeholder = 'F-4E Phantom II';
  addInp.maxLength = 60;

  const addBtn = document.createElement('button');
  addBtn.type = 'button';
  addBtn.className = 'ed-btn-add-sm';
  addBtn.textContent = '+';

  const doAdd = () => {
    const val = addInp.value.trim(); if (!val) return;
    if (!wingConfig.squadrons[sqIdx]) return;
    wingConfig.squadrons[sqIdx].aircraft.push(val);  // sqIdx (number) — safe
    addInp.value = '';
    persistWingConfig(); schedulePreview(); updateWingSizeCounter();
    renderSqAircraftTags(container, sqIdx);
  };
  addBtn.addEventListener('click', doAdd);
  addInp.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); doAdd(); } });

  addRow.appendChild(addInp);
  addRow.appendChild(addBtn);
  container.appendChild(addRow);
}

/* --- Build one squadron card DOM element ---
   CRITICAL: sqIdx (number) captured in ALL closures — never the squadron object.
   The local `sq` variable is used ONLY to read initial values for HTML building,
   never referenced inside any event listener. */
function renderWingSquadronCard(sqIdx) {
  // Read-only snapshot for initial HTML values ONLY
  const sq = wingConfig.squadrons[sqIdx];

  const card = document.createElement('div');
  card.className = 'wing-sq-card';
  card.dataset.sqIdx = sqIdx;

  /* ── Header (toggle + controls) ── */
  const header = document.createElement('div');
  header.className = 'wing-sq-header';

  const toggle = document.createElement('span');
  toggle.className = 'wing-sq-toggle';
  toggle.textContent = sq.id || '(sans id)';
  toggle.addEventListener('click', () => { card.classList.toggle('open'); });

  const btnUp = document.createElement('button');
  btnUp.type = 'button'; btnUp.className = 'ed-btn-icon'; btnUp.title = 'Monter';
  btnUp.innerHTML = '↑';
  btnUp.addEventListener('click', () => {
    if (sqIdx === 0) return;
    const sqs = wingConfig.squadrons;
    [sqs[sqIdx - 1], sqs[sqIdx]] = [sqs[sqIdx], sqs[sqIdx - 1]];  // sqIdx (number)
    persistWingConfig(); applyWingBranding(); schedulePreview();
    renderWingSquadrons();
  });

  const btnDown = document.createElement('button');
  btnDown.type = 'button'; btnDown.className = 'ed-btn-icon'; btnDown.title = 'Descendre';
  btnDown.innerHTML = '↓';
  btnDown.addEventListener('click', () => {
    const sqs = wingConfig.squadrons;
    if (sqIdx >= sqs.length - 1) return;
    [sqs[sqIdx], sqs[sqIdx + 1]] = [sqs[sqIdx + 1], sqs[sqIdx]];  // sqIdx (number)
    persistWingConfig(); applyWingBranding(); schedulePreview();
    renderWingSquadrons();
  });

  const btnDel = document.createElement('button');
  btnDel.type = 'button'; btnDel.className = 'ed-btn-icon danger'; btnDel.title = 'Supprimer escadron';
  btnDel.innerHTML = '×';
  btnDel.addEventListener('click', () => {
    const sqId   = wingConfig.squadrons[sqIdx] ? wingConfig.squadrons[sqIdx].id : '?';  // sqIdx
    const isLast = wingConfig.squadrons.length === 1;
    const extra  = isLast ? '\n\n⚠ Il s\'agit du dernier escadron du wing.' : '';
    if (!confirm('Supprimer l\'escadron "' + escapeHtml(sqId) + '" ?' + extra + '\nLes missions qui le référencent seront affichées grisées.')) return;
    wingConfig.squadrons.splice(sqIdx, 1);  // sqIdx (number)
    persistWingConfig(); applyWingBranding(); schedulePreview();
    renderWingSquadrons();
  });

  header.appendChild(toggle);
  header.appendChild(btnUp);
  header.appendChild(btnDown);
  header.appendChild(btnDel);
  card.appendChild(header);

  /* ── Body (fields) ── */
  const body = document.createElement('div');
  body.className = 'wing-sq-body';

  // Helper: make a labelled input row, bound via sqIdx (number) + field name string
  // fieldName is a plain string (a primitive) — safe to capture in closure
  function makeField(labelText, fieldName, value, placeholder, hint) {
    const wrap = document.createElement('div');
    wrap.className = 'ed-field';
    const lbl = document.createElement('label');
    lbl.innerHTML = escapeHtml(labelText) + (hint ? ' <span class="wing-hint">(' + escapeHtml(hint) + ')</span>' : '');
    const inp = document.createElement('input');
    inp.type = 'text'; inp.value = value || ''; inp.placeholder = placeholder || '';
    inp.addEventListener('input', () => {
      if (!wingConfig.squadrons[sqIdx]) return;
      wingConfig.squadrons[sqIdx][fieldName] = inp.value;  // sqIdx (number), fieldName (string)
      // Update card header label when id changes
      if (fieldName === 'id') {
        toggle.textContent = inp.value || '(sans id)';
        // Visual warning: squadron id must not contain spaces or slashes
        inp.classList.toggle('wing-id-warning', /[\s/]/.test(inp.value) && inp.value.length > 0);
      }
      persistWingConfig(); applyWingBranding(); schedulePreview(); updateWingSizeCounter();
    });
    // Initial validation state for id fields when card is first rendered
    if (fieldName === 'id' && value) {
      inp.classList.toggle('wing-id-warning', /[\s/]/.test(value));
    }
    wrap.appendChild(lbl); wrap.appendChild(inp);
    return wrap;
  }

  const rowIdName = document.createElement('div');
  rowIdName.className = 'ed-field-row';
  rowIdName.appendChild(makeField('Identifiant', 'id', sq.id, 'KHR-26', 'clé stable, ne pas modifier après création'));
  rowIdName.appendChild(makeField('Callsign', 'callsign', sq.callsign, 'DUFF', ''));
  body.appendChild(rowIdName);

  body.appendChild(makeField('Nom complet', 'name', sq.name, '541st Tactical Fighter Squadron', ''));

  const rowNickAc = document.createElement('div');
  rowNickAc.className = 'ed-field-row';
  rowNickAc.appendChild(makeField('Surnom', 'nickname', sq.nickname, 'Bounty Hunter', ''));
  body.appendChild(rowNickAc);

  // Aircraft multi-tags
  const acWrap = document.createElement('div');
  acWrap.className = 'ed-field';
  const acLbl = document.createElement('label');
  acLbl.textContent = 'Appareils';
  const acTags = document.createElement('div');
  acTags.className = 'wing-aircraft-tags';
  acWrap.appendChild(acLbl);
  acWrap.appendChild(acTags);
  body.appendChild(acWrap);
  renderSqAircraftTags(acTags, sqIdx);  // sqIdx (number)

  // Squadron logo
  const logoWrap = document.createElement('div');
  logoWrap.className = 'ed-field';
  const logoLbl = document.createElement('label');
  logoLbl.textContent = 'Logo escadron';
  const logoZone = document.createElement('label');
  logoZone.className = 'ed-img-zone wing-logo-zone';
  logoWrap.appendChild(logoLbl);
  logoWrap.appendChild(logoZone);
  body.appendChild(logoWrap);
  refreshSqLogoZone(logoZone, sqIdx);  // sqIdx (number)

  card.appendChild(body);
  return card;
}

/* --- Squadron list renderer ---
   Preserves open/closed state of cards across re-renders using squadron id strings,
   not indices (indices shift on move/delete). */
let _wingOpenSqIds = new Set();

function _saveWingOpenState() {
  _wingOpenSqIds = new Set();
  document.querySelectorAll('.wing-sq-card.open').forEach(card => {
    const idx = parseInt(card.dataset.sqIdx, 10);
    if (!isNaN(idx) && wingConfig.squadrons[idx]) {
      _wingOpenSqIds.add(wingConfig.squadrons[idx].id);
    }
  });
}

function renderWingSquadrons(openLastCard) {
  _saveWingOpenState();
  const list = document.getElementById('wing-squadrons-list');
  if (!list) return;
  list.innerHTML = '';

  // Iterate by index — _ is the squadron object, NEVER used in closures below
  wingConfig.squadrons.forEach((_, sqIdx) => {
    // sqIdx is a number primitive — safe to pass to renderWingSquadronCard
    const card = renderWingSquadronCard(sqIdx);
    // Restore open state by squadron id (not index, which can shift)
    const isLast = openLastCard && (sqIdx === wingConfig.squadrons.length - 1);
    if (isLast || _wingOpenSqIds.has(wingConfig.squadrons[sqIdx].id)) {
      card.classList.add('open');
    }
    list.appendChild(card);
  });

  updateWingSizeCounter();
}

/* --- Populate static wing-identity inputs from wingConfig ---
   Called on init and after import/reset. */
function renderWingEditor() {
  const w = wingConfig.wing;
  const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
  setVal('wing-shortName', w.shortName);
  setVal('wing-id',        w.id);
  setVal('wing-fullName',  w.fullName);
  setVal('wing-appTitle',  w.appTitle);
  setVal('wing-hqStamp',   w.hqStamp);
  refreshWingLogoZone();
  renderWingSquadrons();
  updateWingSizeCounter();
}

/* --- Bind wing editor events (called ONCE from bindEditorEvents on init) ---
   Static elements (inputs, buttons) only — squadron cards are re-created by renderWingSquadrons. */
function bindWingEditorEvents() {

  // ── Wing identity inputs ──
  // Each field name and element id are string primitives — safe in closures
  [
    ['wing-shortName', 'shortName'],
    ['wing-id',        'id'       ],
    ['wing-fullName',  'fullName' ],
    ['wing-appTitle',  'appTitle' ],
    ['wing-hqStamp',   'hqStamp'  ]
  ].forEach(([elId, field]) => {   // elId and field are string primitives — closure-safe
    const inp = document.getElementById(elId);
    if (!inp) return;
    inp.addEventListener('input', () => {
      wingConfig.wing[field] = inp.value;   // field (string primitive) — safe
      // Visual warning on wing id: no spaces or slashes allowed
      if (field === 'id') {
        inp.classList.toggle('wing-id-warning', /[\s/]/.test(inp.value) && inp.value.length > 0);
      }
      persistWingConfig(); applyWingBranding(); schedulePreview(); updateWingSizeCounter();
    });
    // Initial validation state for wing id on load
    if (field === 'id') {
      inp.classList.toggle('wing-id-warning', /[\s/]/.test(inp.value) && inp.value.length > 0);
    }
  });

  // ── Wing logo: initial bind (zone may be re-rendered, refreshWingLogoZone re-binds) ──
  // The zone itself is static in the HTML; refreshWingLogoZone() re-binds after each render
  refreshWingLogoZone();

  // ── Add squadron ──
  const btnAddSq = document.getElementById('wing-sq-add');
  if (btnAddSq) {
    btnAddSq.addEventListener('click', () => {
      wingConfig.squadrons.push({
        id: '', name: '', nickname: '', callsign: '',
        aircraft: [], logo: ''
      });
      persistWingConfig(); applyWingBranding(); schedulePreview();
      renderWingSquadrons(true);  // true = open last card
      showToast('Escadron ajouté — pensez à renseigner l\'id ✓');
    });
  }

  // ── Import config ──
  const importInp = document.getElementById('wing-import-input');
  if (importInp) {
    importInp.addEventListener('change', e => {
      if (e.target.files[0]) importWingConfig(e.target.files[0]);
      e.target.value = '';
    });
  }

  // ── Export config ──
  const btnExport = document.getElementById('wing-export-btn');
  if (btnExport) {
    btnExport.addEventListener('click', exportWingConfig);
  }

  // ── Reset to default ──
  const btnReset = document.getElementById('wing-reset-btn');
  if (btnReset) {
    btnReset.addEventListener('click', resetWingConfig);
  }
}

/* ============= WING ACTIONS ============= */

/* Serialize wingConfig to JSON and offer download.
   Mirrors downloadJson() — Web Share API first, fallbackDownload as safety net. */
function exportWingConfig() {
  const blob = new Blob([JSON.stringify(wingConfig, null, 2)], { type: 'application/json' });
  const wid  = (wingConfig.wing.id || 'wing').toLowerCase().replace(/[\s/]+/g, '_');
  const fname = 'wing_config_' + wid + '_' + Date.now() + '.json';

  if (navigator.share && navigator.canShare) {
    try {
      const file = new File([blob], fname, { type: 'application/json' });
      if (navigator.canShare({ files: [file] })) {
        navigator.share({
          files: [file],
          title: 'Config ' + wingConfig.wing.shortName,
          text: fname
        }).catch(() => fallbackDownload(blob, fname, 'Config wing exportée ✓'));
        return;
      }
    } catch (e) {}
  }
  fallbackDownload(blob, fname, 'Config wing exportée ✓');
}

/* Read a JSON file, validate it as a wing config, and apply it.
   On error, shows a toast — never throws / alerts. */
function importWingConfig(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = JSON.parse(reader.result);
      const check  = validateWingConfig(parsed);
      if (!check.ok) {
        showToast('⚠ Config invalide : ' + check.errors.slice(0, 2).join(' · ') +
          (check.errors.length > 2 ? ' (+' + (check.errors.length - 2) + ')' : ''));
        return;
      }
      wingConfig = parsed;
      persistWingConfig();
      applyWingBranding();
      renderEditorBindings();
      schedulePreview();
      showToast('Config wing chargée ✓ — ' + escapeHtml(wingConfig.wing.shortName));
    } catch (e) {
      showToast('⚠ JSON invalide : ' + e.message);
    }
  };
  reader.onerror = () => showToast('⚠ Lecture du fichier impossible');
  reader.readAsText(file);
}

/* Hard reset to the embedded DEFAULT_WING_CONFIG, wiping localStorage entry. */
function resetWingConfig() {
  if (!confirm(
    'Réinitialiser au wing par défaut ?\n' +
    'La configuration wing actuelle sera perdue.'
  )) return;
  wingConfig = structuredClone(DEFAULT_WING_CONFIG);
  localStorage.removeItem(KEY_WING);
  applyWingBranding();
  renderEditorBindings();
  schedulePreview();
  showToast('Wing réinitialisé ✓');
}


function setActiveTab(tab) {
  activeTab = tab;
  document.body.dataset.activeTab = tab;
  document.querySelectorAll('.tab-bar button').forEach(b => {
    b.classList.toggle('current', b.dataset.tab === tab);
  });
  // On mobile, force the matching <details> to be open
  if (window.innerWidth <= MOBILE_BREAKPOINT) {
    document.querySelectorAll('.ed-section').forEach(s => {
      if (s.dataset.section === tab) {
        s.setAttribute('open', '');
      }
    });
  }
  // Reset scroll on tab change
  if (tab === 'preview') {
    document.getElementById('preview-wrap').scrollTop = 0;
    applyPreviewScale();
  } else {
    document.getElementById('editor').scrollTop = 0;
  }
}

function bindTabBar() {
  document.querySelectorAll('.tab-bar button').forEach(b => {
    b.addEventListener('click', () => setActiveTab(b.dataset.tab));
  });
}

/* ============= WING BRANDING ============= */
/* Apply wing identity to all dynamic HTML entry-points.
   Must be called:
     - once in init() after loadWingConfig()
     - again after any change to wingConfig (importWingConfig, resetWingConfig, wing editor)
   XSS safety: all values from wingConfig pass through escapeHtml / escapeAttr.
   The static HTML contains 'MY WING' placeholders; this function overwrites
   them at DOMContentLoaded so they never appear if wingConfig is loaded. */
function applyWingBranding() {
  const w = wingConfig.wing;
  // <title>
  document.title = w.shortName + ' // ' + w.appTitle;
  // Toolbar brand
  const brandEl = document.querySelector('.tb-brand-main');
  if (brandEl) brandEl.textContent = w.shortName;
  // Lateral help block (◆ MY WING ◆)
  const helpEl = document.querySelector('.ed-help[data-wing-label]');
  if (helpEl) helpEl.firstChild.textContent = '◆ ' + w.shortName + ' ◆';
}

/* ============= THEME (Phase X — étape E) ============= */
/* Le thème graphique est une préférence utilisateur indépendante du wing
   et du briefing. Stocké en localStorage[KEY_THEME] sous forme d'identifiant
   string. 4 valeurs valides : 'cw-nato' (défaut), 'cw-soviet', 'modern-nato',
   'modern-east'. Toute valeur inconnue ou absente → fallback 'cw-nato'. */
const THEME_IDS = ['cw-nato', 'cw-soviet', 'modern-nato', 'modern-east'];

function loadTheme() {
  try {
    const raw = localStorage.getItem(KEY_THEME);
    if (raw && THEME_IDS.indexOf(raw) !== -1) return raw;
  } catch(e) { /* localStorage may be unavailable */ }
  return 'cw-nato';
}

function applyTheme(themeId) {
  if (THEME_IDS.indexOf(themeId) === -1) themeId = 'cw-nato';
  document.body.dataset.theme = themeId;
  try { localStorage.setItem(KEY_THEME, themeId); }
  catch(e) { /* ignore */ }
  const sel = document.getElementById('theme-select');
  if (sel) sel.value = themeId;
}

/* ============= OVERFLOW DETECTION (chatE étape A) =============
   Détecte les pages dont le contenu déborde de la hauteur A4 figée (1123px).
   Un bandeau rouge "⚠ Contenu tronqué" est injecté en aperçu uniquement.
   Il disparaît dynamiquement si l'utilisateur supprime du contenu.
   Le MutationObserver surveille #preview — aucun re-check disséminé ailleurs.
   ================================================================ */
const OVERFLOW_THRESHOLD_PX = 10;
let overflowObserver = null;

function detectPageOverflows() {
  const pages = document.querySelectorAll('#preview .page');
  pages.forEach(function(page) {
    let warn = page.querySelector('.p-overflow-warning');
    // scrollHeight mesure le contenu réel même avec overflow:hidden — c'est volontaire
    const overflowsBy = page.scrollHeight - page.clientHeight;
    if (overflowsBy > OVERFLOW_THRESHOLD_PX) {
      if (!warn) {
        warn = document.createElement('div');
        warn.className = 'p-overflow-warning';
        warn.textContent = '⚠ Contenu tronqué';
        page.appendChild(warn);
      }
    } else {
      if (warn) warn.remove();
    }
  });
}

function initOverflowObserver() {
  const previewEl = document.getElementById('preview');
  if (!previewEl) return;
  if (overflowObserver) overflowObserver.disconnect();
  overflowObserver = new MutationObserver(function() {
    // Debounce 50ms pour éviter le spam sur les mutations en cascade
    clearTimeout(overflowObserver._timer);
    overflowObserver._timer = setTimeout(detectPageOverflows, 50);
  });
  overflowObserver.observe(previewEl, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
  });
  // Première passe immédiate à l'initialisation
  detectPageOverflows();
}

/* ============= INIT ============= */
function init() {
  applyTheme(loadTheme());          // poser le thème AVANT le branding (cf. brief E)
  wingConfig = loadWingConfig();
  loadState();
  applyWingBranding();
  renderEditorBindings();
  bindEditorEvents();
  bindTabBar();
  setActiveTab('meta');
  renderPreview();
  initOverflowObserver();  // chatE étape A : détection débordement via MutationObserver
  document.getElementById('btn-save').addEventListener('click', downloadJson);
  document.getElementById('btn-load').addEventListener('click', () => document.getElementById('file-load').click());
  document.getElementById('file-load').addEventListener('change', e => {
    if (e.target.files[0]) loadJsonFile(e.target.files[0]);
    e.target.value = '';
  });
  document.getElementById('btn-print').addEventListener('click', openExportModal);
  document.getElementById('btn-reset').addEventListener('click', resetAll);
  document.getElementById('theme-select').addEventListener('change', e => applyTheme(e.target.value));

  window.addEventListener('resize', () => {
    applyPreviewScale();
  });

  // Keyboard shortcuts (desktop)
  document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 's') { e.preventDefault(); downloadJson(); }
    if (e.ctrlKey && e.key === 'p') { /* let browser handle */ }
  });
}

document.addEventListener('DOMContentLoaded', init);

/* ============= EXPORT MODAL ============= */
function openExportModal() {
  const m = document.getElementById('export-modal');
  m.hidden = false;
  // Reset à l'état "choix initial"
  document.getElementById('export-png-config').hidden = true;
  document.querySelector('.export-modal-choices').hidden = false;
  document.getElementById('export-modal-title').textContent = 'Exporter le briefing';
  // Focus pour accessibilité
  document.getElementById('export-choice-pdf').focus();
}

function closeExportModal() {
  document.getElementById('export-modal').hidden = true;
}

function handleExportPdf() {
  closeExportModal();
  // Léger délai pour laisser la modale se fermer avant la boîte d'impression
  setTimeout(() => window.print(), 100);
}

/* ---- Step 2 : sélecteur de pages PNG ---- */

/* Extrait un hint lisible depuis un élément .page du DOM.
   Lit le premier .p-section trouvé dans la page — c'est le titre de section
   qui figure sur chaque page (OPÉRATION, SITAC, MISSION 1…, etc.).
   escapeHtml obligatoire : le contenu vient de données utilisateur. */
function pngPageHint(pageEl) {
  if (!pageEl) return '—';
  const sec = pageEl.querySelector('.p-section');
  if (sec && sec.textContent.trim()) return escapeHtml(sec.textContent.trim());
  return '—';
}

function updatePngExportCount() {
  const cbs = document.querySelectorAll('.export-png-page-cb:checked');
  const span = document.getElementById('export-png-count');
  if (!span) return;
  span.textContent = cbs.length ? '(' + cbs.length + ')' : '';
  const goBtn = document.getElementById('export-png-go');
  if (goBtn) goBtn.disabled = cbs.length === 0;
}

function handleExportPngChoice() {
  // S'assurer que l'aperçu est rendu (les .page doivent exister dans le DOM)
  // On ne force PAS le mode ici : les pages sont générées par renderPreview()
  // déjà appelé à l'init. On s'assure juste qu'elles sont dans le DOM.
  renderPreview();

  const allPageEls = document.querySelectorAll('#preview .page');
  const list = document.getElementById('export-png-list');
  if (!list) return;

  // Construire une checkbox par page — data-idx = index réel dans #preview
  list.innerHTML = '';
  allPageEls.forEach(function(pageEl, i) {
    const hint = pngPageHint(pageEl);
    const row = document.createElement('label');
    row.className = 'export-png-page-row';
    // Numéro de page padé sur 2 chiffres pour l'affichage
    const numStr = String(i + 1).padStart(2, '0');
    row.innerHTML =
      '<input type="checkbox" class="export-png-page-cb" data-idx="' + i + '" checked>' +
      '<span class="export-png-page-num">Page ' + numStr + '</span>' +
      '<span class="export-png-page-hint">' + hint + '</span>';
    list.appendChild(row);
  });

  // Passer au step 2 dans la modale
  document.querySelector('.export-modal-choices').hidden = true;
  document.getElementById('export-png-config').hidden = false;
  document.getElementById('export-modal-title').textContent = 'Export PNG kneeboard';
  updatePngExportCount();
}

/* ---- Rendu d'une page en PNG A4 natif (794×1123) ---- */

/* renderPageToPng — version chatF (consolidation post-chatE étape B)
   La classe .page--for-png réplique les règles @media print en CSS standard.
   html2canvas capture le clone avec scale: 1 explicite → PNG 794×1123 px exact,
   indépendamment du devicePixelRatio de l'appareil (FIX Bug A).
   Plus de second canvas, plus de drawImage, plus de scale 900/794, plus de
   fillRect, plus de cssText bricolé. Le bug de footer disparaît par construction
   (le footer est en position absolute dans la zone figée du clone). */
async function renderPageToPng(pageEl) {
  // Attendre que les polices custom soient chargées (Stardos Stencil, Special Elite…)
  // Évite le FOUT (Flash of Unstyled Text) dans les premiers PNG générés juste après
  // l'ouverture de la page.
  if (document.fonts && document.fonts.ready) {
    await document.fonts.ready;
  }

  const clone = pageEl.cloneNode(true);
  clone.classList.add('page--for-png');   // hérite de toutes les règles @media print via CSS
  // Positionné hors-écran — sans bricoler le layout interne du clone
  clone.style.position = 'fixed';
  clone.style.left = '-9999px';
  clone.style.top = '0';
  clone.style.zIndex = '-1';
  clone.style.pointerEvents = 'none';
  document.body.appendChild(clone);

  try {
    const canvas = await html2canvas(clone, {
      backgroundColor: null,   // la couleur de fond vient de la règle .page (--page-bg)
      logging: false,
      useCORS: true,
      allowTaint: false,
      scale: 1,   // FIX Bug A : forcer scale 1:1 (ignore devicePixelRatio) → 794×1123 px exact
    });

    return new Promise(function(resolve, reject) {
      canvas.toBlob(function(blob) {
        if (blob) resolve(blob);
        else reject(new Error('Conversion canvas → blob PNG échouée'));
      }, 'image/png');
    });

  } finally {
    // Cleanup systématique même en cas d'erreur
    if (clone.parentNode) clone.parentNode.removeChild(clone);
  }
}

/* ---- Export effectif (lancé par le bouton "Exporter (N)") ---- */
async function executePngExport() {
  // Récupérer les index de pages cochées (index réels dans #preview)
  const checkedInputs = document.querySelectorAll('.export-png-page-cb:checked');
  const checkedIdx = Array.from(checkedInputs).map(function(cb) {
    return parseInt(cb.dataset.idx, 10);
  });
  if (!checkedIdx.length) return;

  // Les .page sont toujours dans le DOM (mode édition ou aperçu),
  // querySelectorAll fonctionne indépendamment de la classe preview-only.
  // Aucun forçage de mode nécessaire.

  const allPageEls = document.querySelectorAll('#preview .page');
  const toExport = checkedIdx.map(function(i) { return allPageEls[i]; }).filter(Boolean);
  const total = toExport.length;

  // FIX R4 : feedback de progression (option 4)
  // La modale reste ouverte, le bouton devient "Génération X/N..." et le toast s'actualise
  const goBtn = document.getElementById('export-png-go');
  const originalBtnHtml = goBtn.innerHTML;
  goBtn.disabled = true;
  goBtn.setAttribute('aria-busy', 'true');

  function updateProgress(current) {
    const msg = 'Génération ' + current + '/' + total + '…';
    goBtn.innerHTML = msg;
    showToast(msg);
  }

  try {
    if (total === 1) {
      // Une seule page : téléchargement PNG direct
      updateProgress(1);
      const realIdx = checkedIdx[0];
      const fname = 'kb_' + String(realIdx + 1).padStart(2, '0') + '.png';
      const blob = await renderPageToPng(toExport[0]);
      closeExportModal();
      fallbackDownload(blob, fname, '1 page exportée ✓');

    } else {
      // Plusieurs pages : ZIP
      const zip = new JSZip();
      for (let i = 0; i < toExport.length; i++) {
        updateProgress(i + 1);
        const realIdx = checkedIdx[i];
        const fname = 'kb_' + String(realIdx + 1).padStart(2, '0') + '.png';
        const blob = await renderPageToPng(toExport[i]);
        zip.file(fname, blob);
      }
      const zipBlob = await zip.generateAsync({ type: 'blob' });
      closeExportModal();
      fallbackDownload(zipBlob, 'briefing_kneeboard.zip',
        total + ' pages exportées ✓');
    }
  } catch (err) {
    showToast('⚠ Erreur export PNG : ' + err.message);
    console.error('[Export PNG]', err);
  } finally {
    // Restauration systématique du bouton, même en cas d'erreur
    goBtn.innerHTML = originalBtnHtml;
    goBtn.disabled = false;
    goBtn.removeAttribute('aria-busy');
  }
}

// Bindings modale — câblés ici en global (pas dans init) pour rester cohérent
// avec le pattern "fonctions globales, pas de closures" du projet (cf. DOCS §2.4)
document.addEventListener('DOMContentLoaded', function bindExportModal() {
  document.getElementById('export-modal-backdrop').addEventListener('click', closeExportModal);
  document.getElementById('export-modal-close').addEventListener('click', closeExportModal);
  document.getElementById('export-choice-pdf').addEventListener('click', handleExportPdf);
  document.getElementById('export-choice-png').addEventListener('click', handleExportPngChoice);

  // Boutons Tout cocher / Tout décocher
  document.getElementById('export-png-all').addEventListener('click', function() {
    document.querySelectorAll('.export-png-page-cb').forEach(function(cb) { cb.checked = true; });
    updatePngExportCount();
  });
  document.getElementById('export-png-none').addEventListener('click', function() {
    document.querySelectorAll('.export-png-page-cb').forEach(function(cb) { cb.checked = false; });
    updatePngExportCount();
  });

  // Mise à jour compteur au changement d'une checkbox (délégation sur le container)
  document.getElementById('export-png-list').addEventListener('change', function(e) {
    if (e.target.classList.contains('export-png-page-cb')) updatePngExportCount();
  });

  // Bouton Exporter (N) — lance l'export effectif
  document.getElementById('export-png-go').addEventListener('click', executePngExport);

  // Bouton ← Retour — revient au step 1 (choix PDF/PNG)
  document.getElementById('export-png-back').addEventListener('click', function() {
    document.getElementById('export-png-config').hidden = true;
    document.querySelector('.export-modal-choices').hidden = false;
    document.getElementById('export-modal-title').textContent = 'Exporter le briefing';
  });

  // Échap pour fermer la modale (quelle que soit l'étape)
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && !document.getElementById('export-modal').hidden) {
      closeExportModal();
    }
  });
});

/* ============= CONSOLE API ============= */
/* All functions below are globally accessible from the browser console.
   No IIFE wrapping — window scope is intentional (cf. DOCS §2.4).

   Wing config read/write:
     wingConfig                          // current wing object (mutable)
     loadWingConfig()                    // → parsed localStorage or DEFAULT_WING_CONFIG
     persistWingConfig()                 // debounced save → localStorage[KEY_WING]
     validateWingConfig(obj)             // → { ok, errors[] }

   Import / Export / Reset:
     exportWingConfig()                  // → downloads wing_config_<id>_<ts>.json
     importWingConfig(file)              // file = File object from <input type="file">
     resetWingConfig()                   // → confirm → DEFAULT_WING_CONFIG + localStorage.removeItem

   Branding refresh (always call after mutating wingConfig directly):
     applyWingBranding()

   Quick test sequence (paste in console):
     wingConfig.wing.shortName = 'TEST WING';
     applyWingBranding();                // toolbar title changes immediately
     exportWingConfig();                 // download JSON file
     // Reload page → title back to 'MY WING' (not persisted — expected)
     // To persist: persistWingConfig() — normally called by the wing editor
*/
</script>

</body>
</html>
"""

# ── Generic SVG logos (hardcoded, option C) ──────────────────────────────────
# These are the default wing/squadron logos for the generic "MY WING" config.
# They are embedded as base64 data URLs so the app has no external dependencies.
# Colors: #a8945e (kaki accent) · #2a3038 (anthracite) · #d4c598 (kraft beige)

_GENERIC_WING_LOGO_SVG = '''\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="115" fill="#d4c598"/>
  <circle cx="128" cy="128" r="115" fill="none" stroke="#a8945e" stroke-width="14"/>
  <circle cx="128" cy="128" r="90" fill="none" stroke="#a8945e" stroke-width="5"/>
  <circle cx="128" cy="128" r="70" fill="none" stroke="#a8945e" stroke-width="2"/>
  <text x="128" y="158" text-anchor="middle"
        font-family="Arial Black, Arial, sans-serif"
        font-weight="900" font-size="86" fill="#2a3038" letter-spacing="-3">WG</text>
</svg>'''

_GENERIC_SQN_LOGO_SVG = '''\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="115" fill="#d4c598"/>
  <circle cx="128" cy="128" r="115" fill="none" stroke="#a8945e" stroke-width="14"/>
  <circle cx="128" cy="128" r="90" fill="none" stroke="#a8945e" stroke-width="5"/>
  <circle cx="128" cy="128" r="70" fill="none" stroke="#a8945e" stroke-width="2"/>
  <text x="128" y="158" text-anchor="middle"
        font-family="Arial Black, Arial, sans-serif"
        font-weight="900" font-size="86" fill="#2a3038" letter-spacing="-3">01</text>
</svg>'''

_GENERIC_WING_LOGO_DATAURL = (
    'data:image/svg+xml;base64,' +
    base64.b64encode(_GENERIC_WING_LOGO_SVG.encode('utf-8')).decode('ascii')
)
_GENERIC_SQN_LOGO_DATAURL = (
    'data:image/svg+xml;base64,' +
    base64.b64encode(_GENERIC_SQN_LOGO_SVG.encode('utf-8')).decode('ascii')
)
# ─────────────────────────────────────────────────────────────────────────────


def build_default_wing_config(A):
    """Build the embedded default wing config (generic placeholder).

    This is the single source of truth for the default wing.  At runtime,
    the JS reads `wingConfig.wing.*` and `wingConfig.squadrons[*].logo`
    instead of hardcoded constants.

    The 4th VEAW config is distributed separately as wing_config_4th-veaw.json
    and can be imported via the wing editor (📥 Importer config).

    Returns a dict matching the wing_config.json schema (configSchemaVersion 1).
    """
    return {
        "configSchemaVersion": 1,
        "wing": {
            "id": "MY-WING",
            "shortName": "MY WING",
            "fullName": "Mon Wing Virtuel",
            "appTitle": "GÉNÉRATEUR DE BRIEFING",
            "logo": _GENERIC_WING_LOGO_DATAURL,
            "hqStamp": "HQ ░ MY WING",
        },
        "squadrons": [
            {
                "id": "SQN-01",
                "name": "1st Squadron",
                "nickname": "Demo",
                "callsign": "ALPHA",
                "aircraft": ["F-16C Viper"],
                "logo": _GENERIC_SQN_LOGO_DATAURL,
            },
        ],
    }


# Serialise the default config as a JS string literal.
# json.dumps(json.dumps(...)) double-encodes:
#   * inner dump  → produces a valid JSON document
#   * outer dump  → wraps it in a valid JS-quoted string with proper escaping
# At runtime, JS unquotes the string then JSON.parse turns it into an object.
# Faster than parsing as a JS object literal and safer w.r.t. embedded quotes.
_default_wing_config = build_default_wing_config(A)
_default_wing_config_js = json.dumps(
    json.dumps(_default_wing_config, ensure_ascii=False)
)

HTML = HTML.replace('__CSS__', CSS)
HTML = HTML.replace('__LIB_HTML2CANVAS__', A['lib_html2canvas'])
HTML = HTML.replace('__LIB_JSZIP__', A['lib_jszip'])

# ── KRAFT TEXTURES — Phase X étape B ─────────────────────────────────────────
# Le SVG kraft d'origine ne contient que 2 couleurs hex : #d6c7a3 (fond, 1×) et
# #ccbe99 (grain, 139×). On génère 4 variantes thématiques par str.replace pur,
# encodées en base64 et embarquées via 4 placeholders distincts dans le CSS
# (un par bloc body[data-theme="..."]).
#
# Le grain est dérivé du fond avec le même décalage que l'original
# (delta R=-10, G=-9, B=-10 décimaux), pour conserver l'effet "papier" sur
# tous les thèmes.

def modulate_kraft(svg_str, fond_hex, grain_hex):
    """Substitue les 2 couleurs principales du SVG kraft.
    Le SVG original utilise #d6c7a3 (fond) et #ccbe99 (grain horizontal)."""
    return svg_str.replace('#d6c7a3', fond_hex).replace('#ccbe99', grain_hex)

_kraft_svg_str = base64.b64decode(A['KRAFT_SVG']).decode('utf-8')

_kraft_themes = {
    'NATO':         ('#d6c7a3', '#ccbe99'),  # cw-nato (original — preservé)
    'SOVIET':       ('#d4c075', '#cab76b'),  # cw-soviet — ocre chaud
    'MODERN_NATO':  ('#e4dfd2', '#dad6c8'),  # modern-nato — blanc cassé
    'MODERN_EAST':  ('#c8c1b2', '#beb8a8'),  # modern-east — papier grisé
}

for _key, (_fond, _grain) in _kraft_themes.items():
    _modulated_svg = modulate_kraft(_kraft_svg_str, _fond, _grain)
    _b64 = base64.b64encode(_modulated_svg.encode('utf-8')).decode('ascii')
    HTML = HTML.replace(f'__KRAFT_SVG_{_key}__', _b64)

HTML = HTML.replace('__DEFAULT_WING_CONFIG__', _default_wing_config_js)
HTML = HTML.replace('__APP_VERSION__', APP_VERSION)

# Write the final file
output_path = os.path.join(HERE, 'DCS_World_Briefing_Generator.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"File written: {len(HTML):,} bytes ({len(HTML)/1024:.1f} KB)")
print(f"Path: {output_path}")
