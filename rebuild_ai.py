"""
Pārtaisa AI no atsevišķas tabas uz floating panel.
1. Noņem AI tabu no navigācijas
2. Noņem tab-ai div
3. Pievieno floating chat pogu un panel
4. Pievieno kontekstuālo AI (zina ko kalkulators rāda)
"""
import re

path = r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\index.html"
with open(path, encoding="utf-8") as f:
    html = f.read()

# 1. Remove AI tab button from navigation
html = html.replace(
    '\n<button class="tab-btn" onclick="switchTab(\'ai\',this)">🤖 AI Konsultants</button>',
    ''
)

# 2. Remove the entire tab-ai div
# Find start and end
ai_start = html.find('<div id="tab-ai"')
if ai_start == -1:
    print("ERROR: tab-ai not found")
else:
    # Find the matching closing div - count nesting
    depth = 0
    i = ai_start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                ai_end = i + 6
                break
        i += 1
    removed = html[ai_start:ai_end]
    print(f"Removing AI tab ({len(removed)} chars)")
    html = html[:ai_start] + html[ai_end:]

# 3. Add floating AI panel HTML right before </div><!-- end app -->
FLOATING_AI_HTML = '''
<!-- ══════════════════════════════════════════════════════════
     FLOATING AI CHAT — pieejams no visām tabām
     ══════════════════════════════════════════════════════════ -->

<!-- Floating button -->
<button id="ai-float-btn" onclick="toggleAIPanel()" title="AI Konsultants" style="
  position:fixed;bottom:24px;right:24px;z-index:500;
  width:58px;height:58px;border-radius:50%;
  background:linear-gradient(135deg,var(--navy),#2d4a6b);
  border:2px solid var(--gold);
  box-shadow:0 4px 20px rgba(0,0,0,.4),0 0 0 0 rgba(200,168,75,.4);
  cursor:pointer;display:flex;align-items:center;justify-content:center;
  font-size:1.4rem;transition:all .2s;
  animation:pulse-ring 2.5s ease-out infinite;
" id="ai-fab">🤖</button>

<!-- Floating panel -->
<div id="ai-panel" style="
  position:fixed;bottom:90px;right:24px;z-index:499;
  width:400px;max-width:calc(100vw - 32px);
  height:580px;max-height:calc(100vh - 110px);
  background:white;border-radius:16px;
  box-shadow:0 20px 60px rgba(0,0,0,.35),0 0 0 1px rgba(200,168,75,.2);
  display:none;flex-direction:column;overflow:hidden;
  transform:translateY(20px) scale(0.96);opacity:0;
  transition:all .25s cubic-bezier(.34,1.56,.64,1);
">
  <!-- Panel header -->
  <div style="
    background:var(--navy);padding:14px 16px;
    display:flex;align-items:center;justify-content:space-between;
    border-radius:16px 16px 0 0;flex-shrink:0;
  ">
    <div style="display:flex;align-items:center;gap:10px">
      <div style="width:36px;height:36px;border-radius:50%;background:rgba(200,168,75,.15);border:1px solid var(--gold);display:flex;align-items:center;justify-content:center;font-size:.95rem">🤖</div>
      <div>
        <div style="color:var(--gold);font-size:.9rem;font-weight:700">AI Konsultants</div>
        <div style="color:rgba(255,255,255,.4);font-size:.65rem;letter-spacing:1px">Powered by Abacus AI</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <div id="ai-ctx-badge" style="display:none;background:rgba(200,168,75,.15);border:1px solid rgba(200,168,75,.3);border-radius:12px;padding:2px 8px;font-size:.6rem;color:var(--gold);font-weight:700;letter-spacing:.5px">📊 KONTEKSTS</div>
      <button onclick="aiClearChat()" style="background:rgba(255,255,255,.08);border:none;border-radius:8px;padding:5px 10px;color:rgba(255,255,255,.5);font-size:.7rem;cursor:pointer;">Notīrīt</button>
      <button onclick="toggleAIPanel()" style="background:rgba(255,255,255,.08);border:none;border-radius:8px;padding:5px 9px;color:rgba(255,255,255,.6);font-size:1rem;cursor:pointer;line-height:1">✕</button>
    </div>
  </div>

  <!-- Context strip (shown when calculator has data) -->
  <div id="ai-ctx-strip" style="display:none;background:#fffbf0;border-bottom:1px solid #fde68a;padding:7px 14px;font-size:.72rem;color:#78350f;flex-shrink:0">
    <span id="ai-ctx-text"></span>
    <button onclick="aiSendContext()" style="margin-left:8px;background:var(--gold);color:var(--navy);border:none;border-radius:8px;padding:2px 9px;font-size:.68rem;font-weight:700;cursor:pointer">Analizē ▶</button>
  </div>

  <!-- Quick buttons -->
  <div style="padding:10px 12px 0;flex-shrink:0;background:#fafaf8;border-bottom:1px solid #f0ede6">
    <div style="display:flex;flex-wrap:wrap;gap:5px;padding-bottom:8px">
      <button class="ai-qbtn" onclick="aiQuick(\'Kur sākt ja gribu celt māju? Izskaidro soli pa solim.\')">🏗 Kā sākt?</button>
      <button class="ai-qbtn" onclick="aiQuick(\'Man ir patvaļīgi celta ēka. Ko darīt — pilns process?\')">⚠️ Patvaļīga ēka</button>
      <button class="ai-qbtn" onclick="aiQuick(\'Kas ir NOD un kāpēc tas vajadzīgs?\')">📋 Kas ir NOD?</button>
      <button class="ai-qbtn" onclick="aiQuick(\'Kāda atļauja vajadzīga manai situācijai?\')">📑 Kāda atļauja?</button>
      <button class="ai-qbtn" onclick="aiQuick(\'Kas ir BIS sistēma un kā tā darbojas?\')">💻 Kas ir BIS?</button>
      <button class="ai-qbtn" onclick="aiQuick(\'Cik maksā legalizācija? Dod orientējošu aprēķinu.\')">💰 Cenas?</button>
      <button class="ai-qbtn" onclick="aiQuick(\'Cik ilgi aizņem büvniecības process?\')">⏱️ Termiņi?</button>
      <button class="ai-qbtn" onclick="aiQuick(\'Kādi dokumenti vajadzīgi no klienta?\')">📁 Dokumenti</button>
    </div>
  </div>

  <!-- Chat messages -->
  <div id="ai-chat-window" style="
    flex:1;overflow-y:auto;padding:14px;
    background:#fafaf8;
    scroll-behavior:smooth;
  "></div>

  <!-- Input -->
  <div style="padding:10px 12px;background:white;border-top:1px solid #e8e4da;flex-shrink:0">
    <div style="display:flex;gap:8px;align-items:flex-end">
      <textarea id="ai-input" rows="1" placeholder="Uzdod jautājumu latviski..." onkeydown="aiKeydown(event)" style="
        flex:1;padding:9px 12px;border:1px solid #e2e8f0;border-radius:10px;
        font-size:.88rem;outline:none;resize:none;height:40px;max-height:100px;
        font-family:inherit;background:#fafaf8;transition:border-color .2s;
      "></textarea>
      <button id="ai-send-btn" onclick="aiSend()" style="
        width:40px;height:40px;flex-shrink:0;
        background:var(--navy);color:var(--gold);
        border:none;border-radius:10px;font-size:1rem;
        cursor:pointer;display:flex;align-items:center;justify-content:center;
        transition:opacity .2s;
      ">▶</button>
    </div>
    <div style="text-align:center;margin-top:5px;font-size:.6rem;color:#bbb">
      Abacus AI · Volko Engineering zināšanu bāze
    </div>
  </div>
</div>

<style>
.ai-qbtn {
  font-size:.68rem;padding:4px 9px;
  background:white;border:1px solid #e2e8f0;
  border-radius:14px;cursor:pointer;color:#374151;
  transition:all .15s;white-space:nowrap;
}
.ai-qbtn:hover { border-color:var(--gold);background:#fffbf0;color:var(--navy); }
.msg { max-width:88%;margin-bottom:10px;line-height:1.55; }
.msg.user {
  margin-left:auto;background:var(--navy);color:white;
  padding:9px 13px;border-radius:14px 14px 3px 14px;font-size:.86rem;
}
.msg.ai {
  background:white;border:1px solid #e8e4da;
  padding:10px 13px;border-radius:14px 14px 14px 3px;
  font-size:.84rem;color:#1a2b3c;
  box-shadow:0 1px 3px rgba(0,0,0,.06);
}
.msg.ai strong { color:var(--navy); }
.msg.error { background:#fff5f5;border:1px solid #fca5a5;padding:9px 12px;border-radius:8px;font-size:.82rem;color:#c00; }
.loading-dots { display:inline-flex;gap:4px;align-items:center;padding:4px 0; }
.loading-dots span { width:6px;height:6px;background:var(--gold);border-radius:50%;animation:bounce 1.1s infinite; }
.loading-dots span:nth-child(2){animation-delay:.18s}
.loading-dots span:nth-child(3){animation-delay:.36s}
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}
@keyframes pulse-ring {
  0% { box-shadow:0 4px 20px rgba(0,0,0,.4),0 0 0 0 rgba(200,168,75,.5); }
  70% { box-shadow:0 4px 20px rgba(0,0,0,.4),0 0 0 12px rgba(200,168,75,0); }
  100% { box-shadow:0 4px 20px rgba(0,0,0,.4),0 0 0 0 rgba(200,168,75,0); }
}
#ai-fab:hover { transform:scale(1.1);box-shadow:0 6px 28px rgba(0,0,0,.5); }
#ai-panel.open {
  display:flex !important;
  transform:translateY(0) scale(1);
  opacity:1;
}
</style>
'''

