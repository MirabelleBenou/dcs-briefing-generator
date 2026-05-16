# DCS World Briefing Generator — Documentation technique

### 1. Vue d'ensemble

Application HTML monofichier offline (~825 Ko). Génère des briefings militaires au format A4, style "document kraft" années 80, pour le simulateur DCS World. Conçue pour tablette (900px) avec interface éditeur + prévisualisation temps réel. Export PDF (impression navigateur) et **PNG kneeboard** (page unique ou ZIP multipages, format 794×1123 A4 strict).

**Fichiers du projet :**

| Fichier | Rôle |
|---|---|
| `build_html.py` | Template HTML + JavaScript complet (~3 700 lignes) |
| `build_css.py` | CSS complet (~2 000 lignes) |
| `assets.json` | Logos base64 + fond SVG kraft + html2canvas + JSZip (export PNG) |
| `briefing.css` | Intermédiaire généré par `build_css.py`, consommé par `build_html.py` (non commit) |
| `DCS_World_Briefing_Generator.html` | Livrable final (généré par le build) |
| `wing_config_4th-veaw.json` | Exemple de configuration wing 4th VEAW |

**Build :**
```bash
python3 build_css.py && python3 build_html.py
```
Le CSS est généré d'abord, puis injecté dans le HTML. Les assets (logos, SVG, libs) sont injectés via des placeholders `__KRAFT_SVG__`, `__DEFAULT_WING_CONFIG__`, `__LIB_HTML2CANVAS__`, `__LIB_JSZIP__` remplacés par `str.replace()` dans `build_html.py`.

Les scripts utilisent des chemins relatifs à eux-mêmes (`HERE = os.path.dirname(os.path.abspath(__file__))`), donc fonctionnels sur n'importe quel poste sans modification.
````
---

## 2. Architecture

### 2.1 Responsive

| Breakpoint | Mode |
|---|---|
| ≥ 1100px | Desktop : éditeur gauche (40%) + aperçu droite (60%) |
| < 1100px | Tablette : 11 onglets en barre du bas + page plein écran |

