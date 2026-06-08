"""
Pievieno Jaunbūves L1/L2/L3 konfigurētāju un Legalizācijas vadni.
"""
import re, subprocess, tempfile, os

path = r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\index.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# ── CSS ──────────────────────────────────────────────────────
PKG_CSS = """
/* ── PACKAGE CONFIGURATOR ──────────────────────────────────── */
.pkg-wizard { display:none; margin-top:16px }
.pkg-wizard.visible { display:block }

/* Level selector pills */
.pkg-pills { display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px }
.pkg-pill {
  border:2px solid var(--border);border-radius:10px;padding:11px;
  cursor:pointer;transition:all .15s;text-align:center;background:var(--card);
}
.pkg-pill:hover { border-color:var(--gold) }
.pkg-pill.active { border-color:var(--navy);background:var(--navy) }
.pkg-pill.best { border-color:var(--gold) }
.pkg-pill.best.active { background:var(--navy) }
.pkg-pill .pp-code { font-size:.78rem;font-weight:800;letter-spacing:1px }
.pkg-pill.active .pp-code { color:var(--gold) }
.pkg-pill:not(.active) .pp-code { color:var(--navy) }
.pkg-pill .pp-name { font-size:.72rem;color:var(--muted);margin-top:2px }
.pkg-pill.active .pp-name { color:rgba(255,255,255,.5) }
.pkg-pill .pp-price { font-size:.88rem;font-weight:700;margin-top:5px }
.pkg-pill.active .pp-price { color:var(--gold) }
.pkg-pill:not(.active) .pp-price { color:var(--navy) }
.pkg-best-tag {
  font-size:.55rem;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;
  background:var(--gold);color:var(--navy);padding:1px 7px;border-radius:8px;
  display:block;margin-bottom:5px;
}
.pkg-pill:not(.best) .pkg-best-tag { display:none }

/* Item list */
.pkg-items { display:flex;flex-direction:column;gap:6px;margin-bottom:14px }
.pkg-item {
  display:grid;grid-template-columns:18px 1fr;gap:9px;
  padding:9px 11px;border-radius:8px;border:1.5px solid var(--border);
  background:var(--card);transition:border-color .15s;align-items:flex-start;
  cursor:pointer;
}
.pkg-item:hover:not(.obligats) { border-color:var(--gold) }
.pkg-item.obligats { border-color:#dbeafe;background:#f0f6ff;cursor:default }
.pkg-item.unchecked { border-color:#fca5a5;background:#fff7f7 }
.pkg-item.new-in-level { border-color:#bbf7d0;background:#f0fdf4 }
.pkg-item input[type=checkbox] { width:16px;height:16px;accent-color:var(--navy);cursor:pointer;margin-top:2px }
.pkg-item.obligats input { accent-color:#3b82f6;cursor:not-allowed }
.pi-name { font-size:.82rem;font-weight:600;color:var(--navy);line-height:1.35 }
.pi-tag { display:inline-block;font-size:.58rem;font-weight:700;padding:1px 6px;border-radius:4px;margin-left:4px;vertical-align:middle }
.pi-tag.obligat { background:#dbeafe;color:#1d4ed8 }
.pi-tag.new { background:#dcfce7;color:#166534 }
.pi-warn { font-size:.72rem;color:#991b1b;margin-top:4px;display:none;padding:4px 7px;background:#fff7f7;border-radius:4px }
.pkg-item.unchecked .pi-warn { display:block }
.pi-note { font-size:.7rem;color:#166534;margin-top:3px }
.pkg-item.obligats .pi-note { display:block }
.pkg-item:not(.obligats) .pi-note { display:none }

/* Summary */
.pkg-summary {
  background:var(--navy);border-radius:10px;padding:14px 16px;
}
.pkg-sum-top { display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px }
.pkg-sum-label { font-size:.65rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.4) }
.pkg-sum-price { font-size:1.6rem;font-weight:800;color:var(--gold) }
.pkg-sum-int { font-size:.72rem;color:rgba(255,255,255,.3);margin-top:2px }
.pkg-sum-note { font-size:.7rem;color:rgba(255,255,255,.25);margin-top:4px }
.pkg-warn-count { display:inline-flex;align-items:center;gap:4px;background:rgba(220,38,38,.15);border:1px solid rgba(220,38,38,.3);border-radius:8px;padding:4px 10px;font-size:.72rem;color:#fca5a5;margin-top:8px }
.pkg-warn-count.hidden { display:none }
.pkg-offer-btn {
  width:100%;margin-top:10px;padding:11px;
  background:var(--gold);color:var(--navy);
  border:none;border-radius:8px;font-weight:800;font-size:.88rem;
  letter-spacing:.5px;cursor:pointer;transition:opacity .15s;
}
.pkg-offer-btn:hover { opacity:.88 }

/* Section divider */
.pkg-section-title {
  font-size:.65rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  color:var(--muted);margin:12px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--border);
}

/* Legal wizard */
.legal-wizard { display:none;margin-top:16px }
.legal-wizard.visible { display:block }
.legal-pkg-card {
  border:2px solid var(--border);border-radius:10px;padding:14px;margin-bottom:10px;
  cursor:pointer;transition:all .15s;
}
.legal-pkg-card:hover { border-color:var(--gold) }
.legal-pkg-card.selected { border-color:var(--navy);background:#f0f4ff }
.legal-pkg-card.best { border-color:var(--gold) }
.legal-pkg-card.selected.best { background:#fffbf0;border-color:var(--gold) }
.lpk-header { display:flex;align-items:center;gap:10px;margin-bottom:8px }
.lpk-radio { width:18px;height:18px;accent-color:var(--navy);flex-shrink:0 }
.lpk-name { font-size:.92rem;font-weight:700;color:var(--navy) }
.lpk-price { margin-left:auto;font-size:1rem;font-weight:800;color:var(--navy) }
.legal-pkg-card.selected .lpk-price { color:var(--gold) }
.lpk-items { list-style:none;margin-top:6px }
.lpk-items li { font-size:.76rem;padding:2px 0;display:flex;gap:6px;color:var(--text) }
.lpk-items li::before { content:"✓";color:var(--green);flex-shrink:0;font-weight:700 }
.lpk-risk { background:#fef2f2;border-left:2px solid var(--red);padding:6px 9px;border-radius:0 5px 5px 0;font-size:.73rem;color:#991b1b;margin-top:6px }
.lpk-adv { background:#ecfdf5;border-left:2px solid var(--green);padding:6px 9px;border-radius:0 5px 5px 0;font-size:.73rem;color:#065f46;margin-top:6px }
"""

