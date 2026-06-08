"""
Pievieno pilnu "Projekta pase" sekciju pēc cenas aprēķina.
Rāda: atļaujas tips, BIS dokumenti, EBN punkti, termiņi, riski.
"""
import re

path = r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\index.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# ── 1. ADD CSS FOR PASSPORT ────────────────────────────────────
PASSPORT_CSS = """
/* ── PROJEKTA PASE ─────────────────────────────────────────── */
.passport { display:none }
.passport.visible { display:block }
.pp-section { margin-bottom:14px }
.pp-label { font-size:.63rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:8px;display:flex;align-items:center;gap:6px }
.pp-badge { display:inline-flex;align-items:center;gap:6px;background:var(--navy);color:var(--gold);font-size:.78rem;font-weight:700;padding:6px 12px;border-radius:8px;margin-bottom:10px }
.pp-permit { background:#fffbf0;border:1.5px solid var(--gold);border-radius:8px;padding:10px 13px;margin-bottom:10px }
.pp-permit-name { font-size:.9rem;font-weight:800;color:var(--navy) }
.pp-permit-law { font-size:.7rem;color:var(--muted);margin-top:2px }
.pp-permit-desc { font-size:.75rem;color:var(--text);margin-top:6px;line-height:1.5 }
.doc-cols { display:grid;grid-template-columns:1fr 1fr;gap:12px }
@media(max-width:500px){.doc-cols{grid-template-columns:1fr}}
.doc-col-title { font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;padding:5px 9px;border-radius:6px }
.doc-col-title.client { background:#fff4e0;color:#92400e }
.doc-col-title.volko { background:#e0f0ff;color:#1e3a5f }
.doc-item { display:flex;gap:7px;align-items:flex-start;padding:5px 0;border-bottom:1px solid var(--border);font-size:.76rem;line-height:1.4 }
.doc-item:last-child { border-bottom:none }
.doc-icon { flex-shrink:0;width:16px;text-align:center;font-size:.8rem }
.doc-name { color:var(--text) }
.doc-note { font-size:.68rem;color:var(--muted);margin-top:1px }
.doc-req { display:inline-block;font-size:.6rem;font-weight:700;padding:1px 5px;border-radius:3px;margin-left:4px;vertical-align:middle }
.doc-req.must { background:#fee2e2;color:var(--red) }
.doc-req.maybe { background:#fef9c3;color:#713f12 }
.timeline-steps { display:flex;flex-direction:column;gap:0 }
.tl-step { display:grid;grid-template-columns:28px 1fr;gap:10px;padding:8px 0 }
.tl-step:not(:last-child) { border-bottom:1px dashed var(--border) }
.tl-num { width:24px;height:24px;background:var(--gold);color:var(--navy);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:800;flex-shrink:0;margin-top:2px }
.tl-content {}
.tl-title { font-size:.84rem;font-weight:700;color:var(--navy) }
.tl-price-tag { display:inline-block;background:#fffbf0;border:1px solid #fde68a;border-radius:4px;font-size:.64rem;font-weight:700;color:#92400e;padding:1px 6px;margin-left:5px }
.tl-who { font-size:.7rem;color:var(--muted);margin-top:1px }
.tl-dur { display:inline-flex;align-items:center;gap:3px;font-size:.68rem;background:#f0f6ff;color:#1e3a5f;border-radius:4px;padding:1px 6px;margin-top:3px }
.tl-why { font-size:.72rem;color:#5f4300;background:#fffbf0;border-left:2px solid var(--gold);padding:4px 8px;border-radius:0 5px 5px 0;margin-top:4px;line-height:1.4 }
.risk-row { display:flex;gap:8px;padding:7px;border-radius:7px;margin-bottom:5px;font-size:.76rem;line-height:1.45 }
.risk-row.high { background:#fef2f2;border-left:3px solid var(--red) }
.risk-row.med { background:#fffbf0;border-left:3px solid var(--gold) }
.risk-row.low { background:#f0fdf4;border-left:3px solid var(--green) }
.risk-icon { font-size:.9rem;flex-shrink:0;margin-top:1px }
.cost-table { width:100%;border-collapse:collapse;font-size:.8rem }
.cost-table tr { border-bottom:1px solid var(--border) }
.cost-table tr:last-child { border-bottom:none }
.cost-table td { padding:6px 4px }
.cost-table .ct-name { color:var(--text) }
.cost-table .ct-price { text-align:right;font-weight:600;color:var(--navy);white-space:nowrap }
.cost-table .ct-total { font-weight:800;font-size:.88rem;color:var(--navy) }
.cost-table .ct-total-price { font-weight:800;font-size:.88rem;color:var(--gold);text-align:right }
.cost-table tr.sep td { padding-top:8px;border-top:2px solid var(--border) }
"""

# Insert CSS before closing </style>
html = html.replace('</style>\n</head>', PASSPORT_CSS + '\n</style>\n</head>', 1)

# ── 2. ADD PASSPORT HTML PLACEHOLDER in AR results ────────────
# Insert after the ar-p-fixed div and before closing </div></div>
PASSPORT_HTML = """
<!-- PROJEKTA PASE -->
<div id="ar-passport" class="passport card" style="margin-top:0;padding:0;overflow:hidden">
  <div style="background:linear-gradient(135deg,var(--navy),#1e3a5f);padding:13px 18px;display:flex;align-items:center;justify-content:space-between">
    <div style="color:var(--gold);font-size:.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase">📋 Projekta pase</div>
    <div id="pp-permit-badge" style="background:rgba(200,168,75,.15);border:1px solid rgba(200,168,75,.4);border-radius:8px;padding:3px 10px;font-size:.7rem;color:var(--gold);font-weight:700"></div>
  </div>
  <div style="padding:16px 18px">

    <!-- Atļaujas veids -->
    <div class="pp-section" id="pp-permit-section">
      <div class="pp-label">⚖️ Atļaujas veids</div>
      <div class="pp-permit" id="pp-permit-box"></div>
    </div>

    <!-- Dokumentu saraksts -->
    <div class="pp-section" id="pp-docs-section">
      <div class="pp-label">📁 Dokumentu pakotne BIS iesniegšanai</div>
      <div class="doc-cols" id="pp-doc-cols"></div>
    </div>

    <!-- Soli pa solim -->
    <div class="pp-section" id="pp-steps-section">
      <div class="pp-label">🗓️ Process soli pa solim</div>
      <div class="timeline-steps" id="pp-timeline"></div>
    </div>

    <!-- Izmaksu kopsavilkums -->
    <div class="pp-section" id="pp-cost-section">
      <div class="pp-label">💰 Izmaksu kopsavilkums</div>
      <table class="cost-table" id="pp-cost-table"></table>
    </div>

    <!-- Riski -->
    <div class="pp-section" id="pp-risks-section">
      <div class="pp-label">⚠️ Riski un piezīmes</div>
      <div id="pp-risks"></div>
    </div>

  </div>
</div>
"""

