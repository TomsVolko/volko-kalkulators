// Ražošanas ēkas tests — darbina ĪSTO TIPI / grp() / docForBase() no index.html (ne kopiju).
// Toma lēmums 17.09.2026 (TW #36414329): ēkas tips «Ražošanas ēka (autoserviss, automazgātava,
// darbnīca)», k = 0,70. Gaidītās atbildes nolasītas 25.09.2026 no AUTORITATĪVĀ rīka
// `legalizacijas_cels.py --kategorija industrial` un `ekas_grupa.py --pielietojums razosana`
// (claude-skills, volko-shared/scripts) — kalkulatoram tās jāatkārto, ne jāizdomā.
// Palaišana:  node scripts/test_razosanas_eka.js      (exit 0 = OK, 1 = regresija)
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
  TIPI: nem(/const TIPI=\[[\s\S]*?\n\];/, "TIPI"),
  grp: nem(/function grp\(a,f,cat\)\{[\s\S]*?\n\}/, "grp()"),
  docForBase: nem(/function docForBase\(e\)\{[\s\S]*?\n\}/, "docForBase()"),
};

// DOM ķeksīši — visi izslēgti (tipiskā piedāvājuma situācija); `darb` iestata tests.
function ielade(tipi) {
  const kods = [tipi, avots.grp, avots.docForBase,
    "var darb='jaunbuve';",
    "var document={getElementById:function(){return {checked:false};}};",
    "this.o={TIPI,grp,docForBase,setDarb:function(v){darb=v;}};"].join("\n");
  const ctx = {};
  vm.runInNewContext(kods, ctx);
  return ctx.o;
}

let kritumi = 0;
function t(nos, ok, papildus) {
  console.log((ok ? "  OK    " : "  KRĪT  ") + nos + (ok ? "" : "  :: " + (papildus || "")));
  if (!ok) kritumi++;
}

const k = ielade(avots.TIPI);
const RI = k.TIPI.findIndex(x => x.n.startsWith("Ražošanas ēka"));
function doc(o, tips, darbs, a, f) {
  if (tips < 0) return { dt: "NAV_RINDAS", ref: "" };   // bez rindas krīt ar KRĪT, ne ar izņēmumu
  o.setDarb(darbs);
  return o.docForBase({ tips, platiba: String(a), stavi: String(f) });
}
function ir(r, dt, ref) { return r.dt === dt && String(r.ref).indexOf(ref) !== -1; }

// ── 1. Rinda eksistē, ar lēmuma skaitli, un nenobīda cieti kodētos indeksus ──
t("rinda «Ražošanas ēka …» ir TIPI sarakstā", RI !== -1);
t("k = 0,70 un cat = industrial (Toma lēmums 17.09.2026)", RI !== -1 && k.TIPI[RI].k === 0.70 && k.TIPI[RI].cat === "industrial");
const PIRMIE = ["Individuālā dzīvojamā māja", "Vasarnīca / dārza māja", "Dvīņu māja", "Rindu māja",
  "Daudzdzīvokļu māja", "Dzīvoklis / telpu grupa", "Pirts (palīgēka)", "Saimniecības ēka / šķūnis",
  "Garāža", "Noliktava"];
t("tips 0–9 nemainīti (tips:0/5/6/7 ir cieti kodēti index.html)",
  PIRMIE.every((n, i) => k.TIPI[i].n === n), k.TIPI.slice(0, 10).map(x => x.n).join(" | "));

// ── 2. Tas pats ceļš kā legalizacijas_cels.py --kategorija industrial (nolasīts 25.09.2026) ──
t("jaunbūve 318 m², 1 st. → II gr., būvatļauja 7.³", k.grp(318, 1, "industrial") === "II" && ir(doc(k, RI, "jaunbuve", 318, 1), "bp", "7.³"));
t("jaunbūve 2000 m² → II gr.; 2001 m² → III gr. (MK 500 1. piel.; ekas_grupa.py)",
  k.grp(2000, 1, "industrial") === "II" && k.grp(2001, 1, "industrial") === "III");
t("jaunbūve 50 m², 1 st. → I gr., PR 7.²1. (7.¹4. ražošanas ēku nesedz)", ir(doc(k, RI, "jaunbuve", 50, 1), "pr", "7.²1."));
t("pārbūve 318 m² → būvatļauja 7.³", ir(doc(k, RI, "parbuve", 318, 1), "bp", "7.³"));
t("nojaukšana 318 m² → PR 7.²5. (NAV palīgēka → nav paziņojuma)", ir(doc(k, RI, "nojauksana", 318, 1), "pr", "7.²5."));
t("legalizācija 50 m² → PR 7.²1. (līdz šim kalkulators deva paziņojumu 7.¹4.)", ir(doc(k, RI, "leg-bez", 50, 1), "pr", "7.²1."));

// ── 3. Regresija — esošie tipi atbild tāpat kā līdz šim ──
t("Pirts legalizācija 40 m² → paziņojums 7.¹4. (palīgēkai nemainās)", ir(doc(k, 6, "leg-bez", 40, 1), "pz", "7.¹4."));
t("Saimniecības ēka jaunbūve 318 m² → PR 7.²1. (palīgēkai nemainās)", ir(doc(k, 7, "jaunbuve", 318, 1), "pr", "7.²1."));
t("Noliktava jaunbūve 318 m² → būvatļauja 7.³ (nemainās)", ir(doc(k, 9, "jaunbuve", 318, 1), "bp", "7.³"));

// ── 4. MUTĀCIJA: vecais apvedceļš (ražošana kā «aux») — testam JĀKRĪT ──
const km = ielade(avots.TIPI.replace('k:0.70,cat:"industrial"', 'k:0.70,cat:"aux"'));
const rm = doc(km, RI, "jaunbuve", 318, 1);
t("MUTĀCIJA: ar cat aux ražošanas jaunbūve 318 m² vairs NAV būvatļauja (tests to pamana)",
  !ir(rm, "bp", "7.³"), JSON.stringify(rm));

console.log(kritumi ? `\n${kritumi} KRĪT` : "\nVISS OK (13/13)");
process.exit(kritumi ? 1 : 0);
