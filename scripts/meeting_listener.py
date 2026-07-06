# -*- coding: utf-8 -*-
"""
Volko kalkulatora TIKŠANĀS KLAUSĪTĀJS — klausās sarunu, atzīmē čeklistu un baro
kalkulatora paneli (http://127.0.0.1:8766/state). AUDIO NETIEK GLABĀTS.

Kodols pārmantots no volko-konsultacija/consult_listen.py (Groq Whisper LV,
15 punktu čeklists) — šis pievieno lokālu HTTP serveri, ko lasa kalkulators.

Lietošana:
  python meeting_listener.py            # klausās mikrofonu (Ctrl+C beidz)
  python meeting_listener.py --demo     # BEZ mikrofona — izspēlē sarunu (UI testiem)
  python meeting_listener.py --test     # 5 s mikrofona pārbaude
Apturēšana: Ctrl+C · kalkulatora poga "Beigt" (POST /stop) · STOP fails izvades mapē.

Beigās izvades mapē: transcript_live.txt + celists_final.txt (kā konsultāciju skillā).
"""
import argparse, json, os, re, sys, tempfile, threading, time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# kodols no volko-konsultacija (abi PC: tas pats ceļš caur %USERPROFILE%)
_SK = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive - VolkoEngineering",
                   "claude-skills", "volko-konsultacija", "scripts")
sys.path.insert(0, _SK)
from consult_listen import CHECKLIST, load_groq_key, strip_diac, transcribe, record_chunk, save_wav  # noqa: E402

PORT = 8766

# Beigu atgādinājumi — rāda VIENMĒR pie "Tikšanās beigas" (neatkarīgi no čeklista)
BEIGU_ATGADINAJUMI = [
    "💶 Konsultācijas maksa 50 € + PVN — pasaki klientam un izraksti rēķinu",
    "📅 Vienojies par nākamo soli UN termiņu (kad būs piedāvājums)",
    "📄 Pasaki, kādus dokumentus klients atsūta (zemesgrāmata, plāni, pilnvara)",
    "📇 Pārbaudi klienta e-pastu un tālruni (pa burtiem — Pipedrive ierakstam)",
]

STATE_LOCK = threading.Lock()
STATE = {"klausas": False, "demo": False, "atjaunots": "", "gabali": 0,
         "atzimets": {}, "trukst": [lbl for _, lbl, _ in CHECKLIST],
         "pedejais": "", "beigu_atgadinajumi": BEIGU_ATGADINAJUMI}
STOP_FLAG = {"stop": False}


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        if self.path.startswith("/state"):
            with STATE_LOCK:
                body = json.dumps(STATE, ensure_ascii=False).encode("utf-8")
            self.send_response(200); self._cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers(); self.wfile.write(body)
        else:
            self.send_response(404); self._cors(); self.end_headers()

    def do_POST(self):
        if self.path.startswith("/stop"):
            STOP_FLAG["stop"] = True
            self.send_response(200); self._cors(); self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404); self._cors(); self.end_headers()

    def log_message(self, *a):  # klusē
        pass