> **⚠ Règle critique :** toute nouvelle section éditeur doit avoir son `data-active-tab` ajouté au mapping `@media (max-width: 1100px)` dans `build_css.py`, sinon la section est invisible en tablette portrait (bug constaté lors de l'ajout de la section Annexes en v2.1.0).

### 2.2 Stack technique

- **HTML/CSS/JS vanilla** — aucune dépendance externe, pas de framework
- **LocalStorage** — persistance automatique des données (`khr26_briefing_state_v2`)
- **Impression PDF** — via `window.print()` du navigateur (Chrome/Brave recommandé)
- **Images** — compressées via `canvas.toDataURL('image/jpeg', 0.82)` avant stockage

### 2.3 Fond SVG kraft

Le fond papier kraft est un fichier SVG A4 (210×297mm) encodé en base64, stocké dans `assets.json` sous la clé `KRAFT_SVG`. Il est injecté dans le CSS via le placeholder `__KRAFT_SVG__`.

**Screen :** `background-image` direct sur `.page` avec `background-size: 100% 100%`.

**Print :** même approche. Important : **ne pas utiliser `display: grid` ou `column-count`** sur des éléments enfants de `.page` en impression — cela crée des couches GPU (compositing layers) dans Skia/Chromium qui peuvent faire disparaître ou doubler des pages dans le PDF. Utiliser `display: block` ou `flex-wrap` simples à la place.

### 2.4 JavaScript — accès global

Le JS est **non encapsulé dans une IIFE** — `state`, `renderPreview`, etc. sont accessibles globalement. Pour les tests Playwright :

```javascript
// Injection de state puis refresh du preview
state.phases[0].title = 'Test';
renderPreview();

// Ou injection complète via localStorage
localStorage.setItem('khr26_briefing_state_v2', JSON.stringify(data));
location.reload();
```

---

## 3. Structure du State

Clé localStorage : `khr26_briefing_state_v2`

```javascript
state = {

  meta: {
    operation: 'FOOTHOLD',
    mission: 'M3',
    date: '1989-03-22',          // ISO date
    classification: 'CONFIDENTIEL DÉFENSE',
    docRef: 'VEAW-FH-M3-1989'   // Référence affichée dans les footers
  },

  cover: {
    title: 'OPERATION FOOTHOLD',
    narrative: '...',            // Contexte (multi-paragraphes, \n\n)
    mapImage: ''                 // data URL base64 JPEG
  },

  sitac: {
    date: '22-03-1989',
    points: ['...'],             // Points de situation (string[])
    metar: 'LCRA 221000Z ...',
    mapImage: ''
  },

  mission: {
    objectives: ['...'],         // Objectifs globaux (string[])
    farp: ['...'],               // FARP / aéroports (string[])
    threats: {
      tanks: 'T-55 à T-80',
      apc: 'BRDM-2, BMP-1, ...',
      aaa: 'ZU-57, ZU-23, ...',
      sam: 'Manpads, SA-8, ...',
      note: '...'
    }
  },

  radioPlan: {
    items: [                     // Items globaux, max 6, page Aperçu Mission
      { id: 'atc', label: 'ATC', frequency: '270.00', modulation: 'AM' }
      // modulation: 'AM' | 'FM'
    ],
    aircraftPlans: [             // Plans par appareil → pages annexes radio
      {
        aircraft: 'Mi-24P',
        radios: [
          {
            name: 'R-863',
            channels: [
              {
                channel: 0,
                mode: 'item',    // 'item' = lié à un item global
                itemId: 'grp1'
                // Si mode = 'custom':
                // label, frequency, modulation libres
              }
            ]
          }
        ],
        image: ''                // data URL si on préfère une image à la table
      }
    ]
  },

  phases: [                      // Missions (une par page)
    {
      title: 'Titre de la mission',
      objective: '...',
      execution: [
        {
          text: 'Étape principale',
          subtasks: ['a) sous-tâche 1']    // Affiché a) b) c) dans le PDF
        }
      ],
      flightPlan: 'CAP 352° / Distance 34 Km',
      threatLevel: 'Faible',     // 'Faible' | 'Modéré' | 'Élevé'
      notes: '...',
      images: [                  // Pages dédiées, 2 images par page max
        { title: '...', data: '', caption: '...' }
      ],
      squadron: 'KHR-26',        // ID escadron ou '__guest__'
      aircraft: 'Mi-8',          // Appareil sélectionné
      subgroup: 'ANTON',         // Optionnel — remplace le callsign dans l'affichage
      guestSquadron: {
        name: 'WOLF',            // Nom de l'escadron invité (= son identifiant)
        subgroup: '',            // Nom du groupe invité (optionnel)
        aircraft: 'F-16CM'
      }
    }
  ],

````javascript
  charts: [                      // Pages charts aéroports — liste dynamique illimitée
    { name: 'AKROTIRI (LCRA) — Piste en service : 10', img: '' },
    { name: 'PAPHOS (LCPH) — Piste en service : 11', img: '' }
  ],

  annexes: [                     // Pages annexes libres — liste dynamique illimitée
    { title: 'Notes additionnelles', img: '', caption: 'Commentaire optionnel' }
  ],
````

  roster: {
    groups: [
      {
        // Clé unique = '${id}||${subgroup}||${aircraft}'
        // Exemples: 'KHR-26||ANTON||Mi-8', 'WOLF||WOLF 1||F-16CM'
        missionKey: 'KHR-26||ANTON||Mi-8',
        pilots: [
          { name: 'MirabelleBenou', callsign: 'Anton 1-1' }
        ]
      }
    ]
  }
};
```

### Normalisations au chargement

Appelées dans `loadState()` et `loadJsonFile()`, **jamais dans `buildPages()`** :

| Fonction | Transformation |
|---|---|
| `normalizeExecution(exec)` | `string[]` legacy → `{text, subtasks[]}[]` |
| `normalizePhaseImages(ph)` | `ph.mapImage` legacy → `ph.images[{title,data,caption}]` |
| `normalizeCharts(state)` | `annexes.chart1*/chart2*` legacy → `state.charts[{name,img}]` |
| `normalizeAnnexes(state)` | Normalise `state.annexes[{title,img,caption}]` |
| `normalizeThreatLevel(lvl)` | `'Danger'`/`'Important'` → `'Élevé'` |

> **⚠ Règle critique :** Ne jamais appeler `normalizePhaseImages(ph)` dans `buildPages()`. Cette fonction fait `ph.images = ph.images.map(...)`, ce qui remplace le tableau par un nouveau et invalide toutes les closures des event listeners de `renderPhaseImages`. Cela cause des bugs où titre/caption/upload/suppression semblent ne pas fonctionner.

---

## 4. Escadrons disponibles

Les escadrons ne sont plus codés en dur dans le HTML. Ils font partie de la **configuration wing** (`wing_config.json`), chargée dynamiquement à l'ouverture de l'application.

**À l'ouverture :** l'application charge `wing_config_v1` depuis le localStorage. Si absent, le wing par défaut embarqué (4th VEAW) s'applique.

**Accès JS :**
```javascript
wingConfig.squadrons   // tableau des escadrons du wing courant
getSquadron(id)        // retrouve un escadron par son id
```

**Logique d'affichage (chip + roster) :**
- Sous-groupe défini → `KHR-26 ░ ANTON` (remplace le callsign FRANKEN)
- Sans sous-groupe → `KHR-26 ░ FRANKEN`

**Escadron invité (`__guest__`) :** champs libres — aucun logo, affiché grisé dans la prévisualisation.

**Compatibilité des briefings existants :** si un briefing référence un escadron absent du wing chargé, il s'affiche grisé/vide sans crash.

Pour ajouter, modifier ou supprimer un escadron, utilisez l'interface de l'onglet **09 ░ WING** — aucun build n'est nécessaire. Voir § 13 pour le détail.

---

## 5. Fonctions JS principales

| Fonction | Rôle |
|---|---|
| `init()` | Bootstrap : charge wing + state + attache les bindings |
| `applyWingBranding()` | Met à jour titre, toolbar, logos depuis `wingConfig` |
| `buildPages()` | Construit `pages[]` — pur, sans side effects sur le state |
| `renderPreview()` | Injecte le HTML des pages dans `#preview` |
| `schedulePreview()` | Debounce 200ms → `persistState()` + `renderPreview()` |

---

## 6. Fonctions de rendu éditeur

| Fonction | Rôle |
|---|---|
| `renderEditorBindings()` | Attache les `[data-bind]` sur tous les champs |
| `renderPhases()` | Liste + navigation des missions |
| `renderPhaseFields(ph, idx)` | Champs d'une mission : escadron, exécution, etc. |
| `renderPhaseImages(listEl, phaseIdx)` | Images : upload / titre / caption / suppression |
| `renderRadioPlan()` | Items globaux + plans par appareil |
| `renderChannels(container, ai, ri)` | Canaux d'une radio |
| `renderRoster()` | Groupes équipage avec SELECT dynamique |
| `renderPilots(container, gi)` | Lignes pilotes d'un groupe |
| `renderCharts()` | Liste dynamique des charts (nom + image, ajout/suppression) |
| `renderAnnexes()` | Liste dynamique des annexes libres (titre + image + caption) |

> **⚠ `renderPhaseImages` — règle des closures :** tous les event listeners utilisent `state.phases[phaseIdx].images[k].xxx` directement. Ne jamais capturer `imgs[k]` (référence objet) — capturer uniquement les primitifs `phaseIdx` et `k`.

### Roster helpers

| Fonction | Retour exemple |
|---|---|
| `getMissionGroups()` | `[{key:'KHR-26||ANTON||Mi-8', id, callsign, aircraft, subgroup, isGuest}]` |
| `getRosterLabelParts(keyOrGroup)` | `{shortLabel:'ANTON', label:'KHR-26 ░ ANTON', fullLabel:'KHR-26 ░ ANTON — Mi-8'}` |
| `getRosterLabel(k)` | `'KHR-26 ░ ANTON'` |
| `getRosterShortLabel(k)` | `'ANTON'` (utilisé pour auto-callsign) |

### Preview et persistance

| Fonction | Rôle |
|---|---|
| `schedulePreview()` | Debounce 200ms → `persistState()` + `renderPreview()` |
| `buildPages()` | Construit `pages[]` — pur, sans side effects sur le state |
| `renderPreview()` | Injecte le HTML des pages dans `#preview` |
| `persistState()` | Sauvegarde dans localStorage |
| `loadState()` | Charge + normalise depuis localStorage |
| `loadJsonFile(file)` | Import JSON → normalisation → rechargement |
| `downloadJson()` | Export JSON |

### Utilitaires

| Fonction | Rôle |
|---|---|
| `compressImageFile(file)` | `Promise<{dataUrl}>` — JPEG via canvas |
| `imgFrame(label, url)` | `<div class="p-imgframe">` avec fallback hachures |
| `getPhaseSquadronInfo(ph)` | `{id, callsign, aircraft, subgroup, logo, isGuest}` |
| `threatClass(lvl)` | `'t-faible'` / `'t-modere'` / `'t-eleve'` |
| `genId(prefix)` | ID aléatoire (`prefix_xxxxxxxx`) |
| `escapeHtml(s)` / `escapeAttr(s)` | Sanitisation XSS |

---

## 7. Sections éditeur (onglets)

| Section | `data-section` / `data-tab` | Contenu |
|---|---|---|
| 00 Métadonnées | `meta` | Opération, mission, date, classification, réf. doc |
| 01 Couverture | `cover` | Titre, narratif, carte théâtre |
| 02 SITAC | `sitac` | Date, points situation, METAR, carte tactique |
| 03 Aperçu Mission | `mission` | Objectifs, FARP, menaces |
| 04 Plan Radio | `radio` | Items globaux (max 6) + plans par appareil |
| 05 Missions | `phases` | N missions : exécution, images, escadrons |
| 07 Équipage | `roster` | Groupes pilotes liés aux missions |
| 08 Charts | `charts` | Charts aéroports — liste dynamique illimitée (v2.1.0) |
| 09 Annexes | `annexes` | Pages annexes libres — liste dynamique illimitée (v2.1.0) |
| 10 Wing | `wing` | Configuration du wing : branding, escadrons |
| — Aperçu | `preview` | Prévisualisation PDF (tablette uniquement) |

> Note v2.1.0 : la section 06 a été retirée (anciennement Plan Radio détaillé, désormais intégré dans 04). La section 08 anciennement "Annexes" est devenue "Charts" avec liste dynamique illimitée. Une nouvelle section 09 "Annexes" libre a été créée. La section Wing est passée de 09 à 10.


### Bindings déclaratifs

```html
<!-- Binding simple état → champ -->
<input data-bind="meta.operation" type="text">
<textarea data-bind="cover.narrative"></textarea>
<input data-img-bind="sitac.mapImage">   <!-- zone image drag/drop -->
```

`renderEditorBindings()` attache `addEventListener('input', ...)` sur tous les `[data-bind]`.

### Éditeur missions (phases)

Navigation par flèches ◄ ► (`currentPhaseIdx`). Boutons : `+` ajouter, `⧉` dupliquer, `↑↓` réordonner, `×` supprimer.

Champs par mission :
- Titre, escadron (select), appareil (radio buttons), sous-groupe (optionnel)
- Pour invité : Nom de l'escadron / Nom du groupe (optionnel) / Type d'appareil
- Objectif, étapes d'exécution (ordonnables ▲▼ avec sous-tâches), plan de vol
- Niveau de menace (select), notes tactiques
- Images (+ Ajouter une image → titre + upload + légende)

---

## 8. CSS — Architecture principale

### Variables CSS (`:root`)

```css
--ink: #1a1208            /* texte */
--paper: #d6c7a3          /* fond kraft */
--paper-light: #ddd2b8    /* fond léger */
--paper-edge: #c4b490     /* bordures */
--olive-deep: #2c321e     /* vert militaire profond (bandeaux) */
--olive: #4a5230
--amber: #d4a017          /* or (accents, titres) */
--rust: #8b2020           /* rouge rouille (callsigns) */
--khaki: #8a7d5a

--f-stencil: 'Special Elite', serif      /* titres stencil militaire */
--f-condensed: 'Barlow Condensed', sans  /* libellés compacts */
--f-typewriter: 'Courier Prime', mono    /* texte machine à écrire */
--f-mono: 'Share Tech Mono', mono        /* fréquences, codes */
```

### Classes de page

| Classe | Rôle |
|---|---|
| `.page` | Conteneur A4 — fond SVG kraft |
| `.page--for-png` | Variante du `.page` utilisée pour le clone html2canvas lors de l'export PNG (réplique les règles `@media print` en CSS standard) |
| `.p-header` | En-tête (logos + titre + sous-titre) |
| `.p-header-logo` | Conteneur `<div>` des logos du header (remplace `<img>`, utilise `background-image` pour compatibilité html2canvas) |
| `.p-footer` | Pied de page absolu (position: absolute; bottom: 8mm) |
| `.p-section` | Bandeau pleine largeur (titre section) |
| `.p-subsection` | Sous-titre |
| `.p-imgframe` | Cadre image (hachures si vide, centré avec `margin: auto`) |
| `.p-annexe-caption` | Commentaire optionnel affiché sous l'image dans une page annexe libre |
| `.p-bullets` | Liste à puces |
| `.p-2col` | 2 colonnes (radio annexes) |
| `.squadron-chip` | Identifiant escadron dans les missions (`display: flex; width: fit-content` pour compatibilité html2canvas) |
| `.squadron-grid` | Grille escadrons engagés (cellules identiques) |
| `.squadron-logo-sm` | Logo d'escadron 38×38 ou 32×32, utilisé en `<div background-image>` (pas `<img>`) pour compatibilité html2canvas |
| `.roster-mega` | Tableau roster 4 colonnes |


### Print CSS (`@media print`)

```css
.page {
  width: 210mm; height: 297mm; overflow: hidden;
  break-after: page;
  background-image: url('data:image/svg+xml;base64,...'); /* kraft SVG */
}
.page > * { position: relative; z-index: 1; } /* contenu au-dessus du fond */
.p-footer { position: absolute; bottom: 8mm; } /* ancré en bas */
```

---

## 9. Bugs résolus — référence rapide

### `renderPhaseImages` — frappe lettre par lettre / Suppr. inefficace

**Cause :** `normalizePhaseImages(ph)` dans `buildPages()` remplace `ph.images` → closures orphelines.

**Fix :** supprimer l'appel de `normalizePhaseImages` dans `buildPages()`. Dans `renderPhaseImages`, utiliser `state.phases[phaseIdx].images[k]` (jamais `imgs[k]`).

### Page Équipage : disparition / doublement dans le PDF

**Cause :** `display: grid` ou `column-count` sur des enfants de `.page` en impression créent des compositing layers GPU dans Skia/Chromium, capturés comme des pages PDF séparées.

**Fix :** utiliser **un seul `<table>`** par paire de groupes (plus d'éléments multiples avec backgrounds séparés). Aucun `column-count` ou `display: grid` dans les règles `@media print` pour le roster.

### Images annexes débordant en bas de page

**Cause :** `width: 100%` sans contrainte de hauteur.

**Fix :** `max-width: 100%; width: auto; height: auto; max-height: 560px; margin: 0 auto`.

### Cellules escadrons de tailles inégales (Aperçu Mission)

**Cause :** CSS grid `1fr` — la dernière cellule s'étire.

**Fix :** `display: flex; flex-wrap: wrap` + `flex: 0 0 calc(33.333% - 5.334px)` sur `.squadron-cell`.

### Footer remontant / textes invisibles après ajout de `.page-kraft`

**Cause :** sélecteur `.page > *:not(.page-kraft)` avec spécificité `0,2,0` écrase `.p-footer { position: absolute }` de spécificité `0,1,0`.

**Fix :** ne pas utiliser `:not()` dans les sélecteurs généraux sur `.page > *` — conserver `background-image` directement sur `.page`.

### Régression `btn-mode` (binding perdu — v2.1.0)

**Cause :** lors d'une refonte intermédiaire, l'instruction `document.getElementById('btn-mode').addEventListener('click', toggleMode)` a été perdue. Le bouton œil/aperçu de la toolbar ne réagissait plus.

**Fix :** suppression définitive du bouton (redondant avec la tab-bar mobile sur tablette et inutile sur desktop). Nettoyage complet de `toggleMode()`, `.app.preview-only`, `mode-label`, et du forçage `preview-only` dans `executePngExport()`.

### PNG en 1985×2807 au lieu de 794×1123 (Bug A — v2.1.0)

**Cause :** html2canvas applique par défaut `scale = window.devicePixelRatio` (= 2.5 sur Xiaomi Pad 6). Le commentaire de spec affirmant "scale par défaut = 1" était trompeur.

**Fix :** `scale: 1` explicite dans les options `html2canvas()` de `renderPageToPng()`. Garantit un PNG de 794×1123 px exact, indépendamment du devicePixelRatio.

### Logos déformés en PNG (Bug B — v2.1.0)

**Cause :** html2canvas gère mal `<img>` + `object-fit: contain` (bugs documentés issues html2canvas #1322 et #2425). Les images sont étirées pour remplir leur boîte au lieu de préserver leur ratio.

**Fix :** remplacement systématique des `<img>` capturés en PNG par des `<div>` avec `background-image` inline (data URL) + `background-size: contain`. Pattern recommandé par la communauté html2canvas. Concerné : `.squadron-logo-sm` (page Aperçu Mission) et `.p-header img` → `.p-header-logo` (header de toutes les pages).

### Rectangle vide à la place du nom d'escadron en PNG (Bug C — v2.1.0)

**Cause :** html2canvas gère mal `display: inline-flex` combiné avec `overflow: hidden`. La bordure est rendue mais le contenu interne (les 3 `<span>` colorés du chip) est absent.

**Fix :** `display: flex; width: fit-content` sur `.squadron-chip` au lieu de `display: inline-flex`. Sémantiquement équivalent, mais correctement géré par html2canvas.

### Bug intermittent "page qui disparaît" (v2.1.0)

**Cause :** race condition entre régénération DOM (`buildPages()` réécrit `#preview.innerHTML`), chargement des polices web, et repaints navigateur. Reproductible 1 fois sur 5-10 tentatives, cross-browser (constaté Brave + Chrome + Firefox).

**Fix CSS préventif multi-couches** (aucune touche au JS) :
1. `font-display: block` → `font-display: swap` (4 occurrences `@font-face`) — élimine le black-out 3 secondes
2. Suppression de `-webkit-overflow-scrolling: touch` (déprécié, activait du compositing inutile)
3. Ajout de `overscroll-behavior: contain` sur `.editor` et `.preview-wrap` — isole le scroll, prévient les reflows en cascade
4. Ajout de `contain: layout` sur `.ed-section` — isole le layout des sections éditables, réduit la pression sur le moteur de rendu

### Section Annexes invisible en tablette portrait (v2.1.0)

**Cause :** lors de l'ajout de la nouvelle section Annexes (v2.1.0), le mapping `@media (max-width: 1100px) [data-active-tab="annexes"] .ed-section[data-section="annexes"]` a été oublié dans `build_css.py`. La règle générale `body:not([data-active-tab="preview"]) .ed-section { display: none; }` cachait toutes les sections, et aucune règle ne ré-affichait Annexes.

**Fix :** ajout de `body[data-active-tab="annexes"] .ed-section[data-section="annexes"]` dans la liste du bloc `@media (max-width: 1100px)`.

**Règle de prévention :** voir § 2.1 — toute nouvelle section éditeur doit avoir son `data-active-tab` ajouté à ce mapping responsive.

### Images de charts débordant la page A4 (v2.1.0)

**Cause :** `max-height: 230mm` sur `.p-imgframe img` était trop ambitieux. La page A4 fait 297mm de hauteur, mais le header (logos + titre, ~25mm) + p-section (~10mm) + p-subsection (~8mm) + footer (~10mm) + padding (~20mm) consomment ~75mm. Reste ~222mm utilisables — moins 5mm de marge sécurité = **200mm sûr**.

**Fix :** `max-height: 200mm` sur `.p-imgframe img`. Compromis entre agrandissement (vs 190mm origine) et marge de sécurité (vs 230mm trop large).
---

## 10. Persistance et Import/Export

### Briefing (state)

| Action | Mécanisme |
|---|---|
| Sauvegarde automatique | Debounce 200ms → `localStorage.setItem(KEY, JSON.stringify(state))` |
| Export JSON | `downloadJson()` → fichier `briefing_[op]_[mission]_[ts].json` |
| Import JSON | `loadJsonFile(file)` → `mergeDeep(DEFAULTS, parsed)` + normalisations |
| Reset | `state = structuredClone(DEFAULTS)` + confirmation |

Clé localStorage : `khr26_briefing_state_v2` (**immuable** — ne jamais renommer, sous peine de perdre les briefings des utilisateurs).

### Configuration wing

| Action | Mécanisme |
|---|---|
| Sauvegarde automatique | À chaque modification dans l'onglet 09 ░ WING |
| Export JSON | Bouton « 📤 Exporter config » → fichier `wing_config_[wingId].json` |
| Import JSON | Bouton « 📥 Importer config » → écrase intégralement le wing courant |
| Reset | Bouton « ↺ Réinitialiser » → revient au wing 4th VEAW embarqué |

Clé localStorage : `wing_config_v1`.

---

## 11. Callsigns automatiques (roster)

À l'ajout d'un pilote :
```javascript
const prefix = getRosterShortLabel(grp.missionKey);
// Exemples: 'ANTON' (sous-groupe), 'DUFF' (callsign sans sous-groupe), 'WOLF' (invité)
const autoCallsign = `${prefix} 1-${pilotIndex + 1}`;
// Résultat: 'Anton 1-1', 'Anton 1-2', 'Duff 1-1', 'Wolf 1-1'
```

Le callsign est toujours éditable manuellement après génération.

---

## 12. Notes pour les futures sessions

1. **Ne jamais appeler `normalizePhaseImages(ph)` dans `buildPages()`** — normalisations uniquement au chargement.

2. **Pour tout nouveau layout en print sur les pages équipage** — tester avec 5 générations PDF et comparer les hashes PNG des pages concernées via `pdftoppm` + `md5sum`.

3. **Ajouter un escadron** : utiliser l'interface de l'onglet **09 ░ WING** (bouton « + Ajouter un escadron »). Renseigner id, nom, callsign, appareils, logo. Exporter ensuite la config pour la distribuer. Aucune modification de `build_html.py` ni d'`assets.json` n'est nécessaire pour les utilisateurs finaux. Pour l'embarquer dans le build comme nouveau défaut, ajouter l'entrée dans `build_default_wing_config()` dans `build_html.py` et régénérer.

4. **Ajout d'une page PDF** : `pages.push({body, rightLogo?, rightAlt?})` dans `buildPages()` à la bonne position dans le flux.

5. **Pattern test Playwright** :
```python
await page.evaluate("""
    state.phases[0].title = 'Test';
    renderPreview();
""")
pdf = await page.pdf(format='A4', print_background=True,
                    margin={'top':'0','bottom':'0','left':'0','right':'0'})
```
Il est désormais possible de tester avec plusieurs configurations wing : injecter un wing de test via `localStorage.setItem('wing_config_v1', JSON.stringify(testWingConfig)); location.reload()` avant d'évaluer.

6. **La page équipage doit avoir une seule `<table>` par paire de groupes** — c'est une contrainte architecturale pour la stabilité du rendu PDF, pas juste un choix esthétique.

### Pièges JavaScript / CSS / html2canvas connus

**Pièges JavaScript :**
- **Ne JAMAIS écrire `*/` dans un commentaire de bloc** (même dans une chaîne ou un commentaire de spec partagé entre humains). Cela ferme prématurément le bloc et casse tout le script suivant. Préférer les commentaires `//` sur une ligne.
- **`node --check` sur le script extrait du HTML** est un garde-fou efficace contre les erreurs de syntaxe introduites par mégarde. Pattern :
  ```python
  import re
  with open('DCS_World_Briefing_Generator.html') as f: html = f.read()
  scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
  with open('/tmp/main.js', 'w') as f: f.write(scripts[3])
  # node --check /tmp/main.js
  ```

**Pièges CSS responsive :**
- **Toute nouvelle section éditeur doit avoir son `data-active-tab` ajouté au mapping `@media (max-width: 1100px)`** dans `build_css.py`, sinon elle est invisible en tablette portrait.

**Pièges html2canvas (export PNG) :**
- **Toute `<img>` qui sera capturée en PNG doit utiliser `<div background-image>` à la place** — `object-fit: contain` est mal géré par html2canvas et déforme les images.
- **Toute `display: inline-flex` + `overflow: hidden` capturée en PNG doit passer en `display: flex; width: fit-content`** — sinon la bordure est rendue mais pas le contenu.
- **Forcer `scale: 1` explicitement** dans les options `html2canvas()`, sinon `devicePixelRatio` est appliqué par défaut (× 2 ou × 3 selon l'appareil).

**Pièges build pipeline :**
- **Toujours rebuild le HTML après modif des `.py`**, puis grep sur le HTML final (pas sur les `.py`). Une livraison Sonnet apparemment correcte côté source peut produire un HTML incorrect si le rebuild s'est fait sur une ancienne copie.
````


---

## 13. Configuration multi-wings

### Concept

Le DCS World Briefing Generator est **agnostique au wing**. À l'ouverture, il charge sa configuration depuis deux emplacements indépendants :

- `wing_config_v1` (localStorage) — le wing de l'utilisateur, persisté entre sessions
- `DEFAULT_WING_CONFIG` (embarqué dans le HTML) — le wing 4th VEAW, utilisé si aucune config n'est trouvée

Ces deux couches sont **totalement indépendantes du state du briefing** (`khr26_briefing_state_v2`). Changer de wing n'efface pas le briefing en cours, et réinitialiser le briefing ne touche pas à la config wing.

### Workflow pour un wing admin

1. Ouvrir `DCS_World_Briefing_Generator.html` dans Chrome.
2. Aller dans l'onglet **09 ░ WING**.
3. Renseigner les informations du wing : id, nom court, nom complet, titre de l'appli, logo (drag-drop ou bouton parcourir), tampon QG.
4. Ajouter les escadrons via le bouton **« + Ajouter un escadron »** : pour chaque escadron, saisir l'id, le nom, le callsign, les appareils disponibles, le logo.
5. Cliquer **« 📤 Exporter config »** → un fichier `wing_config_[id].json` est téléchargé.
6. Distribuer ce fichier JSON + le HTML aux pilotes du wing.

### Workflow pour un pilote (import)

1. Ouvrir le HTML, aller dans l'onglet **09 ░ WING**.
2. Cliquer **« 📥 Importer config »**, sélectionner le fichier JSON du wing admin.
3. L'application recharge avec le branding et les escadrons du wing chargé.
4. La configuration est mémorisée — elle se recharge automatiquement à chaque ouverture.

### Schéma JSON (`wing_config.json`)

```json
{
  "configSchemaVersion": 1,
  "wing": {
    "id": "4th-VEAW",
    "shortName": "4th VEAW",
    "fullName": "4th Virtual Expeditionary Air Wing",
    "appTitle": "GÉNÉRATEUR DE BRIEFING",
    "logo": "data:image/png;base64,...",
    "hqStamp": "HQ ░ 4th VEAW"
  },
  "squadrons": [
    {
      "id": "KHR-26",
      "name": "Kampfhubschrauberregiment 26",
      "nickname": "",
      "callsign": "FRANKEN",
      "aircraft": ["Mi-24P", "Mi-8"],
      "logo": "data:image/png;base64,..."
    }
  ]
}
```

**Détail des champs :**

| Champ | Type | Description |
|---|---|---|
| `configSchemaVersion` | `number` | Toujours `1` — pour compatibilité future |
| `wing.id` | `string` | Identifiant technique (ex. `"my-wing"`). Pas d'espaces, pas de `/`. |
| `wing.shortName` | `string` | Affiché dans la toolbar (ex. `"4th VEAW"`) |
| `wing.fullName` | `string` | Nom complet (ex. `"4th Virtual Expeditionary Air Wing"`) |
| `wing.appTitle` | `string` | Sous-titre toolbar (ex. `"GÉNÉRATEUR DE BRIEFING"`) |
| `wing.logo` | `string` | Data URL `data:image/png;base64,...` |
| `wing.hqStamp` | `string` | Texte du tampon couverture (ex. `"HQ ░ 4th VEAW"`) |
| `squadrons[].id` | `string` | Identifiant unique escadron (ex. `"KHR-26"`). Référencé dans le state du briefing. |
| `squadrons[].name` | `string` | Nom complet escadron |
| `squadrons[].nickname` | `string` | Surnom (optionnel, peut être vide) |
| `squadrons[].callsign` | `string` | Callsign radio |
| `squadrons[].aircraft` | `string[]` | Liste des appareils disponibles |
| `squadrons[].logo` | `string` | Data URL `data:image/png;base64,...` |

### Limites et bonnes pratiques

**Taille des logos :** les logos sont compressés automatiquement en **PNG** (256×256 px max) lors du drag-drop ou de la sélection via « Parcourir ». Le format PNG est choisi délibérément pour préserver la transparence, importante pour l'intégration des logos sur le fond kraft des pages PDF. Un logo source de 200×200 px est idéal.

**Format de l'id escadron :** utiliser des caractères alphanumériques, tirets et underscores uniquement (ex. `"KHR-26"`, `"541-TFS"`, `"mon_sqn"`). L'id est utilisé comme clé dans le state du briefing — le modifier ultérieurement rendra les missions existantes orphelines.

**Taille du fichier JSON :** avec 6 escadrons et leurs logos PNG, le fichier JSON fait environ 400–500 Ko. C'est normal — les images sont incluses en base64 inline.

**Import destructif :** l'import d'un JSON de wing écrase intégralement la configuration courante. Il n'y a pas de merge. Exporter d'abord si vous souhaitez conserver l'existant.

**Briefings orphelins :** si un briefing référence l'id `KHR-26` et que le wing chargé ne contient pas cet escadron, les missions concernées s'affichent grisées sans crash. Aucune perte de données.

**Compatibilité amont :** les briefings exportés avec l'ancienne version (KHR-26 Briefing Generator, avant le refactoring multi-wings) s'importent sans modification — la clé localStorage `khr26_briefing_state_v2` n'a pas changé.

### Fichier d'exemple

Le fichier `wing_config_4th_veaw.json` fourni avec le projet est la configuration complète du 4th VEAW (wing par défaut). Il peut servir de point de départ pour créer la configuration d'un autre wing.

---

## 14. Thèmes graphiques

L'application propose 4 thèmes graphiques sélectionnables via la toolbar :

- **Cold War OTAN** (défaut) — papier kraft, kaki, encre rouge OTAN
- **Cold War Soviétique** — papier ocre, vert armée russe, étoile rouge bordeaux
- **OTAN moderne** — papier blanc cassé, gris-bleu militaire, sceaux digitaux noirs
- **Bloc Est moderne** — papier grisé, vert digital, accents bleu-noir

Le thème choisi est persisté en localStorage (clé `theme_v1`) et indépendant
du wing et des briefings. Il s'applique au mode édition, au mode aperçu et
à l'export PDF.

### Implémentation technique

Bascule au runtime via `<body data-theme="...">` (4 valeurs : `cw-nato`,
`cw-soviet`, `modern-nato`, `modern-east`). Chaque thème redéfinit 16 variables
CSS (`--paper`, `--khaki`, `--olive`, `--red-stamp`, `--page-bg`, `--kraft-bg`,
etc.). Les variables sémantiques `--amber`, `--amber-dark`, `--green-radar`
restent constantes (accent UI invariant).

Les textures kraft de fond sont 4 SVG modulés en build-time depuis le SVG
d'origine (`KRAFT_SVG`) via 2 substitutions de couleurs (`#d6c7a3` fond et
`#ccbe99` grain). Le coût total est de ~140 KB pour les 4 versions.

Roboto Mono Regular (subset latin, 12.4 KB WOFF2) est embarqué et activé
sur les 2 thèmes modernes via override de `--f-typewriter`.

Les sceaux d'angle sont thématisés en CSS pur (overrides sur
`body[data-theme="..."] .stamp-classif`), sans modification du DOM ni du JS.
Le texte de classification reste dynamique (`state.meta.classification`).