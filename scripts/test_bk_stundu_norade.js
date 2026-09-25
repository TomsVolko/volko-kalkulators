// BK stundu darbs: kalkulatorā tikai NORĀDE uz Raita kalkulatoru v1.1, bez skaitļa
// (Vladimira lēmums 25.09.2026, TW #36435966). Palaišana: node scripts/test_bk_stundu_norade.js
const fs = require("fs");
const path = require("path");
const t = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
let kludas = 0;
function prasa(nos, ok) { console.log((ok ? "OK    " : "KRITA ") + nos); if (!ok) kludas++; }

const m = t.match(/const BK_STUNDAS_NORADE="([^"]*)";/);
prasa("norāde definēta", !!m);
const norade = m ? m[1] : "";
prasa("norāde sauc Raita kalkulatoru v1.1", norade.includes("Raita kalkulatorā v1.1"));
prasa("norādē NAV skaitļa ar EUR/h", !/\d+\s*(EUR|€)\s*\/\s*h/i.test(norade));
prasa("norāde abās BK rindās (dzīvoklis + ēka)", (t.match(/\+BK_STUNDAS_NORADE\}/g) || []).length === 2);
const slikti = t.split(/\r?\n/).filter(r => /\bBK\b/.test(r) && /\b(20|30)\s*(EUR|€)\s*\/\s*h/i.test(r));
prasa("index.html BK kontekstā nav 20/30 EUR/h (" + slikti.length + ")", slikti.length === 0);
console.log(kludas ? "\n" + kludas + " KLUDAS" : "\nOK (0 kludas)");
process.exit(kludas ? 1 : 0);
