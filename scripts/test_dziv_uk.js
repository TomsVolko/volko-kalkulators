// ŪK rinda dzīvokļa pārplānošanai — darbina ĪSTO svcList() no index.html (ne kopiju).
// TW #36442653: Vladimirs 24.09.2026 prasīja ŪK opcijai «orientējošu cenu no kalkulatora»,
// bet cenas lēmuma vēl nav. Tāpēc: rinda IR, cena NAV izdomāta (UK_APT = null → «JĀIZLEMJ
// TOMAM»), un kopsummā tā neieskaitās kā 0 EUR, kas izskatītos pēc cenas.
// Palaišana:  node scripts/test_dziv_uk.js      (exit 0 = OK, 1 = regresija)
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");

function nem(re, nosaukums) {
  const m = html.match(re);
  if (!m) { console.error("  KRĪT  index.html nav atrasts: " + nosaukums); process.exit(1); }
  return m[0];
}
const avots = {
  APT: nem(/const APT_BASE=[^;]*;/, "APT_BASE/APT_SKICE"),
  UK: nem(/const UK_APT=[^;]*;/, "UK_APT"),
  SVC_BASE: nem(/const SVC_BASE=\{[^}]*\};/, "SVC_BASE"),
  XL: nem(/const BK_XL_NO=[^;]*;/, "BK_XL_NO/M2/MAX"),
  CAP: nem(/const BK_XL_CAP=[^;]*;/, "BK_XL_CAP"),
  bkCena: nem(/function bkCena\(a\)\{[\s\S]*?\n\}/, "bkCena()"),
  r50: nem(/function r50\(n\)\{[^}]*\}/, "r50()"),
  eur: nem(/function eur\(n\)\{[^}]*\}/, "eur()"),
  grp: nem(/function grp\(a,f,cat\)\{[\s\S]*?\n\}/, "grp()"),
  TIPI: nem(/const TIPI=\[[\s\S]*?\n\];/, "TIPI"),
  svcList: nem(/function svcList\(mainE\)\{[\s\S]*?\n\}/, "svcList()"),
};

function ielade(uk) {
  const kods = [avots.APT, uk, avots.SVC_BASE, avots.XL, avots.CAP, avots.bkCena, avots.r50, avots.eur,
    avots.grp, avots.TIPI, avots.svcList,
    "var darb='parbuve'; var muni={s:1};",
    "var document={getElementById:function(){return {checked:false};}};",
    "function docFor(){return {dt:'pr',ref:'',why:''};}",           // ne-dzīvokļa zaram vajag tikai dt
    "this.o={svcList,TIPI,APT_BASE,APT_SKICE,UK_APT};"].join("\n");
  const ctx = {};
  vm.runInNewContext(kods, ctx);
  return ctx.o;
}

let kritumi = 0;
function t(nos, ok, papildus) {
  console.log((ok ? "  OK    " : "  KRĪT  ") + nos + (ok ? "" : "  :: " + (papildus || "")));
  if (!ok) kritumi++;
}

// ── 0. Visa lapa kompilējas (sintakses kļūda salauztu VISU kalkulatoru) ──
const skripti = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let sintakse = null;
for (const s of skripti) { try { new vm.Script(s); } catch (e) { sintakse = e.message; break; } }
t("visi iekšējie <script> bloki kompilējas (" + skripti.length + ")", sintakse === null, sintakse);

const k = ielade(avots.UK);
const DZ = k.TIPI.findIndex(x => x.cat === "apartment");
const MAJA = k.TIPI.findIndex(x => x.n === "Individuālā dzīvojamā māja");
const dz = k.svcList({ tips: DZ, platiba: "60", stavi: "1" });
const uk = dz.find(s => s.id === "uk");