# Find the right place to insert - after ar-p-fixed closing div
target = '</div>\n</div>\n</div>\n</div>\n<div style="margin-top:16px">'
replacement = '</div>\n</div>\n' + PASSPORT_HTML + '\n</div>\n</div>\n<div style="margin-top:16px">'
if target in html:
    html = html.replace(target, replacement, 1)
    print("✓ Passport HTML inserted")
else:
    # Try alternative
    target2 = '<div id="ar-fp-note" id="ar-fp-note">—</div>\n</div>\n</div>\n</div>\n</div>'
    print(f"Target not found, searching...")
    # Just append near ar-p-fixed
    idx = html.find('</div>\n</div>\n</div>\n</div>\n<div style="margin-top:16px">')
    print(f"Alternative idx: {idx}")

# ── 3. ADD PASSPORT JAVASCRIPT ────────────────────────────────
PASSPORT_JS = r"""
// ══════════════════════════════════════════════════════════════
// PROJEKTA PASE — pilna info pēc izvēles
// ══════════════════════════════════════════════════════════════

const PASSPORT_DATA = {
  // ── JAUNBŪVE ────────────────────────────────────────────────
  jaunbuve: {
    permit: (area, grp) => area < 200 ? {
      name: 'Paskaidrojuma raksts',
      law: 'EBN 7.2 (11. punkts) — MK not. Nr.529',
      desc: 'Jaunbūvei līdz 200m² nepieciešams paskaidrojuma raksts. Pašvaldībai 30 darba dienas izskatīšanai. Termiņš 5 gadi (nav pagarināms).',
      bisType: 'Paskaidrojuma raksts'
    } : {
      name: 'Būvprojekts + Būvatļauja',
      law: 'EBN 71.punkts — MK not. Nr.529',
      desc: 'Jaunbūvei ≥200m² nepieciešams pilns būvprojekts un būvatļauja. Termiņš 5+8 gadi (var pagarināt).',
      bisType: 'Būvatļauja'
    },
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'lejuplādēt zemesgramata.lv', req:'must' },
      { icon:'📐', name:'Zemes robežu plāns', note:'no VZD vai topogrāfs', req:'must' },
      { icon:'🗺️', name:'Topogrāfiskais plāns', note:'aktuāls, ne vecāks par 3 gadiem', req:'must' },
      { icon:'📋', name:'Kadastrālās izpētes lieta', note:'kadastrs.lv', req:'must' },
      { icon:'🏛️', name:'TIAN (pašvaldības apbūves noteikumi)', note:'pašvaldībā vai teritorijasplanojums.lv', req:'must' },
      { icon:'🤝', name:'Kaimiņu piekrišana', note:'ja ēka plānota tuvāk par 4m no robežas', req:'maybe' },
      { icon:'👥', name:'Kopīpašnieku piekrišana', note:'notariāli, ja ir vairāki īpašnieki', req:'maybe' },
    ],
    volkoDocs: [
      { icon:'📝', name:'Iesniegums BIS sistēmā', note:'Volko aizpilda elektroniskā veidlapā' },
      { icon:'📍', name:'Situācijas plāns', note:'ēkas novietojums zemes gabalā' },
      { icon:'📐', name:'Plāni (stāvi)', note:'katrs stāvs atsevišķi ar izmēriem' },
      { icon:'🏠', name:'Fasāžu rasējumi (4 fasādes)', note:'visi ārējie skati ar izmēriem' },
      { icon:'✂️', name:'Šķērsgriezums (vismaz 1)', note:'konstruktīvā šķēluma rasējums' },
      { icon:'📋', name:'Paskaidrojuma raksts', note:'tekstuāla daļa — projektētāja apraksts' },
      { icon:'⚡', name:'Energosertifikāts (EPS)', note:'nepieciešams jaunbūvēm ar apkuri' },
      { icon:'🏗️', name:'BK daļa (konstruktīvā)', note:'pamatu, sienu, jumta aprēķini' },
    ],
    steps: [
      { n:1, t:'ESI — Situācijas izpēte', who:'Volko', dur:'1–2 ned.', price:null, why:'Pārbauda TIAN — vai zonā drīkst celt, kādi ierobežojumi, sarkanās līnijas.' },
      { n:2, t:'Topogrāfiskā uzmērīšana', who:'Ārējs mērnieks (Volko koordinē)', dur:'1–2 ned.', price:'400€', why:'Precīzs zemes reljefa plāns — obligāts pamatu projektēšanai un situācijas plānam.' },
      { n:3, t:'Skiču projekts (koncepcija)', who:'Volko', dur:'2–4 ned.', price:'Iekļauts', why:'Klienta apstiprināšanai — plānojums, izskats. Tikai pēc apstiprināšanas sāk pilno projektu.' },
      { n:4, t:'Darba projekts (AR + BK)', who:'Volko', dur:'4–8 ned.', price:'Pēc paketes', why:'Pilna projekta dokumentācija — plāni, fasādes, griezumi, konstruktīvie risinājumi.' },
      { n:5, t:'BIS iesniegums', who:'Volko', dur:'1 diena', price:'Iekļauts', why:'Elektroniski iesniedz BIS — pievienoti visi dokumenti.' },
      { n:6, t:'Pašvaldības izskatīšana', who:'Pašvaldība', dur:'30 darba d.', price:'Valsts nodeva ~28€', why:'Pašvaldība pārbauda atbilstību TIAN un normatīviem. Var pieprasīt precizējumus.' },
      { n:7, t:'Büvatļaujas/Paskaidrojuma raksta saņemšana', who:'Klients + Volko', dur:'1–3 dienas', price:null, why:'Pēc akceptēšanas BIS — var uzsākt büvdarbus.' },
      { n:8, t:'NOD — Nodošana ekspluatācijā', who:'Volko', dur:'1–2 mēn.', price:'950€', why:'Pēc büvdarbu pabeigšanas — oficāli nodod ēku lietošanai. Bez NOD banka nedod hipotēku!' },
      { n:9, t:'Kadastrālā uzmērīšana + ZG', who:'VZD + notārs', dur:'3–5 ned.', price:'200–400€', why:'Ēka ierakstāma kadastrā un ZG — bez tā īpašums nav juridisks.' },
    ],
    risks: [
      { level:'high', icon:'🚫', text:'TIAN ierobežojumi — pirms sāc, pārbaudi vai zonā atļauts tavs projekts. Dažās zonās stingri augstuma, apbūves blīvuma ierobežojumi.' },
      { level:'med', icon:'⚠️', text:'Detālplānojums — dažas pašvaldības pieprasa DP pirms atļaujas. Process 1-3 gadi. Pārbaudīt pie pašvaldības.' },
      { level:'med', icon:'⚠️', text:'Inženiertīklu pieslēgumi — ūdens, kanalizācija, elektrība. Katram vajag atsevišķu saskaņojumu ar tīkla operatoru.' },
      { level:'low', icon:'✅', text:'Jaunbūvei nav patvaļīgas büvniecības riska — process ir tīrs, ja dokumenti kārtībā.' },
    ]
  },

  // ── LEGALIZĀCIJA PATVAĻĪGA (la) ─────────────────────────────
  la: {
    permit: (area, grp) => grp === 'I' ? {
      name: 'Apliecinājuma karte',
      law: 'EBN 7.3.4 un 7.3.5 — vienkāršota procedūra mazēkām',
      desc: 'I grupas mazēkai (≤25m², 1 stāvs) — vienkāršota legalizācija ar apliecinājuma karti. Nav TAA obligāts, nav pilna projekta.',
      bisType: 'Apliecinājuma karte'
    } : area <= 200 ? {
      name: 'Paskaidrojuma raksts (Legalizācijai)',
      law: 'EBN 7.2 (11.punkts) + BL 22.pants — patvaļīgā büvniecība',
      desc: 'Legalizācijai ≤200m² mājai nepieciešams paskaidrojuma raksts ar ESOŠĀ stāvokļa dokumentāciju. Riska faktors — pašvaldība var atteikt!',
      bisType: 'Paskaidrojuma raksts (legalizācijai)'
    } : {
      name: 'Büvatļauja (Legalizācijai)',
      law: 'EBN 71.punkts + BL 22.pants — patvaļīgā büvniecība',
      desc: '≥200m² legalizācijai nepieciešama büvatļauja. Sarežģīts un dārgs process. Riska faktors — pašvaldība var atteikt un pieprasīt nojaukšanu.',
      bisType: 'Büvatļauja (legalizācijai)'
    },
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība + ZG izraksts', note:'zemesgramata.lv — apliecina ka esi īpašnieks', req:'must' },
      { icon:'📋', name:'Kadastrālās izpētes lieta', note:'kadastrs.lv — ēkas dati kadastrā', req:'must' },
      { icon:'📐', name:'Robežu plāns (situācijas plāns)', note:'no VZD — parāda ēku novietojumu', req:'must' },
      { icon:'📁', name:'Esošie projekti / dokumenti (ja ir)', note:'jebkādi sākotnējie rasējumi, TN, citi dok.', req:'maybe' },
      { icon:'🤝', name:'Kaimiņu piekrišana', note:'ja ēka tuvāk par 4m no robežas', req:'maybe' },
      { icon:'👥', name:'Kopīpašnieku piekrišana', note:'notariāli, ja ir vairāki īpašnieki', req:'maybe' },
      { icon:'🌿', name:'TIAN no pašvaldības', note:'teritorijas izmantošanas un apbūves noteikumi', req:'must' },
    ],
    volkoDocs: [
      { icon:'⚖️', name:'ESI — Juridiskā esošās situācijas izpēte', note:'PIRMAIS solis — vai legalizācija iespējama?' },
      { icon:'🔍', name:'TAA — Tehniskā apsekošana + atzinums', note:'konstruktīvā drošība, defektu protokols' },
      { icon:'📏', name:'Uzmērīšana (esošais stāvoklis)', note:'precīzi plāni, fasādes, šķērsgriezums' },
      { icon:'📐', name:'AR projekts (legalizācijai)', note:'plāni + fasādes + paskaidrojuma raksts' },
      { icon:'📝', name:'Iesniegums BIS sistēmā', note:'elektronisks, pievienoti visi dokumenti' },
      { icon:'💬', name:'Sarakste ar pašvaldību', note:'atbildes uz komentāriem, precizējumi' },
      { icon:'📋', name:'NOD dokumentācija', note:'pēc büvatļaujas akceptēšanas' },
    ],
    steps: [
      { n:1, t:'ESI — Juridiskā esošās situācijas izpēte', who:'Volko', dur:'2–4 ned.', price:'950€', why:'KRITISKS! Pārbauda: vai zona atļauj šo ēku, vai nav aizsargjoslas, servitūti, citas juridiskas problēmas. BEZ ESI var iztērēt 5000€ uz projektu kas tiks noraidīts.' },
      { n:2, t:'TAA — Tehniskā apsekošana', who:'Volko', dur:'1–3 ned.', price:'400€', why:'Inženieris fiziski apskata ēku — pārbauda pamatus, sienas, jumtu, plaisas. Ja ēka bīstama — pašvaldība VAR pieprasīt nojaukšanu.' },
      { n:3, t:'Uzmērīšana (esošais stāvoklis)', who:'Volko', dur:'1–2 ned.', price:'Iekļauts AR', why:'Precīzi izmēra katru telpu, sienu, logu, durvi. Uz šiem datiem balstās viss projekts.' },
      { n:4, t:'AR projekts (legalizācijai)', who:'Volko', dur:'3–6 ned.', price:'Pēc kalkulatora', why:'Sagatavo pilnu dokumentāciju kas apliecina ka ēka atbilst normatīviem. Ietver plānus, fasādes, normatīvu analīzi.' },
      { n:5, t:'BIS iesniegums pašvaldībai', who:'Volko', dur:'1 diena', price:'Valsts nodeva ~14€', why:'Elektroniski iesniedz caur BIS — pievienoti visi dokumenti. Pašvaldībai 30 darba dienas atbildei.' },
      { n:6, t:'Pašvaldības izskatīšana + saskaņošana', who:'Pašvaldība + Volko', dur:'1–3 mēn.', price:null, why:'Büvvalde pārbauda projektu. Var pieprasīt precizējumus, papildu dokumentus vai izmaiņas. Volko atbild uz visiem jautājumiem.' },
      { n:7, t:'NOD — Nodošana ekspluatācijā', who:'Volko', dur:'1–2 mēn.', price:'950€', why:'Pēc büvatļaujas saņemšanas — nodod ēku oficāli. Sagatavo büvdarbu žurnālu, inženiertīklu aktus, energosertifikātu.' },
      { n:8, t:'Kadastrālā uzmērīšana', who:'VZD', dur:'2–4 ned.', price:'150–300€', why:'VZD atjaunina kadastra datus — platību, stāvus, adresi. Bez tā ēka kadastrā var būt neprecīza.' },
      { n:9, t:'Zemesgrāmata (ZG)', who:'Notārs / ZG tiesa', dur:'2–4 ned.', price:'50–200€', why:'Ēka ierakstāma ZG kā likumīga. Bez ZG ieraksta banka nedod kredītu, apdrošināšana problemātiska.' },
    ],
    risks: [
      { level:'high', icon:'🚫', text:'ATTEIKUMS: Ja pašvaldība atsakās legalizēt — ēka jānojauc. Risks augsts ja zona neatļauj, aizsargjosla, kultūrvēsturiskā zona.' },
      { level:'high', icon:'🚫', text:'TAA var atklāt defektus: Plaisas, mitrums, vāji pamati → pirms legalizācijas jālabo. Papildu izmaksas nav zināmas iepriekš.' },
      { level:'med', icon:'⚠️', text:'Kaimiņu konflikts: Ja ēka robežai tuvāk par 4m, kaimiņš var iebilst. Bez piekrišanas atļauju neizsniedz.' },
      { level:'med', icon:'⚠️', text:'Laika neskaidrība: Legalizācija reāli aizņem 12–36 mēnešus. Ja ir sarežģītības (kultūrvēsture, kopīpašums) — ilgāk.' },
      { level:'low', icon:'💡', text:'PADOMS: Sāc ar ESI! Ja ESI rāda zaļo gaismu — process ir iespējams. Tikai tad investē TAA un projektā.' },
    ]
  },

  // ── REKONSTRUKCIJA ──────────────────────────────────────────
  rekonstrukcija: {
    permit: (area, grp) => area <= 200 ? {
      name: 'Paskaidrojuma raksts',
      law: 'EBN 7.2 (11.punkts) — pārbūve līdz 200m²',
      desc: 'Rekonstrukcijai ≤200m² — paskaidrojuma raksts ja nemaina stāvu skaitu vai funkciju. Ja maina apjomu vai funkciju — büvatļauja.',
      bisType: 'Paskaidrojuma raksts'
    } : {
      name: 'Büvatļauja',
      law: 'EBN 71.punkts — pārbūve ≥200m²',
      desc: 'Pilnai rekonstrukcijai ≥200m² — büvatļauja. Termiņš 5+8 gadi.',
      bisType: 'Büvatļauja'
    },
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'zemesgramata.lv', req:'must' },
      { icon:'📁', name:'Esošie projekti / inventarizācijas lieta', note:'sākotnējie rasējumi ja ir', req:'must' },
      { icon:'📋', name:'Kadastrālās izpētes lieta', note:'kadastrs.lv', req:'must' },
      { icon:'🤝', name:'Kaimiņu piekrišana', note:'ja izmaiņas skar kopējās sienas vai robežu', req:'maybe' },
      { icon:'👥', name:'Kopīpašnieku piekrišana', note:'ja ir vairāki īpašnieki', req:'maybe' },
    ],
    volkoDocs: [
      { icon:'🔍', name:'TAA — Tehniskā apsekošana', note:'ieteicams — esošā stāvokļa novērtējums' },
      { icon:'📏', name:'Uzmērīšana (esošais stāvoklis)', note:'precīzi izmēri pirms rekonstrukcijas' },
      { icon:'📐', name:'AR projekts (rekonstrukcijai)', note:'izmainītais stāvoklis + normatīvu atbilstība' },
      { icon:'🏗️', name:'BK daļa', note:'ja mainās nesošās konstrukcijas' },
      { icon:'📝', name:'Iesniegums BIS', note:'elektronisks' },
      { icon:'📋', name:'NOD dokumentācija', note:'pēc darbu pabeigšanas' },
    ],
    steps: [
      { n:1, t:'TAA — Tehniskā apsekošana (ieteicams)', who:'Volko', dur:'1–2 ned.', price:'400€', why:'Pirms rekonstrukcijas — zini ar ko strādā. TAA var atklāt slēptas problēmas kas maina projekta apjomu.' },
      { n:2, t:'Skiču koncepcija', who:'Volko', dur:'1–3 ned.', price:'Iekļauts', why:'Klienta apstiprināšanai — kā izskatīsies pēc rekonstrukcijas.' },
      { n:3, t:'Darba projekts (AR + BK ja vajag)', who:'Volko', dur:'3–6 ned.', price:'Pēc kalkulatora', why:'Pilns projekts ar visām izmaiņām, normatīvu atbilstību, materiālu specifikācijām.' },
      { n:4, t:'BIS iesniegums', who:'Volko', dur:'1 diena', price:'Valsts nodeva', why:'Elektroniski iesniedz ar visiem pielikumiem.' },
      { n:5, t:'Pašvaldības izskatīšana', who:'Pašvaldība', dur:'30 darba d.', price:null, why:'Izskata atbilstību TIAN un büvnoteikumiem.' },
      { n:6, t:'Büvdarbi', who:'Klients (büvnieks)', dur:'Atkarīgs', price:'Nav Volko', why:'Rekonstrukcijas darbi pēc atļaujas saņemšanas.' },
      { n:7, t:'NOD — Nodošana ekspluatācijā', who:'Volko', dur:'1–2 mēn.', price:'950€', why:'Oficāli pabeidz rekonstrukciju — ieraksta izmaiņas kadastrā.' },
    ],
    risks: [
      { level:'high', icon:'⚠️', text:'Patvaļīgu izmaiņu atklāšana: Ja TAA atklāj ka jau iepriekš veiktas nereģistrētas izmaiņas — vajag arī tās legalizēt. Papildu izmaksas.' },
      { level:'med', icon:'⚠️', text:'Nesošo konstrukciju risks: Ja plāno mainīt nesošās sienas vai pārsegumus — obligāts BK projekts. Bez tā büvnieks nedrīkst strādāt.' },
      { level:'low', icon:'✅', text:'Rekonstrukcija ir standarta process. Ja nav sarežģītību — 6-12 mēneši no projekta līdz NOD.' },
    ]
  },

  // ── IZMAIŅU PROJEKTS ────────────────────────────────────────
  "izmaiņu": {
    permit: (area, grp) => ({
      name: 'Paskaidrojuma raksts vai Apliecinājuma karte',
      law: 'EBN 7.2 (8.punkts) — izmaiņas büvē',
      desc: 'Atkarīgs no izmaiņu apjoma. Ailas, fasāde, iekšējais plānojums (neskarot nesošās) → apliecinājuma karte. Lielākas izmaiņas → paskaidrojuma raksts.',
      bisType: 'Apliecinājuma karte / Paskaidrojuma raksts'
    }),
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'', req:'must' },
      { icon:'📁', name:'Esošie projekti', note:'sākotnējie rasējumi', req:'must' },
      { icon:'👥', name:'Kopīpašnieku piekrišana', note:'ja ir vairāki īpašnieki', req:'maybe' },
    ],
    volkoDocs: [
      { icon:'📏', name:'Esošā stāvokļa rasējumi', note:'ja nav pieejami oriģinālrasējumi' },
      { icon:'📐', name:'Izmaiņu rasējumi', note:'izmainītais stāvoklis' },
      { icon:'📝', name:'Iesniegums BIS', note:'ar izmaiņu aprakstu' },
    ],
    steps: [
      { n:1, t:'Situācijas izvērtējums', who:'Volko', dur:'1 ned.', price:null, why:'Nosaka vai vajag apliecinājuma karti vai paskaidrojuma rakstu.' },
      { n:2, t:'Izmaiņu rasējumi', who:'Volko', dur:'1–3 ned.', price:'Pēc kalkulatora', why:'Fiksē esošo un plānoto stāvokli.' },
      { n:3, t:'BIS iesniegums', who:'Volko', dur:'1 diena', price:null, why:'Iesniedz un gaida pašvaldības akcepts.' },
      { n:4, t:'Pašvaldības akcepts', who:'Pašvaldība', dur:'30 darba d.', price:null, why:'Apstiprina izmaiņas.' },
    ],
    risks: [
      { level:'med', icon:'⚠️', text:'Pārbaudīt vai izmaiņas neskar nesošās konstrukcijas — tad vajag BK projektu un paskaidrojuma rakstu.' },
      { level:'low', icon:'✅', text:'Izmaiņu projekts parasti ir ātrākais un lētākais process.' },
    ]
  },

  // ── VIENKĀRŠOTA ATJAUNOŠANA ──────────────────────────────────
  vienk: {
    permit: (area, grp) => ({
      name: 'Paskaidrojuma raksts',
      law: 'EBN 7.2 (6.punkts) — atjaunošana',
      desc: 'Fasādes atjaunošana, siltināšana, iekšējo telpu pārplānošana BEZ nesošo skaršanas. Nevar mainīt apjomu!',
      bisType: 'Paskaidrojuma raksts'
    }),
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'', req:'must' },
      { icon:'📁', name:'Esošie projekti', note:'', req:'maybe' },
    ],
    volkoDocs: [
      { icon:'📐', name:'Atjaunošanas apraksts + rasējumi', note:'esošais un plānotais stāvoklis' },
      { icon:'📝', name:'Iesniegums BIS', note:'' },
    ],
    steps: [
      { n:1, t:'Atjaunošanas projekts', who:'Volko', dur:'1–3 ned.', price:'Pēc kalkulatora', why:'Apraksta ko un kā tiks atjaunots.' },
      { n:2, t:'BIS iesniegums', who:'Volko', dur:'1 diena', price:null, why:'' },
      { n:3, t:'Pašvaldības akcepts', who:'Pašvaldība', dur:'30 darba d.', price:null, why:'' },
      { n:4, t:'Darbi', who:'Klients', dur:'Atkarīgs', price:null, why:'' },
    ],
    risks: [
      { level:'med', icon:'⚠️', text:'Nedrīkst skart nesošās konstrukcijas — tad būtu rekonstrukcija, nevis atjaunošana.' },
      { level:'low', icon:'✅', text:'Vienkāršākais un ātrākais legālais process aiz "bez saskaņošanas".' },
    ]
  },

  // ── FUNKCIJAS MAIŅA (lc) ─────────────────────────────────────
  lc: {
    permit: (area, grp) => ({
      name: 'Büvatļauja (ar funkcijas maiņu)',
      law: 'EBN 7.2 (7.punkts) — lietošanas veida maiņa + EBN 71',
      desc: 'Funkcijas maiņa (piem. saimniecības ēka → dzīvojamā) prasa büvatļauju ar rekonstrukcijas elementiem. SVARĪGI: ESI pirms viss — jāpārbauda vai zonā atļauta jaunā funkcija!',
      bisType: 'Büvatļauja (funkcijas maiņa)'
    }),
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'', req:'must' },
      { icon:'🏛️', name:'TIAN no pašvaldības', note:'svarīgi — vai zonā atļauta jaunā funkcija!', req:'must' },
      { icon:'📋', name:'Kadastrālās izpētes lieta', note:'', req:'must' },
      { icon:'👥', name:'Kopīpašnieku piekrišana', note:'ja ir', req:'maybe' },
    ],
    volkoDocs: [
      { icon:'⚖️', name:'ESI — Juridiskā izpēte', note:'PIRMAIS solis — vai iespējama?' },
      { icon:'📏', name:'Uzmērīšana (esošais stāvoklis)', note:'' },
      { icon:'📐', name:'AR projekts (jaunai funkcijai)', note:'sanitārie, ugunsdrošība, EPS' },
      { icon:'📝', name:'BIS iesniegums', note:'' },
      { icon:'📋', name:'NOD dokumentācija', note:'ar jauno funkciju' },
    ],
    steps: [
      { n:1, t:'ESI — Juridiskā esošās situācijas izpēte', who:'Volko', dur:'2–4 ned.', price:'950€', why:'KRITISKS! Pārbauda vai pašvaldības TIAN atļauj jauno funkciju. Bez ESI var iztērēt visu naudu uz projektu kas neiespējams.' },
      { n:2, t:'TAA — Tehniskā apsekošana', who:'Volko', dur:'1–2 ned.', price:'400€', why:'Jaunai funkcijai vajag citas prasības — TAA pārbauda vai ēka atbilst.' },
      { n:3, t:'AR projekts (jaunai funkcijai)', who:'Volko', dur:'4–7 ned.', price:'Pēc kalkulatora', why:'Ietver: plānojumu, sanitāros mezglus, ugunsdrošību, siltumizolāciju, EPS.' },
      { n:4, t:'BIS iesniegums + saskaņošana', who:'Volko', dur:'1–4 mēn.', price:'Valsts nodeva', why:'' },
      { n:5, t:'Büvdarbi (pielāgošana jaunai funkcijai)', who:'Klients', dur:'Atkarīgs', price:null, why:'' },
      { n:6, t:'NOD ar jauno funkciju', who:'Volko', dur:'1–2 mēn.', price:'950€', why:'Nodod ekspluatācijā ar jauno funkciju — kadastrā un ZG mainās funkcija.' },
      { n:7, t:'Kadastra + ZG atjaunošana', who:'VZD + notārs', dur:'3–5 ned.', price:'200€+', why:'' },
    ],
    risks: [
      { level:'high', icon:'🚫', text:'Zona neatļauj jauno funkciju — process apstājas. ESI to pārbauda pirms jebkādiem izdevumiem.' },
      { level:'med', icon:'⚠️', text:'Jaunai funkcijai bieži vajag pilnīgu pārbüvēšanu — sanitārie mezgli, siltumizolācija, ugunsdrošība. Büvniecības izmaksas var būt lielas.' },
      { level:'low', icon:'💡', text:'Ja ESI zaļa gaisma — process ir standarta. Rēķini 12-18 mēneši kopā.' },
    ]
  },

  // ── NOJAUKŠANA ──────────────────────────────────────────────
  "nojaukšana": {
    permit: (area, grp) => ({
      name: 'Apliecinājuma karte (nojaukšanai)',
      law: 'EBN 7.2 (9.punkts) — nojaukšana',
      desc: 'Reģistrētas ēkas nojaukšanai nepieciešama apliecinājuma karte. Pēc nojaukšanas — obligāti jāatjaunina kadastra dati.',
      bisType: 'Apliecinājuma karte'
    }),
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'', req:'must' },
      { icon:'📋', name:'Kadastrālās izpētes lieta', note:'', req:'must' },
      { icon:'⚡', name:'Inženiertīklu atslēgšanas akti', note:'elektriķis, ūdens, gāze', req:'must' },
    ],
    volkoDocs: [
      { icon:'📐', name:'Nojaukšanas projekts', note:'ēkas atrašanās vieta, robežas' },
      { icon:'📝', name:'Iesniegums BIS', note:'' },
      { icon:'📋', name:'Pēc nojaukšanas — kadastra aktualizācija', note:'' },
    ],
    steps: [
      { n:1, t:'Inženiertīklu atslēgšana', who:'Klients (speciālisti)', dur:'1–3 ned.', price:'Atsevišķi', why:'Pirms nojaukšanas — obligāti atslēdz elektrību, ūdeni, gāzi. Katram vajag aktus.' },
      { n:2, t:'Nojaukšanas projekts + BIS', who:'Volko', dur:'1–2 ned.', price:'Pēc kalkulatora', why:'Sagatavo dokumentāciju BIS sistēmai.' },
      { n:3, t:'Pašvaldības akcepts', who:'Pašvaldība', dur:'30 darba d.', price:null, why:'' },
      { n:4, t:'Nojaukšanas darbi', who:'Klients (büvnieks)', dur:'Atkarīgs', price:null, why:'' },
      { n:5, t:'Kadastra datu dzēšana', who:'VZD', dur:'2–4 ned.', price:'50–150€', why:'Obligāti! Pretējā gadījumā ēka papīros joprojām eksistē un tiek aplikta ar nodokļiem.' },
    ],
    risks: [
      { level:'high', icon:'🚫', text:'BEZ kadastra aktualizācijas — ēka joprojām "eksistē" papīros. Par to var piemērot nekustamā īpašuma nodokli!' },
      { level:'med', icon:'⚠️', text:'Kaimiņu ēkas tuvumā — jānodrošina ka nojaukšana neapdraud kaimiņu ēku. Var vajadzēt konstruktoru slēdzienu.' },
    ]
  },

  // ── VIENKĀRŠOTAS IZMAIŅAS (lbv) ──────────────────────────────
  lbv: {
    permit: (area, grp) => ({
      name: 'Paskaidrojuma raksts',
      law: 'EBN 7.2 (8.punkts) — nereģistrētas izmaiņas',
      desc: 'Vienkāršotas izmaiņas kas nav skārušas nesošās konstrukcijas vai fasādi. Salīdzinoši vienkāršs process — bieži 2-4 mēneši.',
      bisType: 'Paskaidrojuma raksts'
    }),
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'', req:'must' },
      { icon:'📁', name:'Esošie projekti', note:'ja ir oriģinālrasējumi', req:'maybe' },
      { icon:'👥', name:'Kopīpašnieku piekrišana', note:'ja ir', req:'maybe' },
    ],
    volkoDocs: [
      { icon:'📏', name:'Uzmērīšana (izmainītais stāvoklis)', note:'precīzi izmēri pēc izmaiņām' },
      { icon:'📐', name:'Rasējumi (esošais vs izmainītais)', note:'parāda ko tika mainīts' },
      { icon:'📝', name:'Iesniegums BIS', note:'' },
    ],
    steps: [
      { n:1, t:'Uzmērīšana un rasējumi', who:'Volko', dur:'1–2 ned.', price:'Pēc kalkulatora', why:'Dokumentē kas faktiski tika uzbūvēts / izmainīts.' },
      { n:2, t:'BIS iesniegums', who:'Volko', dur:'1 diena', price:'Valsts nodeva ~14€', why:'' },
      { n:3, t:'Pašvaldības akcepts', who:'Pašvaldība', dur:'30 darba d.', price:null, why:'' },
      { n:4, t:'Kadastra datu atjaunošana', who:'VZD', dur:'2–4 ned.', price:'50–150€', why:'Ja mainījās platība vai citi parametri.' },
    ],
    risks: [
      { level:'med', icon:'⚠️', text:'Pārbaudi — vai izmaiņas tiešām neskar nesošās sienas vai fasādi. Ja skar → vajag pilno procedūru (lbp).' },
      { level:'low', icon:'✅', text:'Vienkāršākais legalizācijas veids. Ja nav sarežģītību — 2-4 mēneši.' },
    ]
  },

  // ── PILNAS IZMAIŅAS (lbp) ────────────────────────────────────
  lbp: {
    permit: (area, grp) => ({
      name: 'Pārbüves atļauja / Paskaidrojuma raksts',
      law: 'EBN 7.2 (11.punkts) vai EBN 71 — nereģistrētas pārbüves',
      desc: 'Pilnas izmaiņas — nesošās konstrukcijas, fasāde, apjoms. Atkarīgs no ēkas un izmaiņu apjoma — var vajadzēt pārbüves atļauju vai büvatļauju.',
      bisType: 'Pārbüves atļauja'
    }),
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība', note:'', req:'must' },
      { icon:'📁', name:'Esošie projekti (ja ir)', note:'', req:'maybe' },
      { icon:'📋', name:'Kadastrālās izpētes lieta', note:'', req:'must' },
      { icon:'🤝', name:'Kaimiņu piekrišana', note:'ja skar fasādi un robeža <4m', req:'maybe' },
      { icon:'👥', name:'Kopīpašnieku piekrišana', note:'ja ir', req:'maybe' },
    ],
    volkoDocs: [
      { icon:'🔍', name:'TAA — Tehniskā apsekošana', note:'pirms jebkā — nesošo stāvoklis' },
      { icon:'📏', name:'Uzmērīšana', note:'esošais stāvoklis' },
      { icon:'📐', name:'AR projekts', note:'izmainītais stāvoklis + normatīvi' },
      { icon:'🏗️', name:'BK daļa', note:'ja mainās nesošās' },
      { icon:'📝', name:'BIS iesniegums', note:'' },
      { icon:'📋', name:'NOD (ja vajag)', note:'' },
    ],
    steps: [
      { n:1, t:'TAA — Tehniskā apsekošana', who:'Volko', dur:'1–2 ned.', price:'400€', why:'Jāzina esošais konstruktīvais stāvoklis pirms jebkāda projekta izstrādes.' },
      { n:2, t:'Uzmērīšana + AR projekts', who:'Volko', dur:'3–6 ned.', price:'Pēc kalkulatora', why:'Dokumentē faktisko stāvokli un normatīvu atbilstību.' },
      { n:3, t:'BIS iesniegums', who:'Volko', dur:'1 diena', price:'Valsts nodeva', why:'' },
      { n:4, t:'Pašvaldības saskaņošana', who:'Pašvaldība + Volko', dur:'1–3 mēn.', price:null, why:'' },
      { n:5, t:'NOD (ja vajadzīgs)', who:'Volko', dur:'1–2 mēn.', price:'950€', why:'' },
      { n:6, t:'Kadastra atjaunošana', who:'VZD', dur:'2–4 ned.', price:'100–300€', why:'' },
    ],
    risks: [
      { level:'high', icon:'⚠️', text:'TAA var atklāt konstrukciju defektus — pirms legalizācijas jālabo. Papildu izmaksas.' },
      { level:'med', icon:'⚠️', text:'Ja skar fasādi — kaimiņu piekrišana obligāta ja robeža <4m.' },
    ]
  },

  // ── TIPVEIDA ────────────────────────────────────────────────
  tipveida: {
    permit: (area, grp) => ({
      name: 'Paskaidrojuma raksts (atkārtota izmantošana)',
      law: 'EBN 7.2 — paskaidrojuma raksts ar tipveida projektu',
      desc: 'Tipveida projektu var reģistrēt vienu reizi un atkārtoti izmantot. Katrai izmantošanai vajag pielāgošanu konkrētam zemes gabalam.',
      bisType: 'Paskaidrojuma raksts'
    }),
    clientDocs: [
      { icon:'📄', name:'Zemesgrāmatas apliecība (katram zemes gabalam)', note:'', req:'must' },
      { icon:'📐', name:'Zemes robežu plāns', note:'', req:'must' },
      { icon:'🏛️', name:'TIAN', note:'katrai pašvaldībai atsevišķi', req:'must' },
    ],
    volkoDocs: [
      { icon:'📐', name:'Tipveida projekts (1.reize — pilns)', note:'vienu reizi izstrādā' },
      { icon:'📍', name:'Pielāgošana konkrētam zemes gabalam', note:'katrai izmantošanai' },
      { icon:'📝', name:'BIS iesniegums', note:'' },
    ],
    steps: [
      { n:1, t:'Tipveida projekta izstrāde (1.reize)', who:'Volko', dur:'4–8 ned.', price:'Pēc kalkulatora', why:'Pilns projekts ko var izmantot atkārtoti.' },
      { n:2, t:'Pielāgošana konkrētam zemes gabalam', who:'Volko', dur:'1–2 ned.', price:'Samazināta cena', why:'Katrai vietai — situācijas plāns, TN pielāgojums.' },
      { n:3, t:'BIS iesniegums', who:'Volko', dur:'1 diena', price:null, why:'' },
    ],
    risks: [
      { level:'low', icon:'✅', text:'Ekonomisks variants — 2.+ reize ir ievērojami lētāka.' },
      { level:'med', icon:'⚠️', text:'Katrai pašvaldībai TIAN atšķiras — pārbaudi ka tipveida projekts atbilst konkrētai vietai.' },
    ]
  }
};

function getPassportData(type) {
  return PASSPORT_DATA[type] || null;
}

function renderPassport(type, area, floors, muniName, svcCoef) {
  const passport = document.getElementById('ar-passport');
  if (!passport) return;

  const data = getPassportData(type);
  if (!data || !area) { passport.classList.remove('visible'); return; }
  passport.classList.add('visible');

  const g = grp(area, floors);
  const permit = data.permit(area, g);
  svcCoef = svcCoef || 1.0;

  // Permit badge
  const badge = document.getElementById('pp-permit-badge');
  if (badge) badge.textContent = permit.bisType;

  // Permit section
  const permitBox = document.getElementById('pp-permit-box');
  if (permitBox) {
    permitBox.innerHTML = `
      <div class="pp-permit-name">📋 ${permit.name}</div>
      <div class="pp-permit-law" style="margin-top:3px;color:#9ca3af">${permit.law}</div>
      <div class="pp-permit-desc">${permit.desc}</div>
    `;
  }

  // Document columns
  const docCols = document.getElementById('pp-doc-cols');
  if (docCols && data.clientDocs && data.volkoDocs) {
    const clientHtml = `
      <div>
        <div class="doc-col-title client">📂 Klients sagādā</div>
        ${data.clientDocs.map(d => `
          <div class="doc-item">
            <span class="doc-icon">${d.icon}</span>
            <div>
              <div class="doc-name">${d.name}${d.req === 'must' ? '<span class="doc-req must">OBLIGĀTS</span>' : '<span class="doc-req maybe">JA ATTIECAS</span>'}</div>
              ${d.note ? `<div class="doc-note">${d.note}</div>` : ''}
            </div>
          </div>`).join('')}
      </div>
    `;
    const volkoHtml = `
      <div>
        <div class="doc-col-title volko">⚙️ Volko sagatavo BIS</div>
        ${data.volkoDocs.map(d => `
          <div class="doc-item">
            <span class="doc-icon">${d.icon}</span>
            <div>
              <div class="doc-name">${d.name}</div>
              ${d.note ? `<div class="doc-note">${d.note}</div>` : ''}
            </div>
          </div>`).join('')}
      </div>
    `;
    docCols.innerHTML = clientHtml + volkoHtml;
  }

  // Timeline
  const timeline = document.getElementById('pp-timeline');
  if (timeline && data.steps) {
    timeline.innerHTML = data.steps.map(s => `
      <div class="tl-step">
        <div class="tl-num">${s.n}</div>
        <div class="tl-content">
          <div class="tl-title">${s.t}${s.price && s.price !== 'Iekļauts' && s.price !== 'Pēc kalkulatora' && s.price !== null ? `<span class="tl-price-tag">${s.price}</span>` : ''}</div>
          <div class="tl-who">${s.who ? 'Veic: ' + s.who : ''}${s.dur ? ' · <span class="tl-dur">⏱ ' + s.dur + '</span>' : ''}</div>
          ${s.why ? `<div class="tl-why">${s.why}</div>` : ''}
        </div>
      </div>
    `).join('');
  }

  // Cost table
  const costTable = document.getElementById('pp-cost-table');
  if (costTable) {
    // Build cost rows based on steps that have prices
    const costItems = [];
    if (data.steps) {
      data.steps.forEach(s => {
        if (s.price && s.price !== 'Iekļauts' && s.price !== 'Pēc kalkulatora' && s.price !== null && s.price !== 'Nav Volko' && s.price !== 'Atsevišķi') {
          // Parse price
          const match = s.price.match(/(\d+)/);
          if (match) {
            const base = parseInt(match[1]);
            const adjusted = Math.round(base * svcCoef);
            costItems.push({ name: s.t, base: base, adj: adjusted });
          }
        }
      });
    }

    // Get AR project price from main calc
    const mainPriceEl = document.getElementById('ar-p-int');
    const mainPrice = mainPriceEl ? mainPriceEl.textContent.replace(/[^\d]/g,'') : '';

    let html = '';
    if (mainPrice) {
      html += `<tr><td class="ct-name">AR projekts (Volko)</td><td class="ct-price">${parseInt(mainPrice).toLocaleString('lv-LV')} EUR</td></tr>`;
    }
    costItems.forEach(ci => {
      html += `<tr><td class="ct-name">${ci.name}</td><td class="ct-price">${ci.adj.toLocaleString('lv-LV')} EUR</td></tr>`;
    });

    // Valsts nodevas
    html += `<tr><td class="ct-name" style="color:var(--muted)">Valsts nodevas (BIS, kadastra)</td><td class="ct-price" style="color:var(--muted)">~200–500 EUR</td></tr>`;

    // Total
    let total = mainPrice ? parseInt(mainPrice) : 0;
    costItems.forEach(ci => total += ci.adj);
    total += 350; // avg state fees

    html += `<tr class="sep"><td class="ct-total">KOPĀ (iekšējā cena)</td><td class="ct-total-price">~${total.toLocaleString('lv-LV')} EUR</td></tr>`;

    const clientTotal = Math.round(total * 1.2 / 50) * 50;
    html += `<tr><td class="ct-total" style="color:var(--gold)">Klientam (ar 20% rezervi)</td><td class="ct-total-price" style="color:var(--gold)">no ${clientTotal.toLocaleString('lv-LV')} EUR</td></tr>`;

    costTable.innerHTML = html;
  }

  // Risks
  const risksEl = document.getElementById('pp-risks');
  if (risksEl && data.risks) {
    risksEl.innerHTML = data.risks.map(r => `
      <div class="risk-row ${r.level}">
        <span class="risk-icon">${r.icon}</span>
        <span>${r.text}</span>
      </div>
    `).join('');
  }
}
"""

