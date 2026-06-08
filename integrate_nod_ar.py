"""
Integrē NOD tab un AR uzlabojumus index.html.
"""
import re, subprocess, tempfile, os

KALK = r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\index.html"
NOD_TAB = r"C:\Users\matri\OneDrive - VolkoEngineering\nod-tab.html"

with open(KALK, encoding="utf-8") as f:
    html = f.read()
with open(NOD_TAB, encoding="utf-8") as f:
    nod_raw = f.read()

# ── Extract NOD parts ─────────────────────────────────────────
nod_css_match = re.search(r"<style>(.*?)</style>", nod_raw, re.DOTALL)
nod_css = nod_css_match.group(1) if nod_css_match else ""

nod_tab_html_match = re.search(r'(<div id="tab-nod".*?</div>)\s*</div><!-- /tab-nod -->', nod_raw, re.DOTALL)
if nod_tab_html_match:
    nod_html = nod_tab_html_match.group(0).replace("</div><!-- /tab-nod -->", "")
else:
    # fallback - get from tab-nod to script
    nod_start = nod_raw.find('<div id="tab-nod"')
    nod_end = nod_raw.find("<script>", nod_start)
    nod_html = nod_raw[nod_start:nod_end].strip()

nod_js_match = re.search(r"<script>(.*?)</script>", nod_raw, re.DOTALL)
nod_js = nod_js_match.group(1) if nod_js_match else ""

print(f"NOD CSS: {len(nod_css)} chars")
print(f"NOD HTML: {len(nod_html)} chars")
print(f"NOD JS: {len(nod_js)} chars")

# ── 1. Add NOD CSS to existing styles ────────────────────────
html = html.replace("</style>\n</head>", nod_css + "\n</style>\n</head>", 1)

# ── 2. Add NOD tab button ─────────────────────────────────────
old_tabs = '<button class="tab-btn" onclick="switchTab(\'bk\',this)">⚙️ BK — Būvkonstrukcijas</button>\n</div>'
new_tabs = '<button class="tab-btn" onclick="switchTab(\'bk\',this)">⚙️ BK — Būvkonstrukcijas</button>\n<button class="tab-btn" onclick="switchTab(\'nod\',this)">🏁 NOD — Nodošana</button>\n</div>'
if old_tabs in html:
    html = html.replace(old_tabs, new_tabs)
    print("✓ NOD tab button added")
else:
    print("WARNING: could not find BK tab button")

# ── 3. Add NOD tab HTML before closing app div ───────────────
# Find the pattern before the floating AI button
insert_marker = '\n<!-- ══════════════════════════════════════════════════════════\n     FLOATING AI CHAT'
nod_insert = '\n' + nod_html + '\n'
html = html.replace(insert_marker, nod_insert + insert_marker)
print("✓ NOD HTML inserted")

# ── 4. Add NOD JS before 3D init ─────────────────────────────
marker_3d = "// ══════════════════════════════════════════════════════════════\n// THREE.JS"
nod_js_wrapped = "\n// ── NOD TAB JAVASCRIPT ──────────────────────────────────────────\n" + nod_js + "\n"
html = html.replace(marker_3d, nod_js_wrapped + marker_3d)
print("✓ NOD JS added")

