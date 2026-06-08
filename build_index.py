import re

with open(r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\ar-section.html", encoding="utf-8") as f:
    ar = f.read()
with open(r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\bk-ai-section.html", encoding="utf-8") as f:
    bk_ai = f.read()

ar_css  = re.search(r"<style>(.*?)</style>", ar, re.DOTALL).group(1)
ar_js_raw = re.search(r"<script>(.*?)</script>", ar, re.DOTALL).group(1)
ar_js = re.sub(r"// ─── STANDALONE DEMO ─+.*", "", ar_js_raw, flags=re.DOTALL).strip()

bk_css_all = re.findall(r"<style>(.*?)</style>", bk_ai, re.DOTALL)
bk_css = "\n".join(bk_css_all)
bk_ai_js = re.search(r"<script>(.*?)</script>", bk_ai, re.DOTALL).group(1)

bk_start = bk_ai.find('<div id="tab-bk"')
ai_start = bk_ai.find('<div id="tab-ai"')
scr_start = bk_ai.find("<script>", ai_start)
bk_html_raw = bk_ai[bk_start:ai_start].strip()
ai_html_raw = bk_ai[ai_start:scr_start].strip()

# Strip outer div wrappers (they had style="display:none")
bk_html = re.sub(r'^<div id="tab-bk"[^>]*>', '', bk_html_raw).rstrip()
if bk_html.endswith('</div>'):
    bk_html = bk_html[:-6].rstrip()

ai_html = re.sub(r'^<div id="tab-ai"[^>]*>', '', ai_html_raw).rstrip()
if ai_html.endswith('</div>'):
    ai_html = ai_html[:-6].rstrip()

body_start = ar.find("<body>") + 6
script_start = ar.find("<script>")
ar_panels = ar[body_start:script_start].strip()

LOGO_DEFS = """<defs>
<linearGradient id="lg{sfx}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#f0d060"/>
<stop offset="60%" stop-color="#c8a84b"/>
<stop offset="100%" stop-color="#8b6200"/>
</linearGradient>
</defs>"""

def logo_svg(sfx, w):
    d = LOGO_DEFS.replace("{sfx}", sfx)
    return f'<svg width="{w}" height="{w}" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">{d}<path d="M8 46 A24 24 0 1 1 52 46" stroke="url(#lg{sfx})" stroke-width="3" fill="none" stroke-linecap="round"/><rect x="12" y="34" width="9" height="14" rx="1.5" fill="url(#lg{sfx})"/><rect x="25" y="24" width="9" height="24" rx="1.5" fill="url(#lg{sfx})"/><rect x="38" y="14" width="9" height="34" rx="1.5" fill="url(#lg{sfx})"/></svg>'

BASE_CSS = """:root{--navy:#1a2b3c;--gold:#c8a84b;--bg:#f4f5f0;--card:#fff;--text:#1a2b3c;--muted:#6b7280;--border:#e2e8f0;--radius:10px;--red:#dc2626;--green:#059669}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
#lock{position:fixed;inset:0;background:var(--navy);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:999}
.lk-logo{display:flex;align-items:center;gap:12px;margin-bottom:6px}
.lk-brand{color:var(--gold);font-size:2rem;font-weight:800;letter-spacing:5px}
.lk-sub{color:rgba(255,255,255,.25);font-size:.72rem;letter-spacing:3px;text-transform:uppercase;margin-bottom:34px}
#lock input{width:260px;padding:13px 16px;margin-bottom:8px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:8px;color:#fff;font-size:1rem;text-align:center;letter-spacing:4px;outline:none;transition:border-color .2s}
#lock input:focus{border-color:var(--gold)}
#lock button{width:260px;padding:13px;background:var(--gold);color:var(--navy);border:none;border-radius:8px;font-weight:700;font-size:.9rem;letter-spacing:1.5px;text-transform:uppercase;cursor:pointer}
#lock button:hover{opacity:.88}
.lerr{color:#fc8181;font-size:.8rem;margin-top:8px;min-height:18px}
header{background:var(--navy);padding:14px 32px;display:flex;align-items:center;justify-content:space-between}
.h-logo{display:flex;align-items:center;gap:10px}
.h-brand{color:var(--gold);font-size:1.2rem;font-weight:800;letter-spacing:4px}
.h-brand span{color:rgba(255,255,255,.3);font-weight:300;margin-left:6px;font-size:.95rem}
.h-sub{color:rgba(255,255,255,.25);font-size:.7rem;letter-spacing:2px;text-transform:uppercase}
.tabs{background:var(--navy);border-top:1px solid rgba(255,255,255,.08);display:flex;padding:0 32px}
.tab-btn{padding:11px 20px;color:rgba(255,255,255,.4);font-size:.78rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;cursor:pointer;border:none;background:none;border-bottom:2px solid transparent;transition:all .2s}
.tab-btn:hover{color:rgba(255,255,255,.7)}
.tab-btn.active{color:var(--gold);border-bottom-color:var(--gold)}
.tab-panel{display:none}
.tab-panel.active{display:block}
.mw{max-width:1080px;margin:0 auto;padding:22px 18px}
.two-col{display:grid;grid-template-columns:360px 1fr;gap:18px;align-items:start}
@media(max-width:760px){.two-col{grid-template-columns:1fr}}
.card{background:var(--card);border-radius:var(--radius);padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.07),0 4px 12px rgba(0,0,0,.04);margin-bottom:16px}
.card-title{font-size:.66rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.field{margin-bottom:13px}
.lbl{display:block;font-size:.73rem;font-weight:600;color:var(--muted);letter-spacing:.8px;text-transform:uppercase;margin-bottom:5px}
select,input[type=number]{width:100%;padding:9px 11px;border:1px solid var(--border);border-radius:7px;font-size:.9rem;color:var(--text);background:#fafaf8;outline:none;transition:border-color .2s;appearance:none}
select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='7'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%236b7280' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;padding-right:30px}
select:focus,input:focus{border-color:var(--gold);background:#fff}
.checks{display:flex;flex-direction:column;gap:7px}
.chk{display:flex;align-items:flex-start;gap:8px;font-size:.84rem;cursor:pointer}
.chk input{width:15px;height:15px;accent-color:var(--gold);cursor:pointer;flex-shrink:0;margin-top:2px}
.info-card{display:none;background:#f0f6ff;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;padding:10px 13px;margin-top:8px;font-size:.78rem;color:#1e3a5f;line-height:1.55}
.info-card.visible{display:block}
.ic-title{font-weight:700;font-size:.84rem;color:var(--navy);margin-bottom:4px}
.ic-permit{display:inline-block;background:var(--navy);color:var(--gold);font-size:.62rem;font-weight:700;padding:2px 8px;border-radius:12px;margin:4px 4px 4px 0}
.ic-risk{color:var(--red);font-weight:600;margin-top:5px;font-size:.74rem}
.risk-box{background:#fef2f2;border-left:3px solid var(--red);border-radius:0 7px 7px 0;padding:8px 11px;margin-top:6px;font-size:.74rem;color:#991b1b;line-height:1.5;display:none}
.risk-box.visible{display:block}
.risk-box strong{display:block;color:var(--red);margin-bottom:2px;font-size:.77rem}
.grp-row{display:flex;gap:11px;align-items:center;padding:12px 13px;background:var(--bg);border-radius:8px;margin-bottom:13px}
.grp-badge{background:var(--navy);color:var(--gold);padding:7px 13px;border-radius:6px;font-size:.9rem;font-weight:700;letter-spacing:1px;white-space:nowrap}
.grp-desc{font-size:.79rem;color:var(--muted);line-height:1.4}
.p-empty{text-align:center;padding:26px;color:var(--muted);font-size:.83rem}
.p-box{background:var(--navy);border-radius:8px;padding:15px 17px;margin-bottom:9px}
.p-box-lbl{font-size:.63rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.4);margin-bottom:2px}
.p-box-val{font-size:1.75rem;font-weight:700;color:var(--gold)}
.p-box-note{font-size:.7rem;color:rgba(255,255,255,.25);margin-top:2px}
.p-int{background:#ecfdf5;border-radius:7px;padding:9px 13px;display:flex;justify-content:space-between;align-items:center;font-size:.82rem;color:#065f46;margin-bottom:9px}
.brkd{background:var(--bg);border-radius:7px;padding:10px 12px;font-size:.76rem;color:var(--muted)}
.br{display:flex;justify-content:space-between;padding:2px 0}
.br.tot{font-weight:700;color:var(--text);border-top:1px solid var(--border);margin-top:4px;padding-top:6px}
.hint-box{margin-top:9px;padding:9px 11px;background:#fffbf0;border-radius:7px;border-left:3px solid var(--gold);font-size:.76rem;color:#78350f}
.hint-box strong{color:var(--navy)}
.fp-box{background:linear-gradient(135deg,var(--navy),#2d4a6b);border-radius:10px;padding:18px;text-align:center}
.fp-lbl{font-size:.63rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.45);margin-bottom:4px}
.fp-val{font-size:2rem;font-weight:800;color:var(--gold)}
.fp-int{font-size:.7rem;color:rgba(255,255,255,.3);margin-top:3px}
.fp-note{font-size:.73rem;color:rgba(255,255,255,.55);margin-top:8px;line-height:1.45}
.steps-hdr{font-size:.64rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:12px;padding-bottom:7px;border-bottom:1px solid var(--border)}
.step-c{display:flex;gap:12px;padding:11px 0;border-bottom:1px solid var(--border)}
.step-c:last-child{border-bottom:none}
.sn{width:23px;height:23px;flex-shrink:0;background:var(--gold);color:var(--navy);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:800;margin-top:1px}
.sc-title{font-size:.87rem;font-weight:700;color:var(--navy)}
.sc-price{font-size:.73rem;color:var(--gold);font-weight:700}
.why-box{background:#fffbf0;border-left:2px solid var(--gold);padding:5px 8px;border-radius:0 5px 5px 0;font-size:.73rem;color:#78350f;margin:3px 0;line-height:1.4}
.sc-who{font-size:.7rem;color:var(--muted);margin-top:2px}
.sc-docs{margin-top:4px;font-size:.7rem;color:var(--muted)}
.sc-docs strong{color:var(--text)}
.docs-list{list-style:none}
.docs-list li{font-size:.81rem;padding:6px 0;border-bottom:1px solid var(--border);display:flex;gap:6px}
.docs-list li::before{content:"→";color:var(--gold);font-weight:700;flex-shrink:0}
.docs-list li:last-child{border-bottom:none}
.steps-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:640px){.steps-grid{grid-template-columns:1fr}}
#legalizacija-steps{display:none}
#legalizacija-steps.visible{display:block}"""

AR_FORM = """<div class="mw">
<div class="two-col">
<div>
<div class="card">
<div class="card-title">Ēkas parametri</div>
<div class="field"><label class="lbl">Projekta tips</label>
<select id="ar-type" onchange="calcAR()">
<option value="">— izvēlēties —</option>
<optgroup label="Jauns projekts">
<option value="jaunbuve">Jaunbūve</option>
<option value="izmaiņu">Izmaiņu projekts</option>
<option value="rekonstrukcija">Rekonstrukcija / pārbūve</option>
<option value="vienk">Vienkāršota atjaunošana</option>
<option value="nojaukšana">Nojaukšanas projekts</option>
<option value="tipveida">Tipveida projekts</option>
</optgroup>
<optgroup label="Legalizācija">
<option value="la">Patvaļīga būvniecība</option>
<option value="lbv">Nereģistrētas izmaiņas — vienkāršotas</option>
<option value="lbp">Nereģistrētas izmaiņas — pilnas</option>
<option value="lc">Funkcijas maiņa</option>
</optgroup>
</select>
<div class="info-card" id="ar-info-card"></div>
</div>
<div class="field"><label class="lbl">Platība (m²)</label>
<input type="number" id="ar-area" placeholder="piem. 120" min="1" oninput="calcAR()"></div>
<div class="field"><label class="lbl">Stāvu skaits</label>
<select id="ar-floors" onchange="calcAR()">
<option value="1">1 stāvs</option><option value="2">2 stāvi</option>
<option value="3">3 stāvi</option><option value="4">4+ stāvi</option>
</select></div>
<div class="field"><label class="lbl">Ēkas funkcija</label>
<select id="ar-func" onchange="calcAR()">
<option value="1.00">Individuālā dzīvojamā māja</option>
<option value="1.05">Dvīņu māja</option><option value="1.10">Rindu māja</option>
<option value="1.30">Daudzdzīvokļu māja</option>
<option value="0.85">Vasarnīca / dārza māja</option>
<option value="0.70">Saimniecības ēka</option><option value="0.60">Garāža</option>
<option value="0.65">Noliktava</option><option value="1.20">Biroja ēka</option>
<option value="1.25">Tirdzniecības ēka</option>
<option value="1.15">Jaukta lietojuma ēka</option>
<option value="0.50">Inženierbūve / žogs</option>
</select></div>
<div class="field"><label class="lbl">Pašvaldība</label>
<select id="ar-muni" onchange="calcAR()">
<option value='{"p":1.00,"s":1.10}'>— izvēlēties —</option>
<option value='{"p":1.20,"s":1.05}'>Rīga</option>
<option value='{"p":1.10,"s":1.05}'>Mārupes novads</option>
<option value='{"p":1.10,"s":1.05}'>Ķekavas novads</option>
<option value='{"p":1.10,"s":1.05}'>Salaspils novads</option>
<option value='{"p":1.10,"s":1.05}'>Ādažu / Ropažu / Olaines novads</option>
<option value='{"p":1.10,"s":1.05}'>Stopiņu / Garkalnes / Babītes novads</option>
<option value='{"p":1.00,"s":1.10}'>Jūrmala</option>
<option value='{"p":1.00,"s":1.10}'>Siguldas novads</option>
<option value='{"p":1.00,"s":1.10}'>Jelgava / Jelgavas novads</option>
<option value='{"p":1.00,"s":1.10}'>Ogres novads</option>
<option value='{"p":1.00,"s":1.10}'>Saulkrastu / Limbažu novads</option>
<option value='{"p":1.00,"s":1.10}'>Tukuma / Cēsu novads</option>
<option value='{"p":1.00,"s":1.10}'>Dobeles / Bauskas / Kandavas novads</option>
<option value='{"p":1.02,"s":1.15}'>Valmieras novads</option>
<option value='{"p":1.02,"s":1.15}'>Talsu novads</option>
<option value='{"p":1.02,"s":1.15}'>Saldus / Kuldīgas novads</option>
<option value='{"p":1.02,"s":1.15}'>Jēkabpils / Madonas novads</option>
<option value='{"p":1.05,"s":1.20}'>Liepāja</option>
<option value='{"p":1.05,"s":1.20}'>Ventspils</option>
<option value='{"p":1.05,"s":1.20}'>Daugavpils</option>
<option value='{"p":1.05,"s":1.20}'>Rēzekne</option>
<option value='{"p":1.00,"s":1.10}'>Cits novads</option>
</select></div>
<div class="field"><label class="lbl">Apgrūtinājumi (+10% katrs)</label>
<div class="checks">
<label class="chk"><input type="checkbox" id="c1" onchange="calcAR()"> Kultūras piemineklis / NKMP</label>
<div class="risk-box" id="rb1"><strong>NKMP saskaņošana</strong>Katrai izmaiņai darba uzdevums. Ilgs process. +10% + 2–6 mēneši.</div>
<label class="chk"><input type="checkbox" id="c2" onchange="calcAR()"> Patvaļīga būvniecība / legalizācija</label>
<div class="risk-box" id="rb2"><strong>Legalizācija</strong>RISKS: pašvaldība var atteikt. Bieži 12–36 mēneši.</div>
<label class="chk"><input type="checkbox" id="c3" onchange="calcAR()"> Kopīpašums (līdzīpašnieki)</label>
<div class="risk-box" id="rb3"><strong>Kopīpašums</strong>VISU līdzīpašnieku rakstiska piekrišana obligāta.</div>
<label class="chk"><input type="checkbox" id="c4" onchange="calcAR()"> Ēka robežai tuvāk par 4m</label>
<div class="risk-box" id="rb4"><strong>Robeža &lt;4m</strong>Kaimiņa saskaņojums obligāts. Bez tā — atļauju neizsniedz.</div>
<label class="chk"><input type="checkbox" id="c5" onchange="calcAR()"> Steidzams termiņš</label>
<div class="risk-box" id="rb5"><strong>Steidzamība</strong>Mūsu darbu var paātrināt. Pašvaldības 30 dienas — nemainās.</div>
</div></div>
</div>
</div>
<div>
<div class="card" style="margin-bottom:16px">
<div class="card-title">Būves grupa</div>
<div class="grp-row">
<div class="grp-badge" id="ar-grp-badge">—</div>
<div class="grp-desc" id="ar-grp-desc">Ievadi platību un stāvu skaitu</div>
</div>
</div>
<div class="card">
<div class="card-title">Cenas aprēķins</div>
<div id="ar-p-empty" class="p-empty">🏗 Izvēlies tipu un ievadi platību</div>
<div id="ar-p-result" style="display:none">
<div class="p-box">
<div class="p-box-lbl">Klientam piedāvāt</div>
<div class="p-box-val" id="ar-p-client">—</div>
<div class="p-box-note">bez PVN · ar 20% rezervi tirgošanai</div>
</div>
<div class="p-int"><span>Iekšējā cena (minimums)</span><strong id="ar-p-int">—</strong></div>
<div class="brkd" id="ar-brkd"></div>
<div class="hint-box" id="ar-hint"></div>
</div>
<div id="ar-p-fixed" style="display:none">
<div class="fp-box">
<div class="fp-lbl">Klientam (I grupas mazēka)</div>
<div class="fp-val" id="ar-fp-val">—</div>
<div class="fp-int">Iekšējā: <span id="ar-fp-int">—</span></div>
<div class="fp-note" id="ar-fp-note">—</div>
</div>
</div>
</div>
</div>
</div>
<div style="margin-top:16px">"""

AR_JS_MAIN = r"""
const AR_RATES={jaunbuve:[32,30,28,26,24,22,21,20,19,18,16],"izmaiņu":[22,20,18,16,15,14,13,12,11,10,9],rekonstrukcija:[30,28,26,24,22,20,19,18,17,16,14],vienk:[21,19,17,15,14,13,12,11,10,9,8],"nojaukšana":[10,9,8,7,6,5,5,5,4,4,4],tipveida:[14,12,11,10,9,8,7,6,6,6,5]};
const AR_BRACKS=[30,60,90,120,150,180,210,240,270,300,Infinity];
const AR_MINS={jaunbuve:[1700,2100],"izmaiņu":[1700,2100],rekonstrukcija:[2500,2900],la:[2500,2900],lbp:[2500,2900]};
const GC={I:0.75,II:1.20,III:1.80};
const LEGAL_RATE={la:"rekonstrukcija",lbv:"vienk",lbp:"rekonstrukcija",lc:"rekonstrukcija"};
const LEGAL_SVC={la:{I:[],II:[["ESI",950],["TAA",400],["NOD",950]],III:[["ESI",950],["TAA",400],["NOD",950]]},lbv:{I:[],II:[],III:[]},lbp:{I:[["TAA",400]],II:[["TAA",400],["NOD",950]],III:[["TAA",400],["NOD",950]]},lc:{I:[["ESI",950],["NOD",950]],II:[["ESI",950],["NOD",950]],III:[["ESI",950],["NOD",950]]}};
const I_FIXED=[{max:10,int:667,cli:800},{max:15,int:833,cli:1000},{max:20,int:1000,cli:1200},{max:25,int:1167,cli:1400}];
const SVC_BASE={esi:950,taa:400,nod:950,bk_s:1400,bk_m:2000,bk_l:3000,ti:400,eps:370,elt:350,dv:350};
const TYPE_INFO={jaunbuve:{icon:"🏗",title:"Jaunbūve",what:"Pilnīgi jauna ēka uz brīvas zemes.",permit:"Paskaidrojuma raksts (<200m²) vai Būvatļauja (≥200m²)",time:"6–18 mēneši",risks:"Pārbaudi TIAN — vai zonā drīkst celt! Inženiertīklu pieslēgumi.",tip:"Pirms sāc — pasūti zemes robežu plānu un TIAN no pašvaldības."},"izmaiņu":{icon:"✏️",title:"Izmaiņu projekts",what:"Esošas ēkas daļējas izmaiņas. Apjoms nemainās.",permit:"Paskaidrojuma raksts vai Apliecinājuma karte",time:"3–9 mēneši",risks:"Kultūrvēsturiska ēka → NKMP obligāta!",tip:"Izmanto fasādes atjaunošanai vai logu maiņai."},rekonstrukcija:{icon:"🔨",title:"Rekonstrukcija",what:"Pilna pārbūve — var mainīt apjomu, stāvus, funkciju.",permit:"Būvatļauja (sarežģītākai) vai Paskaidrojuma raksts",time:"6–18 mēneši",risks:"Pārbaudi patvaļīgu būvniecību! Kopīpašumā — visu piekrišana.",tip:"I grupas mazēkā (≤25m²) — rekonstrukcija vienkāršāka."},vienk:{icon:"🎨",title:"Vienkāršota atjaunošana",what:"Fasādes siltināšana, pārplānošana BEZ nesošo konstrukciju skaršanas.",permit:"Paskaidrojuma raksts",time:"2–6 mēneši",risks:"Nedrīkst skart nesošās konstrukcijas!",tip:"Lētākais veids kā legāli uzlabot ēku."},"nojaukšana":{icon:"🏚",title:"Nojaukšanas projekts",what:"Reģistrētas ēkas likumīga nojaukšana.",permit:"Apliecinājuma karte",time:"2–6 mēneši",risks:"Pārbaudi inženiertīklus pirms nojaukšanas!",tip:"Pēc nojaukšanas — obligāti jāatjaunina kadastra dati."},tipveida:{icon:"📋",title:"Tipveida projekts",what:"Atkārtoti izmantojams projekts vairākām ēkām.",permit:"Atkarīgs no ēkas",time:"3–9 mēneši (1.reizei)",risks:"Katrai izmantošanai vajag pielāgojumu.",tip:"Ekonomisks ja plāno vairākas vienādas ēkas."},la:{icon:"⚠️",title:"Legalizācija — Patvaļīga būvniecība",what:"Ēka uzcelta BEZ atļaujas. Dokumentācija jāsakārto PĒC.",permit:"Apliecinājuma karte (I gr.) vai Būvatļauja (II/III gr.)",time:"12–36 mēneši",risks:"RISKS: pašvaldība VAR ATTEIKT — tad ēka jānojauc!",tip:"OBLIGĀTI sāc ar ESI — bez tās var iztērēt 3000€ projektā kas tiks noraidīts."},lbv:{icon:"📝",title:"Legalizācija — Nereģistrētas izmaiņas (vienkāršotas)",what:"Nelielas izmaiņas veiktas, bet BIS nav reģistrētas.",permit:"Paskaidrojuma raksts",time:"2–6 mēneši",risks:"Pārbaudi vai izmaiņas neskar nesošās konstrukcijas.",tip:"Vienkāršākais legalizācijas veids."},lbp:{icon:"🔧",title:"Legalizācija — Nereģistrētas izmaiņas (pilnas)",what:"Nozīmīgas izmaiņas nav reģistrētas BIS.",permit:"Pārbūves atļauja vai Apliecinājuma karte",time:"6–18 mēneši",risks:"TAA var atklāt konstruktīvus trūkumus!",tip:"Atšķirībā no vienkāršotajām — vajag pilnu projektu."},lc:{icon:"🔄",title:"Legalizācija — Funkcijas maiņa",what:"Lietošanas veids mainās (piem. saimniecības → dzīvojamā).",permit:"Pārbūves atļauja ar funkcijas maiņu",time:"9–18 mēneši",risks:"ESI KRITISKA — ja zona neatļauj jauno funkciju, process apstājas!",tip:"Vienmēr sāc ar ESI."}};
const STEPS_DATA={la:{I:[{t:"Uzmērīšana",d:"Precīzi izmēri dokumentiem.",who:"Volko",time:"1–2 ned."},{t:"Apliecinājuma karte (BIS)",d:"Oficiālā atzīšana.",who:"Volko",time:"1–2 mēn."},{t:"Kadastra → ZG",d:"Dati valsts reģistros.",who:"VZD",time:"2–4 ned."}],II:[{t:"ESI — Juridiskā esošās situācijas izpēte",price:"950€",d:"Pārbauda vai legalizācija VAR notikt — zona, robežas, ZG. BEZ ESI var iztērēt 5000€ projektā kas tiks noraidīts.",who:"Volko",time:"2–4 ned.",docs:"Zemesgrāmatas izraksts, kadastra izziņa, robežu plāns"},{t:"TAA — Tehniskā apsekošana",price:"400€",d:"Pārbauda konstruktīvo drošību. BEZ TAA pašvaldība var pieprasīt nojaukšanu.",who:"Volko",time:"1–3 ned.",docs:"Piekļuve ēkai"},{t:"Uzmērīšana un rasējumi",d:"Precīzi plāni, šķērsgriezumi, fasādes.",who:"Volko",time:"2–3 ned."},{t:"AR projekts (legalizācijai)",d:"Oficālā dokumentācija normatīvu atbilstībai.",who:"Volko",time:"3–5 ned."},{t:"BIS iesniegums",d:"Formāls pieteikums. Pašvaldībai 30 darba dienas atbildei.",who:"Volko",time:"1–3 mēn."},{t:"Pašvaldības saskaņošana",d:"Arhitekts izvērtē. Var pieprasīt izmaiņas.",who:"Volko",time:"1–3 mēn."},{t:"NOD — Nodošana ekspluatācijā",price:"950€",d:"BEZ NOD ēka juridiski nepabeigta. Banka nedos kredītu pret šo īpašumu!",who:"Volko",time:"2–4 ned."},{t:"Kadastra → ZG",d:"Dati jāatjaunina visos reģistros.",who:"VZD",time:"2–4 ned."}],III:[{t:"ESI",price:"950€",d:"Detalizēta zona un tiesību analīze.",who:"Volko",time:"3–4 ned.",docs:"ZG, kadastra izziņa"},{t:"TAA",price:"400€",d:"Sarežğīta — sertificēts konstruktors.",who:"Volko",time:"2–4 ned."},{t:"Uzmērīšana",d:"Pilna dokumentācija.",who:"Volko",time:"3–4 ned."},{t:"AR + BK projekts",d:"Obligāti abi III grupai.",who:"Volko",time:"5–8 ned."},{t:"BIS — Būvatļauja",d:"III grupai apliecinājuma karte nav pietiekama.",who:"Volko",time:"2–4 mēn."},{t:"NOD",price:"950€",d:"Pilna komisija.",who:"Volko",time:"3–5 ned."},{t:"Kadastra → ZG",d:"Obligāta.",who:"VZD",time:"3–4 ned."}]},lbv:{I:[{t:"Paskaidrojuma raksts (BIS)",d:"",who:"Volko",time:"2–4 ned."},{t:"Rasējumi — izmainītais stāvoklis",d:"",who:"Volko",time:""},{t:"Kadastra datu atjaunošana",d:"",who:"VZD",time:""}],II:[{t:"Paskaidrojuma raksts (BIS)",d:"",who:"Volko",time:"2–4 ned."},{t:"Rasējumi",d:"",who:"Volko",time:""},{t:"BIS akcepts",d:"",who:"",time:""},{t:"Kadastra atjaunošana",d:"",who:"VZD",time:""}],III:[{t:"TAA",price:"400€",d:"",who:"Volko",time:""},{t:"Rasējumi",d:"Pilna dokumentācija.",who:"Volko",time:""},{t:"BIS — Pārbūves atļauja",d:"",who:"Volko",time:""},{t:"Kadastra",d:"",who:"VZD",time:""}]},lbp:{I:[{t:"TAA",price:"400€",d:"Nesošo konstrukciju pārbaude.",who:"Volko",time:""},{t:"Uzmērīšana",d:"",who:"Volko",time:""},{t:"AR projekts",d:"",who:"Volko",time:""},{t:"BIS — Apliecinājuma karte",d:"",who:"Volko",time:""},{t:"Kadastra",d:"",who:"VZD",time:""}],II:[{t:"TAA",price:"400€",d:"Nesošo konstrukciju pārbaude.",who:"Volko",time:""},{t:"Uzmērīšana",d:"",who:"Volko",time:""},{t:"AR projekts",d:"Izmainītais stāvoklis + normatīvi.",who:"Volko",time:""},{t:"BIS atļauja",d:"",who:"Volko",time:""},{t:"NOD (ja vajag)",price:"950€",d:"",who:"Volko",time:""},{t:"Kadastra",d:"",who:"VZD",time:""}],III:[{t:"TAA",price:"400€",d:"",who:"Volko",time:""},{t:"AR + BK projekts",d:"Obligāti abi.",who:"Volko",time:""},{t:"BIS atļauja",d:"",who:"Volko",time:""},{t:"NOD",price:"950€",d:"",who:"Volko",time:""},{t:"Kadastra",d:"",who:"VZD",time:""}]},lc:{I:[{t:"ESI",price:"950€",d:"Vai zonā ļauj jauno funkciju.",who:"Volko",time:"",docs:"Pašv. TIN, ZG"},{t:"AR projekts",d:"",who:"Volko",time:""},{t:"BIS atļauja",d:"",who:"Volko",time:""},{t:"NOD",price:"950€",d:"",who:"Volko",time:""},{t:"Kadastra → ZG",d:"Bieži vajag notāru.",who:"VZD",time:""}],II:[{t:"ESI",price:"950€",d:"SVARĪGI: vai zonā ļauj jauno funkciju.",who:"Volko",time:"2–4 ned.",docs:"Pašvaldības TIN, ZG izraksts"},{t:"AR projekts (jaunai funkcijai)",d:"Plānojums, sanitārie mezgli, ugunsdrošība, energoefektivitāte.",who:"Volko",time:"4–6 ned."},{t:"BIS atļauja",d:"",who:"Volko",time:""},{t:"NOD",price:"950€",d:"Ar jauno funkciju.",who:"Volko",time:""},{t:"Kadastra → ZG",d:"Bieži vajag notāru.",who:"VZD",time:""}],III:[{t:"ESI",price:"950€",d:"Detalizēta.",who:"Volko",time:""},{t:"AR + BK projekts",d:"",who:"Volko",time:""},{t:"BIS atļauja",d:"",who:"Volko",time:""},{t:"NOD",price:"950€",d:"",who:"Volko",time:""},{t:"Kadastra → ZG",d:"",who:"VZD",time:""}]}};
const DOCS_DATA={la:["Zemesgrāmatas izraksts (zemesgramata.lv)","Kadastra izziņa (kadastrs.lv)","Robežu plāns (VZD)","Pašvaldības TIN","Kaimiņu piekrišana (robeža <4m)","Kopīpašnieku piekrišana (ja ir)","Esošie projekti (ja ir)"],lbv:["Zemesgrāmatas izraksts","Esošie projekti / plāni","Kopīpašnieku piekrišana"],lbp:["Zemesgrāmatas izraksts","Kadastra izziņa","Esošie projekti","Kopīpašnieku piekrišana"],lc:["Zemesgrāmatas izraksts","Kadastra izziņa","Pašvaldības TIN — vai zonā ļauj jauno funkciju","Esošie projekti","Kopīpašnieku piekrišana"]};

function grp(a,f){if(a<=25&&f<=1)return"I";if(a>1500||f>=4)return"III";return"II";}
function bi(a){for(let i=0;i<AR_BRACKS.length;i++)if(a<=AR_BRACKS[i])return i;return AR_BRACKS.length-1;}
function r50(n){return Math.round(n/50)*50;}
function eur(n){return n.toLocaleString("lv-LV")+" EUR";}
function isLegal(t){return["la","lbv","lbp","lc"].includes(t);}

function calcAR(){
  const type=document.getElementById("ar-type").value;
  const area=parseFloat(document.getElementById("ar-area").value)||0;
  const floors=parseInt(document.getElementById("ar-floors").value)||1;
  const fCoef=parseFloat(document.getElementById("ar-func").value)||1;
  let muni={p:1.00,s:1.10};
  try{muni=JSON.parse(document.getElementById("ar-muni").value);}catch(e){}
  const encs=["c1","c2","c3","c4","c5"].filter(id=>document.getElementById(id).checked).length;
  const eCoef=encs>0?+(1+encs*0.10).toFixed(2):1.00;
  ["1","2","3","4","5"].forEach(n=>{const rb=document.getElementById("rb"+n);const cb=document.getElementById("c"+n);if(rb&&cb)rb.classList.toggle("visible",cb.checked);});
  const ic=document.getElementById("ar-info-card");
  if(type&&TYPE_INFO[type]){
    const ti=TYPE_INFO[type];ic.classList.add("visible");
    ic.innerHTML=`<div class="ic-title">${ti.icon} ${ti.title}</div><div>${ti.what}</div><span class="ic-permit">📋 ${ti.permit}</span><span style="display:inline-flex;align-items:center;gap:3px;font-size:.72rem;color:#2563eb;margin-left:6px">⏱ ${ti.time}</span>${ti.risks?`<div class="ic-risk">⚠ ${ti.risks}</div>`:""}${ti.tip?`<div style="margin-top:4px;font-size:.71rem;color:#2563eb">💡 ${ti.tip}</div>`:""}`;
  }else{ic.classList.remove("visible");}
  if(area>0){
    const g=grp(area,floors);document.getElementById("ar-grp-badge").textContent=g+" grupa";
    const gd={I:"≤25m² un 1 stāvs — vienkāršota procedūra (apliecinājuma karte)",II:"26–1500m², līdz 3 stāviem — standarta procedūra",III:">1500m² vai 4+ stāvi — sarežğīta procedūra (būvatļauja)"};
    document.getElementById("ar-grp-desc").textContent=gd[g];
  }else{document.getElementById("ar-grp-badge").textContent="—";document.getElementById("ar-grp-desc").textContent="Ievadi platību un stāvu skaitu";}
  const isLeg=isLegal(type);
  document.getElementById("legalizacija-steps").classList.toggle("visible",isLeg&&area>0);
  if(isLeg&&area>0)renderSteps(type,grp(area,floors),muni.s);
  if(!type||area<=0){
    document.getElementById("ar-p-empty").style.display="block";
    document.getElementById("ar-p-result").style.display="none";
    document.getElementById("ar-p-fixed").style.display="none";
    ["jaunbuve-paketes","legalizacija-paketes","auto-ieteikumi"].forEach(id=>{document.getElementById(id).classList.remove("visible");});
    return;
  }
  const g=grp(area,floors);const gCoef=GC[g];
  if(g==="I"&&!isLeg){
    const fp=I_FIXED.find(x=>area<=x.max)||I_FIXED[I_FIXED.length-1];
    document.getElementById("ar-p-empty").style.display="none";
    document.getElementById("ar-p-result").style.display="none";
    document.getElementById("ar-p-fixed").style.display="block";
    document.getElementById("ar-fp-val").textContent=eur(fp.cli);
    document.getElementById("ar-fp-int").textContent=eur(fp.int);
    document.getElementById("ar-fp-note").textContent="Fiksētā cena I grupas mazēkai (≤25m², 1 stāvs). Iekļauj apliecinājuma karte + uzmērīšana.";
    renderARPanels(type,area,muni.s);return;
  }
  const rKey=isLeg?(LEGAL_RATE[type]||"rekonstrukcija"):type;
  const rates=AR_RATES[rKey];if(!rates)return;
  const rate=rates[bi(area)];
  const base=area*rate*fCoef*gCoef*muni.p*eCoef;
  const minA=AR_MINS[isLeg?type:rKey];
  const minV=minA?(area<=60?minA[0]:minA[1]):0;
  const arInt=r50(Math.max(base,minV));
  const svcs=isLeg?(LEGAL_SVC[type]?.[g]||LEGAL_SVC[type]?.["II"]||[]):[];
  const svcTot=svcs.reduce((acc,s)=>acc+s[1]*muni.s,0);
  const totInt=arInt+svcTot;const totCli=r50(totInt*1.20);
  document.getElementById("ar-p-empty").style.display="none";
  document.getElementById("ar-p-result").style.display="block";
  document.getElementById("ar-p-fixed").style.display="none";
  document.getElementById("ar-p-client").textContent=eur(totCli);
  document.getElementById("ar-p-int").textContent=eur(totInt);
  let bh=`<div class="br"><span>Likme (${rKey})</span><span>${rate} €/m²</span></div><div class="br"><span>Platība</span><span>${area} m²</span></div><div class="br"><span>Funkcija</span><span>×${fCoef.toFixed(2)}</span></div><div class="br"><span>Grupa (${g})</span><span>×${gCoef.toFixed(2)}</span></div><div class="br"><span>Pašvaldība</span><span>×${muni.p.toFixed(2)}</span></div>${encs>0?`<div class="br"><span>Apgrūtinājumi (${encs}×10%)</span><span>×${eCoef.toFixed(2)}</span></div>`:""}<div class="br tot"><span>AR projekts</span><span>${eur(arInt)}</span></div>`;
  if(svcTot>0){svcs.forEach(s=>{bh+=`<div class="br"><span>+ ${s[0]}</span><span>${eur(r50(s[1]*muni.s))}</span></div>`;});bh+=`<div class="br tot"><span>Kopā (iekšējā)</span><span>${eur(totInt)}</span></div>`;}
  document.getElementById("ar-brkd").innerHTML=bh;
  document.getElementById("ar-hint").innerHTML=`<strong>Piedāvājumā:</strong> "no <strong>${totCli.toLocaleString("lv-LV")}</strong> EUR + PVN" <span style="color:#a16207;margin-left:6px">(rezerve: ${eur(totCli-totInt)})</span>`;
  renderARPanels(type,area,muni.s);
}

function renderSteps(type,g,svcCoef){
  const tt={la:"Patvaļīga būvniecība",lbv:"Nereģistrētas izmaiņas (vienkāršotas)",lbp:"Nereģistrētas izmaiņas (pilnas)",lc:"Funkcijas maiņa"};
  document.getElementById("steps-title").textContent=(tt[type]||type)+" · "+g+" grupa";
  const sd=STEPS_DATA[type]?.[g]||STEPS_DATA[type]?.["II"]||[];
  document.getElementById("steps-list").innerHTML=sd.map((s,i)=>`<div class="step-c"><div class="sn">${i+1}</div><div><div class="sc-title">${s.t}${s.price?` <span class="sc-price">${s.price}</span>`:""}</div>${s.d?`<div class="why-box">${s.d}</div>`:""}<div class="sc-who">${s.who?"Veic: "+s.who:""}${s.time?" · "+s.time:""}</div>${s.docs?`<div class="sc-docs"><strong>Klients sagādā:</strong> ${s.docs}</div>`:""}</div></div>`).join("");
  document.getElementById("docs-list").innerHTML=(DOCS_DATA[type]||[]).map(d=>`<li>${d}</li>`).join("");
}
"""

html = f"""<!DOCTYPE html>
<html lang="lv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Volko Engineering — Projektu kalkulators</title>
<style>
{BASE_CSS}
{ar_css}
{bk_css}
</style>
</head>
<body>

<div id="lock">
<div class="lk-logo">
{logo_svg("lk","54")}
<div class="lk-brand">VOLKO</div>
</div>
<div class="lk-sub">Engineering · Projektu kalkulators</div>
<input type="password" id="pi" placeholder="Parole" autocomplete="off">
<button onclick="auth()">Ienākt</button>
<div class="lerr" id="pe"></div>
</div>

<div id="app" style="display:none">
<header>
<div class="h-logo">
{logo_svg("hd","30")}
<div class="h-brand">VOLKO<span>Engineering</span></div>
</div>
<div class="h-sub">Projektu kalkulators</div>
</header>

<div class="tabs">
<button class="tab-btn active" onclick="switchTab('ar',this)">🏗 AR — Arhitektūra</button>
<button class="tab-btn" onclick="switchTab('bk',this)">⚙️ BK — Būvkonstrukcijas</button>
<button class="tab-btn" onclick="switchTab('ai',this)">🤖 AI Konsultants</button>
</div>

<div id="tab-ar" class="tab-panel active">
{AR_FORM}
{ar_panels}
<div id="legalizacija-steps" class="card">
<div class="card-title" id="steps-title">Legalizācijas soļi</div>
<div class="steps-grid">
<div><div class="steps-hdr">Darba secība — solis pa solim</div><div id="steps-list"></div></div>
<div><div class="steps-hdr">Ko klients sagādā</div><ul class="docs-list" id="docs-list"></ul></div>
</div>
</div>
</div>
</div>
</div>

<div id="tab-bk" class="tab-panel">
<div class="mw">
{bk_html}
</div>
</div>

<div id="tab-ai" class="tab-panel">
<div class="mw">
{ai_html}
</div>
</div>

</div>

<script>
const PWD="22!Deamontools";
function auth(){{if(document.getElementById("pi").value===PWD){{document.getElementById("lock").style.display="none";document.getElementById("app").style.display="block";sessionStorage.setItem("va","1");}}else{{document.getElementById("pe").textContent="Nepareiza parole";document.getElementById("pi").value="";}}}}
document.getElementById("pi").addEventListener("keydown",e=>{{if(e.key==="Enter")auth();document.getElementById("pe").textContent="";}});
if(sessionStorage.getItem("va")){{document.getElementById("lock").style.display="none";document.getElementById("app").style.display="block";}}
function switchTab(id,btn){{document.querySelectorAll(".tab-panel").forEach(t=>t.classList.remove("active"));document.querySelectorAll(".tab-btn").forEach(b=>b.classList.remove("active"));document.getElementById("tab-"+id).classList.add("active");btn.classList.add("active");}}
{AR_JS_MAIN}
{ar_js}
{bk_ai_js}
</script>
</body>
</html>"""

out = r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\index.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

lines = html.count('\n')
print(f"Written {len(html)} chars, ~{lines} lines to index.html")