html = html.replace("</style>\n</head>", PKG_CSS + "</style>\n</head>", 1)
print("✓ Package configurator CSS added")

# ── HTML — insert Jaunbūve wizard + Legal wizard in the AR full-row area ──
# Find where the jaunbuve-paketes card starts and replace it with our new wizard
OLD_JB_CARD_START = '<div id="jaunbuve-paketes" class="card">'
JAUNBUVE_WIZARD_HTML = """
<!-- ══ JAUNBŪVES PAKETES + KONFIGURĒTĀJS ══ -->
<div id="jaunbuve-paketes" class="card">
  <div class="card-title">🏗 Jaunbūve — Izvēlies paketi un konfigurē saturu</div>
  <div style="font-size:.78rem;color:var(--muted);margin-bottom:14px">
    Platība: <strong id="pb-area-2">—</strong> m² · Cenas klientam (ar 20% rezervi) · Atzīme satur / noņem elements no paketes
  </div>

  <!-- LEVEL PILLS -->
  <div class="pkg-pills">
    <div class="pkg-pill" id="pkg-pill-L1" onclick="selectPkg('L1')">
      <div class="pp-code">L1</div>
      <div class="pp-name">Standarta</div>
      <div class="pp-price" id="pkg-price-L1">—</div>
    </div>
    <div class="pkg-pill best" id="pkg-pill-L2" onclick="selectPkg('L2')">
      <span class="pkg-best-tag">IETEICAMS</span>
      <div class="pp-code">L2 ⭐</div>
      <div class="pp-name">Uzlabots</div>
      <div class="pp-price" id="pkg-price-L2">—</div>
    </div>
    <div class="pkg-pill" id="pkg-pill-L3" onclick="selectPkg('L3')">
      <div class="pp-code">L3</div>
      <div class="pp-name">Premium</div>
      <div class="pp-price" id="pkg-price-L3">—</div>
    </div>
  </div>

  <!-- ITEMS LIST -->
  <div id="pkg-items-list" class="pkg-items"></div>

  <!-- SUMMARY -->
  <div class="pkg-summary">
    <div class="pkg-sum-top">
      <div>
        <div class="pkg-sum-label">Klientam piedāvāt</div>
        <div class="pkg-sum-price" id="pkg-final-price">—</div>
        <div class="pkg-sum-int">Iekšējā: <span id="pkg-final-int">—</span></div>
      </div>
      <div style="text-align:right">
        <div class="pkg-sum-label" id="pkg-selected-name">—</div>
        <div class="pkg-sum-note">bez PVN · 20% rezerve tirgošanai</div>
      </div>
    </div>
    <div class="pkg-warn-count hidden" id="pkg-warn-count">
      ⚠ <span id="pkg-warn-num">0</span> pozīcija izslēgta — pārbaudi riskus!
    </div>
    <button class="pkg-offer-btn" onclick="copyPkgToOffer()">
      ✓ Iekļaut piedāvājumā — <span id="pkg-offer-text">—</span>
    </button>
  </div>
</div>

<!-- ══ LEGALIZĀCIJAS PAKETES (esošais bloks saglabāts) ══ -->
"""

