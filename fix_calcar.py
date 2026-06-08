"""
1. Noņem duplicate calcAR + cirkulāro _origCalcAR
2. Iebūvē showMuniInfo + showPreChecklist tieši oriģinālajā calcAR
3. Uzlabo papildu pakalpojumu UI
"""
import re, subprocess, tempfile, os

path = r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\index.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# ── 1. Remove the bad calcAR override (circular reference) ────
bad_block = r"""// Hook into existing calcAR to call showMuniInfo and showPreChecklist
const _origCalcAR = calcAR;
function calcAR() {
  _origCalcAR();
  const muniVal = document.getElementById('ar-muni') ? document.getElementById('ar-muni').value : '';
  const typeVal = document.getElementById('ar-type') ? document.getElementById('ar-type').value : '';
  showMuniInfo(muniVal);
  showPreChecklist(typeVal);
}"""
if bad_block in html:
    html = html.replace(bad_block, "// showMuniInfo + showPreChecklist called directly from calcAR below")
    print("✓ Removed bad calcAR override")
else:
    print("WARNING: bad block not found exactly — trying regex")
    html = re.sub(
        r"// Hook into existing calcAR.*?function calcAR\(\) \{.*?showPreChecklist\(typeVal\);\s*\}",
        "// showMuniInfo + showPreChecklist called directly from calcAR below",
        html, flags=re.DOTALL
    )
    print("✓ Removed via regex")

# ── 2. Add showMuniInfo + showPreChecklist calls inside the real calcAR ──
# Find the end of calcAR (before renderARPanels call at the end)
# We'll add the calls right before the final renderARPanels call
old_render_line = "  renderARPanels(type,area,muni.s);\n  const _mname = document.getElementById(\"ar-muni\").options[document.getElementById(\"ar-muni\").selectedIndex]?.text || \"\";\n  renderPassport(type,area,floors,_mname,muni.s);\n}"
new_render_line = """  renderARPanels(type,area,muni.s);
  const _mname = document.getElementById("ar-muni").options[document.getElementById("ar-muni").selectedIndex]?.text || "";
  renderPassport(type,area,floors,_mname,muni.s);
  // Municipality info + pre-checklist
  if(typeof showMuniInfo==="function") showMuniInfo(document.getElementById("ar-muni").value);
  if(typeof showPreChecklist==="function") showPreChecklist(type);
}"""
if old_render_line in html:
    html = html.replace(old_render_line, new_render_line)
    print("✓ showMuniInfo/showPreChecklist added to calcAR")
else:
    print("WARNING: render line not found — trying alternative")
    # Try to find and patch the end of calcAR differently
    old2 = "  renderARPanels(type,area,muni.s);\n}"
    new2 = """  renderARPanels(type,area,muni.s);
  if(typeof showMuniInfo==="function") showMuniInfo(document.getElementById("ar-muni")?.value||"");
  if(typeof showPreChecklist==="function") showPreChecklist(type);
}"""
    if old2 in html:
        html = html.replace(old2, new2)
        print("✓ showMuniInfo/showPreChecklist added (alt)")

# ── 3. Also fix the hidden state to call these functions ────
# When no type/area selected, hide the panels properly
old_hide = '    const _pp=document.getElementById("ar-passport");if(_pp)_pp.classList.remove("visible");\n    return;\n  }'
new_hide = '''    const _pp=document.getElementById("ar-passport");if(_pp)_pp.classList.remove("visible");
    if(typeof showMuniInfo==="function") showMuniInfo(document.getElementById("ar-muni")?.value||"");
    if(typeof showPreChecklist==="function") showPreChecklist(type);
    return;
  }'''
if old_hide in html:
    html = html.replace(old_hide, new_hide)
    print("✓ Hide state also calls muni+checklist")