# Insert PASSPORT_JS before the 3D init
marker = '// ══════════════════════════════════════════════════════════════\n// THREE.JS'
html = html.replace(marker, PASSPORT_JS + '\n' + marker)

# ── 4. CALL renderPassport FROM calcAR ───────────────────────
# Add call to renderPassport at the end of calcAR (before renderARPanels call)
old_render = '  renderARPanels(type,area,muni.s);\n}'
new_render = '  renderARPanels(type,area,muni.s);\n  const _mname = document.getElementById("ar-muni").options[document.getElementById("ar-muni").selectedIndex]?.text || "";\n  renderPassport(type,area,floors,_mname,muni.s);\n}'
if old_render in html:
    html = html.replace(old_render, new_render, 1)
    print("✓ renderPassport call added to calcAR")
else:
    print("WARNING: Could not find calcAR render call")

# Also hide passport when no type
old_hide = '    ["jaunbuve-paketes","legalizacija-paketes","auto-ieteikumi"].forEach(id=>{document.getElementById(id).classList.remove("visible");});\n    return;\n  }'
new_hide = '    ["jaunbuve-paketes","legalizacija-paketes","auto-ieteikumi"].forEach(id=>{document.getElementById(id).classList.remove("visible");});\n    const _pp=document.getElementById("ar-passport");if(_pp)_pp.classList.remove("visible");\n    return;\n  }'
if old_hide in html:
    html = html.replace(old_hide, new_hide, 1)
    print("✓ Passport hide on empty added")

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Done! {len(html)} chars")

# Syntax check
import subprocess, tempfile, os
scriptStart = html.find("<script>") + 8
scriptEnd = html.rfind("</script>")
js = html[scriptStart:scriptEnd]
tmp = os.path.join(tempfile.gettempdir(), "volko_passport_check.js")
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(js)
result = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
if result.returncode == 0:
    print("✓ JS syntax OK")
else:
    print("✗ JS ERROR:", result.stderr[:600])