# Insert before closing </div> of app
app_end = html.rfind('</div>\n\n<script>')
if app_end == -1:
    app_end = html.rfind('</div>')
    print(f"Using fallback app_end at: {app_end}")
else:
    print(f"Found app_end at: {app_end}")

html = html[:app_end] + FLOATING_AI_HTML + '\n' + html[app_end:]

# 4. Update JS: add toggleAIPanel, context reader, update aiClearChat
# Find and update aiClearChat to reset the floating panel
html = html.replace(
    'function aiClearChat() {\n    aiChatHistory = [];\n    const win = document.getElementById(\'ai-chat-window\');\n    win.innerHTML = aiWelcomeMsg();\n}',
    '''function aiClearChat() {
    aiChatHistory = [];
    const win = document.getElementById('ai-chat-window');
    if (win) win.innerHTML = aiWelcomeMsg();
}'''
)

# 5. Add toggleAIPanel and context functions before the 3D init
NEW_JS = '''
// ── FLOATING AI PANEL ─────────────────────────────────────────
let aiPanelOpen = false;

function toggleAIPanel() {
    const panel = document.getElementById('ai-panel');
    aiPanelOpen = !aiPanelOpen;
    if (aiPanelOpen) {
        panel.classList.add('open');
        panel.style.display = 'flex';
        setTimeout(() => {
            panel.style.transform = 'translateY(0) scale(1)';
            panel.style.opacity = '1';
        }, 10);
        // Init welcome if empty
        const win = document.getElementById('ai-chat-window');
        if (win && !win.innerHTML.trim()) win.innerHTML = aiWelcomeMsg();
        // Update context
        updateAIContext();
        // Focus input
        setTimeout(() => { const inp = document.getElementById('ai-input'); if(inp) inp.focus(); }, 300);
    } else {
        panel.style.transform = 'translateY(20px) scale(0.96)';
        panel.style.opacity = '0';
        setTimeout(() => { panel.style.display = 'none'; panel.classList.remove('open'); }, 250);
    }
}

function updateAIContext() {
    // Read current calculator state
    const type = document.getElementById('ar-type') ? document.getElementById('ar-type').value : '';
    const area = document.getElementById('ar-area') ? document.getElementById('ar-area').value : '';
    const muni = document.getElementById('ar-muni') ? document.getElementById('ar-muni').options[document.getElementById('ar-muni').selectedIndex]?.text : '';
    const priceEl = document.getElementById('ar-p-client');
    const price = priceEl ? priceEl.textContent : '';
    const typeNames = {jaunbuve:'Jaunbūve',izmaiņu:'Izmaiņu projekts',rekonstrukcija:'Rekonstrukcija',vienk:'Vienkāršota atjaunošana',nojaukšana:'Nojaukšana',tipveida:'Tipveida',la:'Legalizācija (patvaļīga)',lbv:'Legalizācija (vienkāršotas izm.)',lbp:'Legalizācija (pilnas izm.)',lc:'Funkcijas maiņa'};

    const strip = document.getElementById('ai-ctx-strip');
    const ctxText = document.getElementById('ai-ctx-text');
    const badge = document.getElementById('ai-ctx-badge');

    if (type && area) {
        const typeName = typeNames[type] || type;
        const muniShort = muni && muni !== '— izvēlēties —' ? muni.split(' ')[0] : '';
        const ctx = [typeName, area ? area+'m²' : '', muniShort, price ? '~'+price : ''].filter(Boolean).join(' · ');
        ctxText.textContent = '📊 Kalkulatorā: ' + ctx;
        strip.style.display = 'block';
        badge.style.display = 'block';
        // Save context for AI
        window._aiCurrentContext = `Klients kalkulatorā ir ievadījis: Tips=${typeName}, Platība=${area}m², Pašvaldība=${muniShort || 'nav izvēlēta'}, Aprēķinātā cena klientam=${price || 'nav aprēķināta'}. Atbildi kontekstuāli par šo projektu.`;
    } else {
        strip.style.display = 'none';
        badge.style.display = 'none';
        window._aiCurrentContext = '';
    }
}

function aiSendContext() {
    if (window._aiCurrentContext) {
        if (!aiPanelOpen) toggleAIPanel();
        aiQuick('Pamatojoties uz kalkulatora datiem — ' + window._aiCurrentContext.replace('Klients kalkulatorā ir ievadījis: ','') + ' — izskaidro nākamos soļus un vai cena ir adekvāta.');
    }
}

// Update context when calculator changes
document.addEventListener('change', () => { if(aiPanelOpen) updateAIContext(); });
document.addEventListener('input', () => { if(aiPanelOpen) updateAIContext(); });

'''