# ── 4. Improve papildu pakalpojumi section CSS and HTML ──────
BETTER_REC_CSS = """
/* Improved recommendations section */
#auto-ieteikumi { display:none }
#auto-ieteikumi.visible { display:block }
.rec-section-header {
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:12px;
}
.rec-section-title { font-size:.88rem;font-weight:700;color:var(--navy) }
.rec-section-sub { font-size:.72rem;color:var(--muted) }

/* Better rec item */
.rec-item {
  border:1.5px solid var(--border);border-radius:8px;
  padding:10px 13px;margin-bottom:7px;
  display:grid;grid-template-columns:20px 1fr auto;
  gap:10px;align-items:flex-start;
  transition:all .15s;cursor:pointer;
}
.rec-item:hover { border-color:var(--gold);background:#fffbf0; }
.rec-item.critical { border-color:#fca5a5;background:#fff7f7; }
.rec-item.recommended { border-color:#fde68a;background:#fffdf7; }
.rec-item.selected { border-color:var(--navy);background:#f0f4ff; }

.rec-cb { margin-top:2px;width:15px;height:15px;accent-color:var(--navy);cursor:pointer;flex-shrink:0 }
.rec-body {}
.rec-name { font-size:.84rem;font-weight:700;color:var(--navy);margin-bottom:2px }
.rec-why-text { font-size:.72rem;color:var(--muted);line-height:1.4 }
.rec-when-text { font-size:.66rem;color:var(--muted);margin-top:2px;font-style:italic }
.rec-price-col { text-align:right;white-space:nowrap;flex-shrink:0 }
.rec-price-eur { font-size:.82rem;font-weight:700;color:var(--navy) }
.rec-price-note { font-size:.62rem;color:var(--muted) }

.rec-urgency-badge {
  display:inline-flex;align-items:center;gap:3px;
  font-size:.6rem;font-weight:700;letter-spacing:.5px;
  text-transform:uppercase;padding:1px 7px;border-radius:10px;
  margin-bottom:3px;
}
.urg-critical { background:#fee2e2;color:#991b1b }
.urg-recommended { background:#fef9c3;color:#713f12 }
.urg-if_needed { background:#f3f4f6;color:var(--muted) }

.rec-total-bar {
  background:linear-gradient(135deg,var(--navy),#2d4a6b);
  border-radius:8px;padding:11px 15px;
  display:flex;justify-content:space-between;align-items:center;
  margin-top:12px;
}
.rec-total-label { font-size:.65rem;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.4) }
.rec-total-int { font-size:.78rem;color:rgba(255,255,255,.5) }
.rec-total-cli { font-size:1.05rem;font-weight:700;color:var(--gold) }
.rec-total-note { font-size:.62rem;color:rgba(255,255,255,.3);margin-top:2px }
"""
html = html.replace("</style>\n</head>", BETTER_REC_CSS + "</style>\n</head>", 1)
print("✓ Better rec CSS added")

# ── 5. Replace renderRecs function with better version ────────
OLD_RENDER_RECS = """function renderRecs(recs,area,svcCoef){
  const groups={critical:[],recommended:[],if_needed:[]};
  recs.forEach(r=>{if(groups[r.urgency])groups[r.urgency].push(r);});
  Object.entries(groups).forEach(([urg,items])=>{
    const grpEl=document.getElementById("urg-"+urg);
    const listEl=document.getElementById("urg-"+urg+"-list");
    if(!items.length){grpEl.style.display="none";return;}
    grpEl.style.display="block";
    listEl.innerHTML=items.map(item=>{
      const price=item.priceFn?item.priceFn(area,svcCoef):0;
      const chk=urg==="critical"?"checked":"";
      return`<div class="rec-item ${urg}"><input type="checkbox" class="rec-cb" ${chk} data-price="${price}" onchange="updRecTot()"><div><div class="rec-name">${item.name}<span class="iw"><span class="ii">?</span><span class="tb">${item.why}</span></span></div><div class="rec-price">${price>0?eur(price)+" + PVN":"pēc aprēķina"}</div><div class="rec-why">${item.why}</div><div class="rec-when"><strong>Kad:</strong> ${item.when_required}</div></div></div>`;
    }).join("");
  });
  updRecTot();
}"""

NEW_RENDER_RECS = """function renderRecs(recs,area,svcCoef){
  // Flatten all recs sorted: critical first, recommended second, if_needed last
  const urgOrder={critical:0,recommended:1,if_needed:2};
  const sorted=[...recs].sort((a,b)=>urgOrder[a.urgency]-urgOrder[b.urgency]);

  const urgLabels={
    critical:'<span class="rec-urgency-badge urg-critical">🔴 KRITISKI</span>',
    recommended:'<span class="rec-urgency-badge urg-recommended">⭐ IETEICAMS</span>',
    if_needed:'<span class="rec-urgency-badge urg-if_needed">○ Ja attiecas</span>'
  };

  // Show all groups if they have items
  ["critical","recommended","if_needed"].forEach(urg=>{
    const grpEl=document.getElementById("urg-"+urg);
    const items=sorted.filter(r=>r.urgency===urg);
    if(!items.length){grpEl.style.display="none";return;}
    grpEl.style.display="block";
    const listEl=document.getElementById("urg-"+urg+"-list");
    listEl.innerHTML=items.map(item=>{
      const price=item.priceFn?item.priceFn(area,svcCoef):0;
      const autoCheck=urg==="critical"?"checked":"";
      const priceHtml=price>0
        ?`<div class="rec-price-eur">${price.toLocaleString("lv-LV")} EUR</div><div class="rec-price-note">+ PVN · klientam</div>`
        :`<div class="rec-price-note">pēc aprēķina</div>`;
      return`<label class="rec-item ${urg}" onclick="">
        <input type="checkbox" class="rec-cb" ${autoCheck} data-price="${price}" onchange="updRecTot()">
        <div class="rec-body">
          ${urgLabels[urg]}
          <div class="rec-name">${item.name}</div>
          <div class="rec-why-text">${item.why}</div>
          <div class="rec-when-text">📋 ${item.when_required}</div>
        </div>
        <div class="rec-price-col">${priceHtml}</div>
      </label>`;
    }).join("");
  });
  updRecTot();
}"""

