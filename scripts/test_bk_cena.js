// BK cenas tests — darbina ĪSTO bkCena() no index.html (ne kopiju).
// Toma lēmums 24.09.2026 (TW #36435977): līdz 100 m² bāze 2200 EUR pirms koeficienta s,
// visām ēkām; virs 100 m² pakāpes aug no 2200 tāpat kā agrāk no 1400 -> 2800 / 3800.
// Palaišana:  node scripts/test_bk_cena.js      (exit 0 = OK, 1 = regresija)
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
  SVC_BASE: nem(/const SVC_BASE=\{[^}]*\};/, "SVC_BASE"),
  XL: nem(/const BK_XL_NO=[^;]*;/, "BK_XL_NO/M2/MAX"),
  CAP: nem(/const BK_XL_CAP=[^;]*;/, "BK_XL_CAP"),
  bkCena: nem(/function bkCena\(a\)\{[\s\S]*?\n\}/, "bkCena()"),
  r50: nem(/function r50\(n\)\{[^}]*\}/, "r50()"),
  MT: nem(/const _MT=\{[\s\S]*?\};/, "_MT"),
};

function ielade(svc) {
  const kods = [svc, avots.XL, avots.CAP, avots.bkCena, avots.r50, avots.MT,
    "this.o={SVC_BASE,BK_XL_NO,BK_XL_M2,BK_XL_MAX,BK_XL_CAP,bkCena,r50,_MT};"].join("\n");
  const ctx = {};
  vm.runInNewContext(kods, ctx);
  return ctx.o;
}

function augosa(k) {  // pirmā platība, kur cena KRĪT (vai null)
  for (let a = 1; a < 3000; a++) if (k.bkCena(a + 1) < k.bkCena(a)) return a + 1;
  return null;
}

let kritumi = 0;
function t(nos, ok, papildus) {
  console.log((ok ? "  OK    " : "  KRĪT  ") + nos + (ok ? "" : "  :: " + (papildus || "")));
  if (!ok) kritumi++;
}

const k = ielade(avots.SVC_BASE);
const s = (grupa) => k._MT[grupa].s;
t("līdz 100 m² bāze 2200 (50 un 100 m²)", k.bkCena(50) === 2200 && k.bkCena(100) === 2200,
  k.bkCena(50) + " / " + k.bkCena(100));
t("Ropaži (Pierīga, s 1.05): 100 m² -> 2300, vairs NE 1450",
  k.r50(k.bkCena(100) * s("P")) === 2300, String(k.r50(k.bkCena(100) * s("P"))));
t("pakāpes aug no 2200 kā agrāk no 1400: 101 m² 2800, 251 m² 3800",
  k.bkCena(101) === 2800 && k.bkCena(251) === 3800, k.bkCena(101) + " / " + k.bkCena(251));
t("cena nekad nekrīt, platībai augot (1–3000 m²)", augosa(k) === null, "krīt pie " + augosa(k) + " m²");
t("virs 450 m² +10 EUR/m² bez lēciena (450 -> 451)",
  k.bkCena(451) - k.bkCena(450) === k.BK_XL_M2, String(k.bkCena(451) - k.bkCena(450)));
t("griesti 12 000 nemainīti; iestājas no 1270 m²",
  k.BK_XL_MAX === 12000 && k.BK_XL_CAP === 1270 && k.bkCena(5000) === 12000,
  k.BK_XL_MAX + " / " + k.BK_XL_CAP);
t("dzīvokļa ceļš joprojām lieto bk_s (tātad arī 2200 × s)",
  /id:"bk",n:"BK — būvkonstrukciju daļa",st:"cond",p:r50\(SVC_BASE\.bk_s\*muni\.s\)/.test(html));

// MUTĀCIJA: tikai bk_s -> 2200, pārējās pakāpes vecās (2000 / 3000) — tieši tā kļūda,
// ko šis tests ir domāts noķert: 101 m² ēka tad maksā mazāk nekā 100 m².
const mut = ielade(avots.SVC_BASE.replace(/bk_m:\d+/, "bk_m:2000").replace(/bk_l:\d+/, "bk_l:3000"));
t("MUTĀCIJA: vecās pakāpes ar jauno bāzi -> kritums pie 101 m² TIEK pieķerts", augosa(mut) === 101,
  "augosa() = " + augosa(mut));

console.log("\n" + (kritumi ? "KRITIS" : "IZTURĒTS") + ": " + kritumi + " kritumi");
process.exit(kritumi ? 1 : 0);