# ── 5. Add Sadaļa 7 (NOD) to AI_SYSTEM ───────────────────────
NOD_AI_SECTION = """
══════════════════════════════════════════
SADAĻA 7 — NOD (NODOŠANA EKSPLUATĀCIJĀ)
══════════════════════════════════════════

NOD ir OBLIGĀTS pēdējais solis pēc büvdarbu pabeigšanas.
BEZ NOD ēka juridiski ir "büvniecībā" pat ja fiziski pilnīgi gatava.

SEKAS BEZ NOD:
- Banka NEIZSNIEDZ hipotekāro kredītu
- Ēka kadastrā = "nepabeigta"
- Zemāka nekustamā īpašuma vērtība
- Problēmas ar elektroenerģijas/gāzes pieslēgumu aktivizēšanu
- Juridiskie riski pārdošanā

NOD DOKUMENTS — VISI ATZINUMI:

VIENMĒR OBLIGĀTI:
1. Büvdarbu žurnāls — büvnieks aizpilda BIS. BIEŽA KĻŪDA: nav aizpildīts → NOD apstājas!
2. Atbilstības deklarācija — büvnieks paraksta
3. NOD iesniegums BIS — Volko sagatavo un iesniedz (~30€ valsts nodeva)

TEHNISKIE ATZINUMI (atkarīgi no sistēmām):
ELT (~120-200€) — elektroinstalācija. Sertificēts elektriķis (SAB sertifikāts). OBLIGĀTS. Bez ELT Sadales tīkls neaktivizē elektroenerģiju!
EPS (~370€) — energosertifikāts. Sertificēts energoauditors. OBLIGĀTS jaunbüvēm ar apkuri. (MK not. 348)
D/V (~60-110€) — dümvadu/ventilācijas atzinums. Sertificēts skursteņslauķis/inspektors. JA ir kamīns, dümvads, mehāniskā ventilācija.
Santehnika (~80-130€) — ūdens/kanalizācijas akts. Sertificēts santehniķis. JA ir ūdensapgāde.
Gāze (~100-150€) — LAGAS atzinums. Latvijas Gāze/Conexus speciālists. JA ir gāze. KRITISKS — bez tā gāze netiek aktivizēta!
Apkure (~80-120€) — siltumtehniskais atzinums. JA ir autonomā apkures sistēma.
VUGD (~150-250€) — ugunsdrošības atzinums. OBLIGĀTS publiskām, komercobjektiem, daudzdzīvokļu mājām.
Lifts (~300-400€) — PTAC reģistrācija un atzinums. JA ir lifts (bez izņēmuma).
PV saules (~150-200€) — ELT atzinums par saules sistēmu. JA ir saules paneļi.

KOMUNĀLIE TĪKLI:
Sadales tīkls — elektroenerģijas pieslēguma apliecinājums (bez maksas, klients kārto)
Ūdenssaimniecība — pieslēguma akts (bez maksas, klients kārto ar ūdens operatoru)
Siltumtīkls — pieslēguma akts (bez maksas, klients kārto ar siltuma operatoru)
Latvijas Gāze — gāzes pieslēguma akts (klients kārto tieši)

KADASTRĀLĀ UZMĒRĪŠANA:
VZD kadastrālā uzmērīšana (~400-800€) — ja ēkas izmēri atšķiras no projekta
Zemesgrāmatas ieraksts (~30-50€) — pēc NOD akcepta

NOD PROCESS (termiņi):
1. Dokumentu sagatavošana: 1-2 ned. (Volko)
2. Atzinumu pasūtīšana: 1-3 ned. (paralēli, daži klients kārto patstāvīgi)
3. BIS iesniegums: 1 diena
4. BIS izskatīšana: 10-30 darba dienas (likumā noteikts)
5. Inspekcija + akcepts: 5-15 darba dienas
KOPĀ: optimistiskais 6-10 ned., reālistiskais 2-4 mēneši

VOLKO KĀRTO: BIS iesniegums, ELT koordinācija, EPS koordinācija, D/V koordinācija, visu dokumentu apkopošana
KLIENTS KĀRTO: büvdarbu žurnāls (caur büvnieku), santehnikas akts, gāzes akts (Latvijas Gāze tieši), lifta atzinums, pieslēgumu akti

SVARĪGI: Katrai ēkai dokumentu saraksts atšķiras. Precīzam sarakstam → Volko Engineering.
"""

old_ai_end = "INFORMĀCIJA PAR VOLKO:\n- Kontakts: info@volkoengineering.com | volkoengineering.com\n- Projektu konsultants: Toms (Arhitektūra/AR)\n- Büvkonstrukcijas: Vladimirs (BK)\n- Novirzi uz Volko: precīzai cenai, situācijas izvērtēšanai, pašvaldības specifiskiem jautājumiem`;"
new_ai_end = "INFORMĀCIJA PAR VOLKO:\n- Kontakts: info@volkoengineering.com | volkoengineering.com\n- Projektu konsultants: Toms (Arhitektūra/AR)\n- Büvkonstrukcijas: Vladimirs (BK)\n- Novirzi uz Volko: precīzai cenai, situācijas izvērtēšanai, pašvaldības specifiskiem jautājumiem" + NOD_AI_SECTION + "`;"
html = html.replace(old_ai_end, new_ai_end)
print("✓ NOD Sadaļa 7 added to AI_SYSTEM")