DEMO_LINES = [
    "Labdien, runāsim par māju Priežu ielā divi Mārupē.",
    "Tā ir divstāvu dzīvojamā māja, kopā apmēram simts astoņdesmit kvadrātmetri.",
    "Piebūve uzcelta bez atļaujas, gribam legalizēt, jo banka prasa sakārtot.",
    "Zemesgrāmatā ēka ir ierakstīta, kadastra numurs man ir līdzi papīros.",
    "Mērķis ir refinansēt kredītu un varbūt pēc gada pārdot.",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--chunk", type=int, default=40)
    ap.add_argument("--device", type=int, default=None)
    ap.add_argument("--silence", type=int, default=250)
    ap.add_argument("--demo", action="store_true", help="bez mikrofona — izspēlē sarunu (UI testiem)")
    ap.add_argument("--test", action="store_true", help="5 s mikrofona pārbaude")
    a = ap.parse_args()

    key = None
    if not a.demo:
        key = load_groq_key()
        if not key:
            print("GROQ_API_KEY_MISSING — ievieto volko-shared/scripts/.env.local", file=sys.stderr)
            sys.exit(2)

    out = a.out or os.path.join(os.environ.get("USERPROFILE", "."), "Downloads",
                                "tiksanas_" + datetime.now().strftime("%Y%m%d_%H%M"))
    os.makedirs(out, exist_ok=True)
    t_path = os.path.join(out, "transcript_live.txt")
    stop_path = os.path.join(out, "STOP")

    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"🎙  Klausītājs gatavs · kalkulatora panelis: http://127.0.0.1:{PORT}/state · izvade: {out}")
    if a.demo:
        print("    DEMO režīms — mikrofons netiek lietots.")

    state_local = {k: None for k, _, _ in CHECKLIST}
    full_norm = ""
    chunks = 0

    def publish(text_tail=""):
        with STATE_LOCK:
            STATE["klausas"] = not STOP_FLAG["stop"]
            STATE["demo"] = a.demo
            STATE["atjaunots"] = datetime.now().strftime("%H:%M:%S")
            STATE["gabali"] = chunks
            STATE["atzimets"] = {lbl: state_local[k] for k, lbl, _ in CHECKLIST if state_local[k]}
            STATE["trukst"] = [lbl for k, lbl, _ in CHECKLIST if not state_local[k]]
            if text_tail:
                STATE["pedejais"] = text_tail[-220:]

    def absorb(text, ts):
        nonlocal full_norm
        if not text:
            return
        with open(t_path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {text}\n")
        full_norm += " " + strip_diac(text)
        for k, lbl, pat in CHECKLIST:
            if not state_local[k] and re.search(pat, full_norm):
                state_local[k] = ts
                print(f"   ✅ {lbl}")
        publish(text)

    publish()
    try:
        if a.demo:
            i = 0
            while not STOP_FLAG["stop"] and not os.path.exists(stop_path):
                ts = datetime.now().strftime("%H:%M")
                absorb(DEMO_LINES[i % len(DEMO_LINES)], ts)
                chunks += 1; i += 1
                for _ in range(40):  # ~4 s, bet ātri reaģē uz stop
                    if STOP_FLAG["stop"]: break
                    time.sleep(0.1)
        else:
            chunk_len = 5 if a.test else a.chunk
            while not STOP_FLAG["stop"] and not os.path.exists(stop_path):
                buf, peak = record_chunk(chunk_len, a.device)
                chunks += 1
                ts = datetime.now().strftime("%H:%M")
                if peak < a.silence and not a.test:
                    publish(); continue
                tmp = tempfile.mktemp(suffix=".wav")
                save_wav(buf, tmp)
                try:
                    text = transcribe(tmp, key)
                finally:
                    try: os.remove(tmp)      # AUDIO NEGLABĀ
                    except OSError: pass
                absorb(text, ts)
                if a.test:
                    print("TESTS OK:", text or "(klusums)"); break
    except KeyboardInterrupt:
        print("\nApturēts.")

    STOP_FLAG["stop"] = True
    publish()
    missing = [lbl for k, lbl, _ in CHECKLIST if not state_local[k]]
    with open(os.path.join(out, "celists_final.txt"), "w", encoding="utf-8") as f:
        f.write("TIKŠANĀS ČEKLISTA GALA ATSKAITE — " + datetime.now().strftime("%d.%m.%Y %H:%M") + "\n\n")
        f.write("IZSKANĒJA:\n")
        for k, lbl, _ in CHECKLIST:
            if state_local[k]:
                f.write(f"  ✅ {lbl} (no {state_local[k]})\n")
        f.write("\n❗ NEIZSKANĒJA:\n" + "".join(f"  ❌ {m}\n" for m in missing))
        f.write("\nBEIGU ATGĀDINĀJUMI:\n" + "".join(f"  • {r}\n" for r in BEIGU_ATGADINAJUMI))
    print("Gala atskaite:", os.path.join(out, "celists_final.txt"))
    time.sleep(1.5)   # ļauj panelim nolasīt pēdējo stāvokli
    srv.shutdown()


if __name__ == "__main__":
    main()