if OLD_RENDER_RECS in html:
    html = html.replace(OLD_RENDER_RECS, NEW_RENDER_RECS)
    print("✓ renderRecs improved")
else:
    print("WARNING: renderRecs not found exactly")

# ── 6. Replace updRecTot with better version ─────────────────
OLD_REC_TOT = """function updRecTot(){
  let t=0;
  document.querySelectorAll(".rec-cb:checked").forEach(cb=>{t+=parseInt(cb.dataset.price)||0;});
  document.getElementById("rec-total").textContent=eur(t);
}"""

NEW_REC_TOT = """function updRecTot(){
  let totInt=0,totCli=0;
  document.querySelectorAll(".rec-cb:checked").forEach(cb=>{
    const p=parseInt(cb.dataset.price)||0;
    totInt+=p;
    totCli+=Math.round(p*1.20/50)*50;
  });
  const el=document.getElementById("rec-total");
  if(el) el.textContent=eur(totCli);
  // Update total bar
  const bar=document.getElementById("rec-total-bar");
  if(!bar) return;
  if(totInt>0){
    bar.style.display="flex";
    const intEl=document.getElementById("rec-bar-int");
    const cliEl=document.getElementById("rec-bar-cli");
    if(intEl) intEl.textContent=eur(totInt);
    if(cliEl) cliEl.textContent=eur(totCli);
  } else {
    bar.style.display="none";
  }
}"""

if OLD_REC_TOT in html:
    html = html.replace(OLD_REC_TOT, NEW_REC_TOT)
    print("✓ updRecTot improved")

# ── 7. Update the auto-ieteikumi HTML section ────────────────
OLD_REC_HTML = """  <div class="rec-tot">
      <div class="rec-tot-lbl">Papildu pakalpojumi (klientam)</div>
      <div class="rec-tot-val" id="rec-total">0 EUR</div>
    </div>"""

NEW_REC_HTML = """  <div id="rec-total-bar" class="rec-total-bar" style="display:none">
      <div>
        <div class="rec-total-label">Papildu pakalpojumi</div>
        <div class="rec-total-int">Iekšējā: <span id="rec-bar-int">0 EUR</span></div>
      </div>
      <div style="text-align:right">
        <div class="rec-total-cli" id="rec-bar-cli">0 EUR</div>
        <div class="rec-total-note">klientam + PVN</div>
      </div>
    </div>
    <div style="display:none"><span id="rec-total">0 EUR</span></div>"""

if OLD_REC_HTML in html:
    html = html.replace(OLD_REC_HTML, NEW_REC_HTML)
    print("✓ rec-total HTML improved")

# ── 8. Add section header to auto-ieteikumi ──────────────────
OLD_AUTOI_HEADER = """  <div class="card-title">Ieteicamie papildu pakalpojumi</div>
    <p style="font-size:.78rem;color:var(--muted);margin-bottom:14px">Izvēlies ko iekļaut piedāvājumā. Cenas ar pašvaldības koef. un 20% rezervi.</p>"""

NEW_AUTOI_HEADER = """  <div class="rec-section-header">
      <div>
        <div class="card-title" style="margin-bottom:2px">Papildu pakalpojumi</div>
        <div class="rec-section-sub">Atzīmē ko iekļaut piedāvājumā · Cenas klientam (ar 20%)</div>
      </div>
    </div>"""

if OLD_AUTOI_HEADER in html:
    html = html.replace(OLD_AUTOI_HEADER, NEW_AUTOI_HEADER)
    print("✓ auto-ieteikumi header improved")

# ── Write + syntax check ──────────────────────────────────────
with open(path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\nFile written: {len(html)} chars")

scriptStart = html.find("<script>") + 8
scriptEnd = html.rfind("</script>")
js = html[scriptStart:scriptEnd]
tmp = os.path.join(tempfile.gettempdir(), "volko_fix.js")
with open(tmp, "w", encoding="utf-8") as f:
    f.write(js)
result = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
if result.returncode == 0:
    print("✓ JS syntax OK")
else:
    print("✗ JS ERROR:", result.stderr[:500])

# Also verify calcAR count is now 1
count = js.count("function calcAR()")
print(f"calcAR() declarations: {count} (should be 1)")