if OLD_JB_CARD_START in html:
    # Find the end of jaunbuve-paketes card
    start_idx = html.find(OLD_JB_CARD_START)
    # Find the matching closing of this card - look for the next top-level card div
    # The jaunbuve-paketes card ends before the legalizacija-paketes card
    end_marker = '\n\n  <div id="legalizacija-paketes"'
    end_idx = html.find(end_marker, start_idx)
    if end_idx != -1:
        html = html[:start_idx] + JAUNBUVE_WIZARD_HTML + html[end_idx:]
        print("✓ Jaunbūve wizard HTML inserted")
    else:
        print("WARNING: Could not find end of jaunbuve-paketes card")
else:
    print("WARNING: jaunbuve-paketes not found")

# ── JavaScript ────────────────────────────────────────────────
PKG_JS = r"""
// ══════════════════════════════════════════════════════════════
// JAUNBŪVES PAKETES KONFIGURĒTĀJS
// ══════════════════════════════════════════════════════════════

const PAKETES_BR = [
    {max:60,  L1:3100, L2:3900,  L3:6100},
    {max:100, L1:3550, L2:4450,  L3:6950},
    {max:160, L1:4000, L2:5000,  L3:7850},
    {max:220, L1:4450, L2:5600,  L3:8700},
    {max:300, L1:4900, L2:6150,  L3:9550},
    {max:400, L1:5750, L2:7250,  L3:11300},
    {max:Infinity, L1:8900, L2:11150, L3:17400},
];

// All possible items across all levels
// level: which level first includes this item
// obligats: cannot be deselected
// warning: shown when unchecked
// note: shown when obligats=true (why it's mandatory)
const PKG_ITEMS_ALL = [
    { id:'skice_2d',     name:'1× 2D skice (pamata plāns)', level:'L1', obligats:false,
      warning:'Bez 2D skices klients nevar vizuāli saprast plānojumu pirms apstiprināšanas. Risks: vēlāk dārgas izmaiņas.' },
    { id:'viz_3d_l1',    name:'1× 3D vizualizācija', level:'L1', obligats:false,
      warning:'Bez 3D klients neredz kā māja izskatīsies. Var rasties pārpratumi → dārgas projekta izmaiņas.' },
    { id:'viz_3d_l2',    name:'2× 3D varianti (nevis 1×)', level:'L2', obligats:false,
      warning:'Tikai 1× 3D variants. 2 varianti ļauj klientam izvēlēties stilistiku pirms projekta sākšanas.' },
    { id:'viz_3d_l3',    name:'3× 3D varianti (nevis 2×)', level:'L3', obligats:false,
      warning:'Tikai 2× 3D varianti. Maksimāla stila izvēle iekļauta L3.' },
    { id:'vr_l1',        name:'VR tūre (360° apskate telefonā)', level:'L1', obligats:false,
      warning:'Bez VR tūres klients mazāk iesaistās projektā. Pārpratumu risks palielinās.' },
    { id:'vr_l3',        name:'2× VR tūres (interjers + eksterjers)', level:'L3', obligats:false,
      warning:'Tikai 1× VR tūre. L3 ietver arī interjera VR tūri.' },
    { id:'ar_project',   name:'Arhitektūras projekts (plāni, fasādes)', level:'L1', obligats:true,
      note:'OBLIGĀTS — bez AR projekta nav iespējams iesniegt BIS. Pamats visam.' },
    { id:'ar_griezums_l1', name:'1 griezums', level:'L1', obligats:true,
      note:'Obligāts minimums BIS iesniegumam.' },
    { id:'ar_griezumi_l2', name:'4 griezumi + 4 mezgli (nevis 1+0)', level:'L2', obligats:false,
      warning:'Tikai 1 griezums un bez mezgliem. Büvniekam var rasties jautājumi → papildu izmaksas büvlaikā.' },
    { id:'ar_griezumi_l3', name:'7 griezumi, kāpnes, 8 mezgli (nevis 4+4)', level:'L3', obligats:false,
      warning:'4 griezumi un 4 mezgli. L3 ietver kāpnes un pilnīgu mezglu dokumentāciju.' },
    { id:'galv_plans',   name:'Galvenais plāns + situācijas apliecinājums', level:'L1', obligats:true,
      note:'OBLIGĀTS BIS iesniegumam — ēkas novietojums zemes gabalā.' },
    { id:'gp_vertik',    name:'GP ar vertikālo plānojumu un žogu', level:'L2', obligats:false,
      warning:'Bez vertikālā plānojuma grūtāk kontrolēt apbüves niveles un atkāpes.' },
    { id:'buvapjomi',    name:'Büvapjomu saraksts (precīzs materiālu daudzums)', level:'L3', obligats:false,
      warning:'L3 ietver büvapjomu sarakstu. Var iegūt precīzu büvniecības tāmi no büvnieka.' },
    { id:'izmaksu_l2',   name:'Orientējoša celtniecības izmaksu prognoze', level:'L2', obligats:false,
      warning:'Bez izmaksu prognozes klients var nebūt sagatavots büvniecības budžetam.' },
    { id:'izmaksu_l3',   name:'Izmaksu prognoze ar detalizētiem papildinājumiem', level:'L3', obligats:false,
      warning:'L3 ietver detalizētāku izmaksu prognozi.' },
    { id:'bk_2d',        name:'BK 2D (pamata konstruktīvie aprēķini)', level:'L1', obligats:false,
      warning:'BEZ BK: büvnieks bez konstruktīvajiem aprēķiniem! Büvniecības kļūdu un drošības risks.' },
    { id:'bk_l2',        name:'BK 3D LOD200 (precīzāks par BK 2D)', level:'L2', obligats:false,
      warning:'BK 2D ir mazāk detalizēts. LOD200 ļauj büvniekam precīzāk plānot materiālus.' },
    { id:'bk_l3',        name:'BK 3D LOD300 (ražošanas precizitāte)', level:'L3', obligats:false,
      warning:'LOD200 nav pietiekami precīzs CLT/koka karkasa ražošanai. LOD300 = kļūdu risks minimāls.' },
    { id:'eps_base',     name:'Energosertifikāts EPS (bāzes novērtējums)', level:'L1', obligats:false,
      warning:'BEZ EPS: NEVAR saņemt NOD (nodošanu ekspluatācijā)! Māja paliks juridiski "nepabeigta"!' },
    { id:'eps_nde',      name:'Gandrīz nulles enerģijas sertifikāts (augstākā klase)', level:'L3', obligats:false,
      warning:'Bāzes EPS. L3 ietver augstākās klases sertifikātu — zemāki komunālie, augstāka mājas vērtība.' },
    { id:'kor_l1',       name:'1 korekciju kārta', level:'L1', obligats:false,
      warning:'1 korekcija. Papildu izmaiņas pec tās maksā atsevišķi.' },
    { id:'kor_l2',       name:'2 korekciju kārtas (nevis 1×)', level:'L2', obligats:false,
      warning:'Tikai 1 korekcija. 2. korekciju kārta palīdz precizēt projektu bez papildu izmaksām.' },
    { id:'kor_l3',       name:'3 korekciju kārtas (nevis 2×)', level:'L3', obligats:false,
      warning:'2 korekciju kārtas. Maksimāla elastība L3.' },
];

// Which items appear in each level
const LEVEL_ITEMS = {
    L1: ['skice_2d','viz_3d_l1','vr_l1','ar_project','ar_griezums_l1','galv_plans','bk_2d','eps_base','kor_l1'],
    L2: ['skice_2d','viz_3d_l1','viz_3d_l2','vr_l1','ar_project','ar_griezumi_l2','galv_plans','gp_vertik','izmaksu_l2','bk_l2','eps_base','kor_l2'],
    L3: ['skice_2d','viz_3d_l1','viz_3d_l2','viz_3d_l3','vr_l1','vr_l3','ar_project','ar_griezumi_l3','galv_plans','gp_vertik','buvapjomi','izmaksu_l3','bk_l3','eps_nde','kor_l3'],
};

let currentPkg = 'L2';
let pkgChecked = {};  // {itemId: true/false}
let currentPkgArea = 0;

function getPkgPrice(level, area) {
    const br = PAKETES_BR.find(b => area <= b.max) || PAKETES_BR[PAKETES_BR.length-1];
    return br[level];
}

function initPkgChecked(level) {
    pkgChecked = {};
    (LEVEL_ITEMS[level] || []).forEach(id => { pkgChecked[id] = true; });
}

function selectPkg(level) {
    currentPkg = level;
    initPkgChecked(level);
    ['L1','L2','L3'].forEach(l => {
        const p = document.getElementById('pkg-pill-'+l);
        if (p) p.classList.toggle('active', l === level);
    });
    renderPkgItems();
    updatePkgSummary();
}

function renderPkgItems() {
    const container = document.getElementById('pkg-items-list');
    if (!container) return;
    const levelItems = LEVEL_ITEMS[currentPkg] || [];
    const prevLevel = currentPkg === 'L2' ? 'L1' : currentPkg === 'L3' ? 'L2' : null;

    let html = '';
    let lastSection = '';

    levelItems.forEach(id => {
        const item = PKG_ITEMS_ALL.find(x => x.id === id);
        if (!item) return;
        const isNew = prevLevel && !LEVEL_ITEMS[prevLevel]?.includes(id);
        const isChecked = pkgChecked[id] !== false;

        // Section header
        let section = '';
        if (['skice_2d','viz_3d_l1','viz_3d_l2','viz_3d_l3','vr_l1','vr_l3'].includes(id)) section = '🎨 Vizualizācija un skices';
        else if (['ar_project','ar_griezums_l1','ar_griezumi_l2','ar_griezumi_l3','galv_plans','gp_vertik','buvapjomi'].includes(id)) section = '📐 Arhitektūras projekts (AR)';
        else if (['izmaksu_l2','izmaksu_l3'].includes(id)) section = '💰 Izmaksu plānošana';
        else if (['bk_2d','bk_l2','bk_l3'].includes(id)) section = '🏗 Büvkonstrukcijas (BK)';
        else if (['eps_base','eps_nde'].includes(id)) section = '⚡ Energosertifikāts (EPS)';
        else if (['kor_l1','kor_l2','kor_l3'].includes(id)) section = '✏️ Korekciju kārtas';

        if (section && section !== lastSection) {
            html += `<div class="pkg-section-title">${section}</div>`;
            lastSection = section;
        }

        const classes = ['pkg-item',
            item.obligats ? 'obligats' : '',
            !isChecked ? 'unchecked' : '',
            isNew ? 'new-in-level' : ''
        ].filter(Boolean).join(' ');

        const newTag = isNew ? '<span class="pi-tag new">JAUNS</span>' : '';
        const obligatTag = item.obligats ? '<span class="pi-tag obligat">OBLIGĀTS</span>' : '';

        html += `<div class="${classes}" onclick="${item.obligats ? '' : `togglePkgItem('${id}')`}">
            <input type="checkbox" ${isChecked?'checked':''} ${item.obligats?'disabled':''} onchange="togglePkgItem('${id}')">
            <div>
                <div class="pi-name">${item.name}${obligatTag}${newTag}</div>
                ${item.obligats ? `<div class="pi-note">📋 ${item.note}</div>` : ''}
                <div class="pi-warn">⚠ ${item.warning || ''}</div>
            </div>
        </div>`;
    });

    container.innerHTML = html;
}

function togglePkgItem(id) {
    const item = PKG_ITEMS_ALL.find(x => x.id === id);
    if (!item || item.obligats) return;
    pkgChecked[id] = !pkgChecked[id];
    renderPkgItems();
    updatePkgSummary();
}

function updatePkgSummary() {
    const area = currentPkgArea;
    if (!area) return;
    const baseInt = getPkgPrice(currentPkg, area);
    const baseCli = Math.round(baseInt * 1.20 / 50) * 50;

    // Count unchecked (non-obligats)
    const levelItems = LEVEL_ITEMS[currentPkg] || [];
    const unchecked = levelItems.filter(id => {
        const item = PKG_ITEMS_ALL.find(x => x.id === id);
        return item && !item.obligats && pkgChecked[id] === false;
    }).length;

    const nameMap = {L1:'L1 Standarta', L2:'L2 Uzlabots', L3:'L3 Premium'};

    const setPEl = (id, val) => { const el=document.getElementById(id); if(el) el.textContent=val; };
    setPEl('pkg-final-price', baseCli.toLocaleString('lv-LV') + ' EUR');
    setPEl('pkg-final-int', baseInt.toLocaleString('lv-LV') + ' EUR');
    setPEl('pkg-selected-name', nameMap[currentPkg]);
    setPEl('pkg-offer-text', baseCli.toLocaleString('lv-LV') + ' EUR');

    const warnEl = document.getElementById('pkg-warn-count');
    const warnNum = document.getElementById('pkg-warn-num');
    if (warnEl) warnEl.classList.toggle('hidden', unchecked === 0);
    if (warnNum) warnNum.textContent = unchecked;
}

function initPkgWizard(area) {
    currentPkgArea = area;
    // Update prices in pills
    ['L1','L2','L3'].forEach(l => {
        const el = document.getElementById('pkg-price-'+l);
        if (el) {
            const int = getPkgPrice(l, area);
            const cli = Math.round(int * 1.20 / 50) * 50;
            el.textContent = cli.toLocaleString('lv-LV') + ' EUR';
        }
    });
    // Update area display
    const areaEl = document.getElementById('pb-area-2');
    if (areaEl) areaEl.textContent = area;

    // Init with current level
    if (!pkgChecked || Object.keys(pkgChecked).length === 0) {
        initPkgChecked(currentPkg);
    }
    // Activate current pill
    selectPkg(currentPkg);
}

function copyPkgToOffer() {
    // Update the main price display to match selected package
    const area = currentPkgArea;
    const baseInt = getPkgPrice(currentPkg, area);
    const baseCli = Math.round(baseInt * 1.20 / 50) * 50;
    const priceEl = document.getElementById('ar-p-client');
    const intEl = document.getElementById('ar-p-int');
    if (priceEl) priceEl.textContent = eur(baseCli);
    if (intEl) intEl.textContent = eur(baseInt);
    // Flash confirmation
    const btn = event.currentTarget;
    const orig = btn.textContent;
    btn.textContent = '✓ Pievienots piedāvājumam!';
    btn.style.background = 'var(--green)';
    setTimeout(() => { btn.textContent = orig; btn.style.background = ''; }, 2000);
}

// Hook into renderARPanels to init wizard
const _origRenderARPanels = renderARPanels;
function renderARPanels(type, area, svcCoef) {
    _origRenderARPanels(type, area, svcCoef);
    if (type === 'jaunbuve' && area > 0) {
        initPkgWizard(area);
    }
}
"""

# Insert before the 3D init
marker = "// ══════════════════════════════════════════════════════════════\n// THREE.JS"
html = html.replace(marker, PKG_JS + "\n" + marker)
print("✓ Package configurator JS added")

# ── Syntax check ──────────────────────────────────────────────
with open(path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"File: {len(html)} chars")

scriptStart = html.find("<script>") + 8
scriptEnd = html.rfind("</script>")
js = html[scriptStart:scriptEnd]
tmp = os.path.join(tempfile.gettempdir(), "volko_pkg.js")
with open(tmp, "w", encoding="utf-8") as f:
    f.write(js)
result = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
if result.returncode == 0:
    print("✓ JS syntax OK")
else:
    print("✗ JS ERROR:", result.stderr[:500])