# Insert NEW_JS before the 3D init comment
marker = '// ══════════════════════════════════════════════════════════════\n// THREE.JS'
html = html.replace(marker, NEW_JS + marker)

# 6. Update AI_SYSTEM to add context instruction
html = html.replace(
    'JAUTĀ ja nezini — labāk atzīt nezināšanu nekā sniegt neprecīzu info.`;',
    '''JAUTĀ ja nezini — labāk atzīt nezināšanu nekā sniegt neprecīzu info.

KONTEKSTUĀLĀ APZINĀŠANĀS: Ja ziņojumā ir "kalkulatora dati" vai specifiskas vērtības (tips, platība, pašvaldība, cena) — izmanto tos lai dotu personalizētu padomu. Piemēram, ja tips=Legalizācija un platība=120m² un pašvaldība=Rīga, tad aprēķini konkrētas izmaksas un izskaidro tieši šo gadījumu.`;'''
)

# Write
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done! File: {len(html)} chars")

# Syntax check
import subprocess, sys, tempfile, os
scriptStart = html.find("<script>") + 8
scriptEnd = html.rfind("</script>")
js = html[scriptStart:scriptEnd]
tmp = os.path.join(tempfile.gettempdir(), "volko_rebuild_check.js")
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(js)
result = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
if result.returncode == 0:
    print("✓ JS syntax OK")
else:
    print("✗ JS syntax ERROR:", result.stderr[:500])