# ── 6. Add AR municipality info panel ────────────────────────
# Add function showMuniInfo + pre-checklist data
AR_EXTRAS_CSS = """
/* AR municipality info panel */
.muni-info-panel{display:none;background:#fffbf0;border-left:3px solid var(--gold);border-radius:0 8px 8px 0;padding:10px 13px;margin-top:8px;font-size:.76rem;line-height:1.55}
.muni-info-panel.visible{display:block}
.muni-info-title{font-weight:700;color:var(--navy);margin-bottom:5px;font-size:.82rem}
.muni-note{display:flex;gap:5px;padding:2px 0;color:var(--text)}
.muni-note::before{content:"ℹ";color:var(--gold);flex-shrink:0}
.muni-warn{display:flex;gap:5px;padding:2px 0;color:#991b1b}
.muni-warn::before{content:"⚠";flex-shrink:0}
.muni-time-badge{display:inline-flex;align-items:center;gap:4px;background:var(--navy);color:var(--gold);font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:12px;margin-top:6px}
/* Pre-checklist */
.pre-checklist{display:none}
.pre-checklist.visible{display:block}
.cl-item{display:flex;gap:8px;padding:6px 0;border-bottom:1px solid var(--border);font-size:.78rem;align-items:flex-start}
.cl-item:last-child{border-bottom:none}
.cl-item input{width:14px;height:14px;accent-color:var(--gold);flex-shrink:0;margin-top:2px;cursor:pointer}
.cl-item.critical{background:#fff7f7;border-left:2px solid var(--red);padding-left:6px;border-radius:0 4px 4px 0;border-bottom:none;margin-bottom:2px}
.cl-cat{display:inline-block;font-size:.58rem;font-weight:700;padding:1px 5px;border-radius:3px;margin-left:4px;vertical-align:middle}
.cl-cat.zona{background:#dbeafe;color:#1e40af}
.cl-cat.ipasums{background:#dcfce7;color:#166534}
.cl-cat.tehniski{background:#fef9c3;color:#713f12}
.cl-cat.finanses{background:#f3e8ff;color:#6b21a8}
.cl-prog{font-size:.72rem;color:var(--muted);margin-top:8px;text-align:right}
"""

html = html.replace("</style>\n</head>", AR_EXTRAS_CSS + "</style>\n</head>", 1)