// ── 1. Vietturis, ne izdomāta cena ──
t("UK_APT = null (cena nav izdomāta)", k.UK_APT === null, String(k.UK_APT));
t("dzīvoklim ir ŪK rinda, NOSACĪTI (st cond)", !!uk && uk.st === "cond", JSON.stringify(uk));
t("rinda atzīmēta jaizlemj + teksts «JĀIZLEMJ TOMAM» + TW numurs",
  !!uk && uk.jaizlemj === true && uk.w.includes("JĀIZLEMJ TOMAM") && uk.w.includes("36442653"));
t("vietturim p = 0 (summā nekas netiek pieskaitīts)", !!uk && uk.p === 0);

// ── 2. Nekas cits nemainās ──
t("dzīvokļa pārējās rindas un statusi tie paši (taa cond, bk cond, eps no, ti no)",
  JSON.stringify(dz.filter(s => s.id !== "uk").map(s => s.id + ":" + s.st)) ===
  JSON.stringify(["taa:cond", "bk:cond", "eps:no", "ti:no"]));
t("ēkai (ne dzīvoklim) ŪK rindas NAV", !k.svcList({ tips: MAJA, platiba: "150", stavi: "2" }).some(s => s.id === "uk"));
t("dzīvokļa bāze bez ŪK nemainās: 450 / ar skici 950", k.APT_BASE === 450 && k.APT_SKICE === 950);

// ── 3. MUTĀCIJA: kad Toms ieliks skaitli, vietturis pazūd un cena ir tieši tā ──
const km = ielade("const UK_APT=500;");
const ukm = km.svcList({ tips: DZ, platiba: "60", stavi: "1" }).find(s => s.id === "uk");
t("MUTĀCIJA: UK_APT=500 → jaizlemj false, p 500, teksts bez «JĀIZLEMJ»",
  !!ukm && ukm.jaizlemj === false && ukm.p === 500 && !ukm.w.includes("JĀIZLEMJ"), JSON.stringify(ukm));

// ── 4. Īstais calc() ar viltus DOM (lapai ir paroles slēdzene — pārlūkā to neapejam) ──
// Palaiž VISU lapas skriptu un pārbauda, KO cilvēks ieraudzīs, kad atzīmē ŪK bez izlemtas cenas.
const el = {};
function elem(id) {
  if (!el[id]) el[id] = { id, style: {}, innerHTML: "", textContent: "", value: "", checked: false,
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {}, setAttribute() {}, getAttribute() { return null; }, focus() {},
    querySelectorAll() { return []; }, querySelector() { return null; }, appendChild() {} };
  return el[id];
}
const dom = { document: { getElementById: elem, querySelectorAll: () => [], querySelector: () => null,
    addEventListener() {}, createElement: () => elem("_tmp" + Math.random()), body: elem("body") },
  localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
  sessionStorage: { getItem: () => null, setItem() {}, removeItem() {} },
  navigator: { clipboard: { writeText() {} } }, setTimeout() {}, clearTimeout() {}, console,
  location: { hash: "", search: "" }, alert() {}, confirm: () => true, addEventListener() {} };
dom.window = dom;
vm.createContext(dom);
for (const s of skripti) vm.runInContext(s, dom);
vm.runInContext(`darb = "dziv";
  ekas = [{tips: TIPI.findIndex(t => t.cat === "apartment"), platiba: "60", stavi: 1, apsild: false}];
  calc(); svcChecked.uk = true; calc(false);`, dom);
const sub = el["total-sub"].textContent;
t("calc(): atšifrējumā «ŪK … JĀIZLEMJ TOMAM», ne «0 EUR»", /ŪK<\/span><span>JĀIZLEMJ TOMAM/.test(el["brk"].innerHTML));
t("calc(): zem kopsummas brīdinājums, ka ŪK NAV iekļauta; kopsumma 450 EUR (bāze bez skices)",
  sub.includes("ŪK cena kalkulatorā vēl nav izlemta") && el["total"].textContent === "450 EUR",
  el["total"].textContent + " | " + sub);

console.log(kritumi ? `\n${kritumi} KRĪT` : "\nVISS OK (11/11)");
process.exit(kritumi ? 1 : 0);