AR_EXTRAS_JS = r"""
// ── AR MUNICIPALITY INFO ──────────────────────────────────────
const MUNI_INFO = {
  '{"p":1.20,"s":1.05}': {
    name:'Rīga',
    notes:['Lielākā un sarežğītākā pašvaldība Latvijā','Büvniecības padome lieliem objektiem (>500m² vai 3+ stāvi) — papildu 1-2 mēn.','Digitālā iesniegšana BIS labi attīstīta','RDPAD, Dzirnavu iela 140 | e.riga.lv'],
    warnings:['Rīgas Vēsturiskais Centrs (RVC): NKMP saskaņošana VISĀM izmaiņām — +3-6 mēn.!','Pārbaudīt vai objekts nav RVC aizsargjoslā pirms projekta sākšanas'],
    time:'Standarta: 6-10 mēn. | RVC: 12-18 mēn.'
  },
  '{"p":1.10,"s":1.05}': {
    name:'Rīgas apkārtne',
    notes:['Mārupes, Ķekavas, Salaspils, Ādažu, Ropažu, Olaines, Stopiņu, Garkalnes, Babītes, Carnikavas novads','Augsts büvniecības pieprasījums — pašvaldības noslogotas','Standarta procedūras pēc EBN'],
    warnings:['Jaunattīstāmās teritorijas — var būt nepietiekami inženiertīkli'],
    time:'5-8 mēn.'
  },
  '{"p":1.00,"s":1.10}': {
    name:'Jūrmala / Sigulda / Standarta novadi',
    notes:['Jūrmala: 6 pilsētbüvniecības pieminekļi, krasta kāpu aizsargjosla','Sigulda: Gaujas NP — saskaņot ar Dabas aizsardzības pārvaldi','Jūrmalā pieejams līdzfinansējums pieminekļu atjaunošanai'],
    warnings:['Jūrmala piekraste 300m — büvniecība LIEGTA. 150m apdzīvotās — strikti ierobežojumi','Jūrmala: kulturtelpa@jurmala.lv jāsaskaņo koka ēku izmaiņas'],
    time:'6-10 mēn. (7-14 mēn. kultūrvēsturiskā zonā)'
  },
  '{"p":1.02,"s":1.15}': {
    name:'Valmiera, Talsi, Saldus un citi',
    notes:['Valmieras novads: Gaujas piekrastes aizsargjosla','Standarta procedūras, zemāks pieprasījums'],
    warnings:[],
    time:'6-10 mēn.'
  },
  '{"p":1.05,"s":1.20}': {
    name:'Liepāja, Ventspils, Daugavpils, Rēzekne',
    notes:['Liepājas Karosta: striktas NKMP prasības (valsts nozīmes piemineklis)','Daugavpils cietoksnis: aktīva restaurācija','Rēzeknes novads: standarta procedūras'],
    warnings:['Karosta zona: NKMP saskaņošana OBLIGĀTA'],
    time:'6-10 mēn.'
  }
};

function showMuniInfo(val) {
  const panel = document.getElementById('ar-muni-info-panel');
  if (!panel) return;
  const data = MUNI_INFO[val];
  if (!data) { panel.classList.remove('visible'); return; }
  panel.classList.add('visible');
  let html = `<div class="muni-info-title">📍 ${data.name}</div>`;
  data.notes.forEach(n => { html += `<div class="muni-note">${n}</div>`; });
  data.warnings.forEach(w => { html += `<div class="muni-warn">${w}</div>`; });
  html += `<div class="muni-time-badge">⏱ Tipiskais termiņš: ${data.time}</div>`;
  panel.innerHTML = html;
}

// ── AR PRE-PROJECT CHECKLIST ─────────────────────────────────
const PRE_CHECKS = {
  jaunbuve: [
    {text:'Pārbaudi TIAN — kāda zona, apbüves procents, max augstums, atkāpes no robežas', cat:'zona', why:'Bez TIAN pārbaudes var taisīt projektu kas pašvaldībā tiks noraidīts', critical:true},
    {text:'Noskaidro vai zeme nav lauksaimniecības zeme (vajag mērķa maiņu)', cat:'zona', why:'Lauksaimniecības zeme → mērķa maiņa 3-6 mēn. pirms büvniecības', critical:true},
    {text:'Pārbaudi vai nav servitūti, aizsargjoslas (gāze, elektrolīnija, upe)', cat:'ipasums', why:'Aizsargjoslā var liegt büvniecību', critical:false},
    {text:'Pārbaudi vai pašvaldība nepieprasa Detālplānojumu (DP)', cat:'zona', why:'DP process 1-3 gadi — jāzina pirms projekta sākšanas', critical:true},
    {text:'Noskaidro inženiertīklu pieslēguma iespējas (ūdens, kanalizācija, elektrība, gāze)', cat:'tehniski', why:'Bez pieslēgumiem jaunbüves vērtība ir zemāka', critical:false},
    {text:'Pasūti robežu plānu un topogrāfiju (ja nav aktuāls)', cat:'tehniski', why:'Nepieciešams projekta sākšanai', critical:false},
    {text:'Pārbaudi kopīpašnieku situāciju', cat:'ipasums', why:'Visu kopīpašnieku piekrišana obligāta', critical:false},
    {text:'Noskaidro orientējošo büvniecības budžetu', cat:'finanses', why:'Projektam jāatbilst finansiālajām iespējām', critical:false},
  ],
  la: [
    {text:'ESI — Juridiskā esošās situācijas izpēte (950€) — PIRMS VISA!', cat:'zona', why:'ESI pārbauda vai legalizācija vispār iespējama. Bez ESI risks iztērēt 5000€ projektā kas tiks noraidīts.', critical:true},
    {text:'Pārbaudi vai kaimiņš nezina/iebilst (robeža <4m)', cat:'ipasums', why:'Kaimiņa piekrišana obligāta — bez tā BIS noraidīs', critical:true},
    {text:'Pārbaudi vai nav aktīvu tiesvedību par īpašumu', cat:'ipasums', why:'Tiesvedības bloķē BIS procesus', critical:true},
    {text:'TAA — Tehniskā apsekošana (400€) — konstruktīvā drošība', cat:'tehniski', why:'Pašvaldība var pieprasīt nojaukšanu ja ēka bīstama', critical:true},
    {text:'Noskaidro TIAN — vai zona atļauj šo ēku', cat:'zona', why:'Ja zona neatļauj → legalizācija neiespējama', critical:true},
    {text:'Pārbaudi kopīpašnieku situāciju', cat:'ipasums', why:'Visu kopīpašnieku piekrišana obligāta pirms legalizācijas', critical:false},
  ],
  rekonstrukcija: [
    {text:'Pārbaudi vai nav patvaļīgas büvniecības (arī iepriekšējo īpašnieku)', cat:'ipasums', why:'Atklātas patvaļīgās izmaiņas jālegalizē vienlaikus — papildu izmaksas', critical:true},
    {text:'Ieteicams TAA — Tehniskā apsekošana (400€) pirms projekta', cat:'tehniski', why:'TAA var atklāt slēptas problēmas kas maina projekta apjomu', critical:false},
    {text:'Pārbaudi vai mainīsies nesošās konstrukcijas — vajag BK projektu', cat:'tehniski', why:'Bez BK projekta büvnieks nedrīkst mainīt nesošās', critical:false},
    {text:'Pārbaudi kopīpašnieku situāciju', cat:'ipasums', why:'Piekrišana obligāta', critical:false},
    {text:'Noskaidro vai skar kultūrvēsturisko zonu (NKMP)', cat:'zona', why:'NKMP saskaņošana +2-6 mēn.', critical:false},
  ],
  izmaiņu: [
    {text:'Pārbaudi vai izmaiņas neskar nesošās konstrukcijas', cat:'tehniski', why:'Ja skar → vajag pārbüves projektu, nevis izmaiņu projektu', critical:true},
    {text:'Pārbaudi vai ēka ir kultūrvēsturiskā zonā', cat:'zona', why:'NKMP saskaņošana obligāta katrai izmaiņai', critical:false},
  ],
  vienk: [
    {text:'Pārbaudi ka atjaunošana neskar nesošās konstrukcijas vai fasādes apjomu', cat:'tehniski', why:'Ja skar → vajag pārbüves projektu, ne atjaunošanu', critical:true},
  ],
  lbv: [
    {text:'Pārbaudi vai izmaiņas tiešām neskar nesošās sienas vai fasādi', cat:'tehniski', why:'Ja skar → vajag pilno legalizācijas procedūru (lbp)', critical:true},
  ],
  lbp: [
    {text:'ESI — Juridiskā esošās situācijas izpēte — ieteicams pirms visa', cat:'zona', why:'Pārbauda vai pilnā legalizācija iespējama', critical:false},
    {text:'TAA — Tehniskā apsekošana pirms projekta', cat:'tehniski', why:'TAA parāda faktisko stāvokli, var atklāt problēmas', critical:true},
  ],
  lc: [
    {text:'ESI — Juridiskā izpēte — OBLIGĀTA PIRMĀ (950€)', cat:'zona', why:'Pārbauda vai jaunā funkcija atļauta šajā zonā. Bez ESI var iztērēt visu naudu uz neiespējamu projektu.', critical:true},
    {text:'Pārbaudi vai zonā atļauta jaunā funkcija (TIAN)', cat:'zona', why:'Ja zona neatļauj → process apstājas uzreiz', critical:true},
  ],
  nojaukšana: [
    {text:'Pārbaudi vai nav aktīvo inženiertīklu (elektroinstalācija, gāze, ūdens)', cat:'tehniski', why:'Pirms nojaukšanas jāatslēdz visi tīkli un jāsaņem atslēgšanas akti', critical:true},
    {text:'Pārbaudi vai blakus ēkas nav risks no nojaukšanas', cat:'tehniski', why:'Var vajadzēt konstruktoru slēdzienu', critical:false},
  ],
  tipveida: [
    {text:'Pārbaudi TIAN konkrētajam zemes gabalam', cat:'zona', why:'Katrai pašvaldībai un vietai noteikumi atšķiras', critical:true},
    {text:'Pasūti topogrāfiju konkrētajam zemes gabalam', cat:'tehniski', why:'Tipveida projektam vajag pielāgot situācijas plānu', critical:false},
  ]
};

function showPreChecklist(type) {
  const panel = document.getElementById('ar-pre-checklist');
  if (!panel) return;
  const items = PRE_CHECKS[type];
  if (!items || items === undefined) { panel.classList.remove('visible'); return; }
  panel.classList.add('visible');
  const catLabels = {zona:'Zona',ipasums:'Īpašums',tehniski:'Tehniski',finanses:'Finanses'};
  let html = '';
  items.forEach((item,i) => {
    html += `<div class="cl-item${item.critical?' critical':''}">
      <input type="checkbox" id="cl-${i}" onchange="updateClProgress()">
      <div>
        <span>${item.text}</span>
        <span class="cl-cat ${item.cat}">${catLabels[item.cat]||item.cat}</span>
        <div style="font-size:.68rem;color:var(--muted);margin-top:2px">💡 ${item.why}</div>
      </div>
    </div>`;
  });
  html += `<div class="cl-prog" id="cl-prog">0 / ${items.length} izpildīts</div>`;
  panel.querySelector('.pre-checklist-body').innerHTML = html;
}

function updateClProgress() {
  const total = document.querySelectorAll('.cl-item input').length;
  const done = document.querySelectorAll('.cl-item input:checked').length;
  const prog = document.getElementById('cl-prog');
  if (prog) prog.textContent = `${done} / ${total} izpildīts`;
}

// Hook into existing calcAR to call showMuniInfo and showPreChecklist
const _origCalcAR = calcAR;
function calcAR() {
  _origCalcAR();
  const muniVal = document.getElementById('ar-muni') ? document.getElementById('ar-muni').value : '';
  const typeVal = document.getElementById('ar-type') ? document.getElementById('ar-type').value : '';
  showMuniInfo(muniVal);
  showPreChecklist(typeVal);
}
"""

# Add AR extras JS before 3D init
html = html.replace("// ── NOD TAB JAVASCRIPT", AR_EXTRAS_JS + "\n// ── NOD TAB JAVASCRIPT")
print("✓ AR municipality info + pre-checklist JS added")

# ── 7. Add muni info panel and pre-checklist HTML to AR form ─
# Insert after the municipality select
old_muni_field = '          <option value=\'{"p":1.00,"s":1.10}\'>Cits novads</option>\n        </select></div>'
new_muni_field = old_muni_field + '\n        <div id="ar-muni-info-panel" class="muni-info-panel"></div>'
html = html.replace(old_muni_field, new_muni_field, 1)

# Insert pre-checklist after apgrūtinājumi section (before closing </div></div>)
old_encumb_end = '</div></div>\n</div>\n</div>\n<div style="margin-top:16px">'
new_encumb_end = old_encumb_end.replace(
    '</div></div>\n</div>\n</div>',
    '</div></div>\n</div>\n</div>\n<div class="card pre-checklist" id="ar-pre-checklist" style="margin-top:0">\n<div class="card-title">✅ Pirms sākam — pārbaudi šos punktus</div>\n<div class="pre-checklist-body"></div>\n</div>'
)
if old_encumb_end in html:
    html = html.replace(old_encumb_end, new_encumb_end, 1)
    print("✓ Pre-checklist panel added to AR form")

# Add onchange to municipality select
html = html.replace(
    'id="ar-muni" onchange="calcAR()"',
    'id="ar-muni" onchange="calcAR();showMuniInfo(this.value)"'
)

# ── Write and verify ──────────────────────────────────────────
with open(KALK, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\nFile written: {len(html)} chars")

scriptStart = html.find("<script>") + 8
scriptEnd = html.rfind("</script>")
js = html[scriptStart:scriptEnd]
tmp = os.path.join(tempfile.gettempdir(), "volko_nod_check.js")
with open(tmp, "w", encoding="utf-8") as f:
    f.write(js)
result = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
if result.returncode == 0:
    print("✓ JS syntax OK")
else:
    print("✗ JS ERROR:", result.stderr[:500])
