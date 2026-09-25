// VR cenas tests — darbina ĪSTĀS vrEka()/vrCena()/vrKomerc() no index.html (ne kopiju).
// Vladimira lēmums 25.09.2026 (TW #36447107): katrai ēkai max(tirgus, stundu grīda), noapaļo
// līdz 10 €; 2. un nākamajām ēkām tirgus −15 %, bet ne zem grīdas; virs 700 m² — individuāli;
// komerclietošana = 2× 3. līmenis.
// Palaišana:  node scripts/test_vr_cena.js      (exit 0 = OK, 1 = regresija)
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
const AVOTS = [
  nem(/const VR_TIRGUS=\{[^}]*\};/, "VR_TIRGUS"),
  nem(/const VR_STUNDAS=\{[^}]*\};/, "VR_STUNDAS"),
  nem(/const VR_LIKME=[^;]*;/, "VR_LIKME"),
  nem(/const VR_KOEF=\[[^;]*\];/, "VR_KOEF"),
  nem(/const VR_ATLAIDE=[^;]*;/, "VR_ATLAIDE"),
  nem(/function r10\(n\)\{[^}]*\}/, "r10()"),
  nem(/function vrKoef\(a\)\{[^\n]*\}/, "vrKoef()"),
  nem(/function vrEka\(a,lim,nr\)\{[\s\S]*?\n\}/, "vrEka()"),
  nem(/function vrCena\(platibas,lim\)\{[\s\S]*?\n\}/, "vrCena()"),
  nem(/function vrKomerc\(platibas\)\{[^\n]*\}/, "vrKomerc()"),
].join("\n");

function ielade(kods) {
  const ctx = {};
  vm.runInNewContext(kods + "\nthis.o={vrEka,vrCena,vrKoef,vrKomerc,r10};", ctx);
  return ctx.o;
}

// [nosaukums, izturēja?, ko ieguva]
function parbaudes(k) {
  const kopa = (pl, l) => k.vrCena(pl, l).kopa;
  const tri = (pl) => ["L1", "L2", "L3"].map((l) => kopa(pl, l));
  const r = [];
  const viena = tri([267]);
  r.push(["1 ēka 267 m² → 820 / 1390 / 2130", viena.join("/") === "820/1390/2130", viena.join("/")]);
  const divas = tri([460, 135]);
  r.push(["2 ēkas 460 + 135 m² → 1890 / 2890 / 4460", divas.join("/") === "1890/2890/4460", divas.join("/")]);
  const pirts = ["L1", "L2"].map((l) => k.vrCena([460, 135], l).rindas[1].cena);
  r.push(["2. ēka −15 %, bet ne zem grīdas: pirts L1 590 (grīda), L2 730 (−15 %)",
    pirts.join("/") === "590/730", pirts.join("/")]);
  const maza = k.vrCena([50], "L1").rindas[0];
  r.push(["mazai ēkai uzvar grīda: 50 m² L1 → 460 (22 h × 30 × 0,7)",
    maza.cena === 460 && maza.grida > maza.tirgus, String(maza.cena)]);
  const robezas = [60, 61, 100, 101, 160, 161, 250, 251, 400, 401, 700].map((a) => k.vrKoef(a));
  r.push(["koeficienta robežas iekļaujošas (≤60 0,7 … ≤700 1,3)",
    robezas.join(",") === "0.7,0.8,0.8,0.9,0.9,1,1,1.1,1.1,1.3,1.3", robezas.join(",")]);
  const liela = k.vrCena([701], "L1");
  const jaukta = k.vrCena([460, 701], "L3");
  r.push(["virs 700 m² → individuāli, kopsummas nav (arī, ja tāda ir palīgēka)",
    liela.kopa === null && liela.rindas[0].individ === true && jaukta.kopa === null,
    String(liela.kopa) + " / " + String(jaukta.kopa)]);
  r.push(["komerclietošana = 2× 3. līmenis: 267 m² 4260, 460+135 m² 8920, >700 m² individuāli",
    k.vrKomerc([267]) === 4260 && k.vrKomerc([460, 135]) === 8920 && k.vrKomerc([701]) === null,
    k.vrKomerc([267]) + " / " + k.vrKomerc([460, 135])]);
  r.push(["noapaļo līdz TUVĀKAJIEM 10 € (817,5 → 820; 1894 → 1890; 815 → 820)",
    k.r10(817.5) === 820 && k.r10(1894) === 1890 && k.r10(815) === 820,
    [k.r10(817.5), k.r10(1894), k.r10(815)].join("/")]);
  return r;
}

let kritumi = 0;
function t(nos, ok, papildus) {
  console.log((ok ? "  OK    " : "  KRĪT  ") + nos + (ok ? "" : "  :: " + (papildus || "")));
  if (!ok) kritumi++;
}

console.log("VR cena — īstā index.html versija:");
for (const [nos, ok, info] of parbaudes(ielade(AVOTS))) t(nos, ok, info);

// Mutācijas: katrai JĀNOGĀŽ vismaz viena pārbaude — citādi tests to kļūdu nepamanītu.
const MUTACIJAS = [
  ["2. ēkai bez −15 %", "const VR_ATLAIDE=0.15;", "const VR_ATLAIDE=0;"],
  ["grīda ignorēta", "cena:r10(Math.max(tirgus,grida))", "cena:r10(tirgus)"],
  ["apaļo uz augšu", "return Math.round(n/10)*10;", "return Math.ceil(n/10)*10;"],
  ["−15 % arī galvenajai ēkai", "(nr>0?1-VR_ATLAIDE:1)", "(1-VR_ATLAIDE)"],
  ["robeža ≤ kļūst par <", "if(a<=lim)return k", "if(a<lim)return k"],
  ["3. līmeņa m² likme 6,0", "L3:[390,6.5]", "L3:[390,6.0]"],
  ["virs 700 m² tomēr rēķina", "return k;return null;}", "return k;return 1.3;}"],
  ["komerclietošana 1× L3", "return v.kopa===null?null:2*v.kopa;", "return v.kopa===null?null:v.kopa;"],
];
console.log("Mutācijas (katrai jākrīt):");
for (const [nos, no, uz] of MUTACIJAS) {
  if (!AVOTS.includes(no)) { t("mutācija «" + nos + "» — paraugs index.html vairs NAV", false, no); continue; }
  const krit = parbaudes(ielade(AVOTS.replace(no, uz))).filter(([, ok]) => !ok).length;
  t("mutācija «" + nos + "» pieķerta (" + krit + " pārb.)", krit > 0, "neviena pārbaude nekrita");
}

// Savienojums ar lapu: kartītes un atjaunošana pēc katra calc()
console.log("Lapa:");
t("kreisajā kolonnā ieslēgšana + komerclietošana", /id="vr-on"/.test(html) && /id="vr-komerc"/.test(html));
t("labajā kolonnā VR kartīte", /id="vr-card"/.test(html) && /id="vr"/.test(html));
t("vrRender() iet PĒC katra calc() (apvalks)",
  /const _calcBezVR=calc;\s*calc=function\(resetSvc\)\{_calcBezVR\(resetSvc\);vrRender\(\);\};/.test(html));
t("darbību joprojām 8 (VR nav 9. darbība)", (nem(/const DARBS=\[[\s\S]*?\];/, "DARBS").match(/\{id:"/g) || []).length === 8);

// vrRender() ar minimālu document aizstājēju: kartīte redzama tikai ieslēgtai VR ar platību,
// bez darbības paslēpj «izvēlies darbību», kopsummas un komerclietošana nonāk HTML.
function zimet(ekas, ieslegts, komerc, darb) {
  const el = {};
  for (const id of ["vr-card", "empty-card", "vr"]) el[id] = { style: {}, innerHTML: "" };
  el["vr-on"] = { checked: ieslegts };
  el["vr-komerc"] = { checked: komerc };
  const ctx = { document: { getElementById: (id) => el[id] }, ekas, darb };
  vm.runInNewContext([
    nem(/const TIPI=\[[\s\S]*?\];/, "TIPI"),
    nem(/function eur\(n\)\{[^}]*\}/, "eur()"),
    AVOTS,
    nem(/function vrRender\(\)\{[\s\S]*?\n\}/, "vrRender()"),
    "vrRender();",
  ].join("\n"), ctx);
  return { el, eur: ctx.eur };
}
// Gaidīto virkni veido lapas PAŠAS eur() — tūkstošu atdalītājs (lv-LV ICU) tad nav jāmin.
const norm = (s) => s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
const divasZ = zimet([{ tips: 0, platiba: "460" }, { tips: 6, platiba: "135" }], true, true, null);
const divasEl = divasZ.el, E = divasZ.eur;
const divasTxt = norm(divasEl.vr.innerHTML);
t("vrRender: 2 ēkas — KOPĀ 1890 / 2890 / 4460 EUR un komerclietošana 8920 EUR",
  divasTxt.includes(norm("KOPĀ " + E(1890) + " " + E(2890) + " " + E(4460))) &&
  divasTxt.includes(norm("Komerclietošana (2× 3. līmenis): " + E(8920))),
  divasTxt.slice(0, 300));
t("vrRender: kartīte redzama; bez darbības «izvēlies darbību» paslēpta",
  divasEl["vr-card"].style.display === "block" && divasEl["empty-card"].style.display === "none");
const izslEl = zimet([{ tips: 0, platiba: "460" }], false, false, null).el;
t("vrRender: izslēgta VR → kartīte paslēpta, «izvēlies darbību» neaiztikta",
  izslEl["vr-card"].style.display === "none" && izslEl["empty-card"].style.display === undefined);
const lielaTxt = norm(zimet([{ tips: 0, platiba: "750" }], true, false, "jaunbuve").el.vr.innerHTML);
t("vrRender: 750 m² → «individuāli» un brīdinājums, nekādas kopsummas",
  /individuāli/.test(lielaTxt) && /virs 700 m²/.test(lielaTxt) && /KOPĀ\s+—\s+—\s+—/.test(lielaTxt), lielaTxt.slice(0, 200));

console.log(kritumi ? "\nREZULTĀTS: " + kritumi + " KRĪT" : "\nREZULTĀTS: viss OK");
process.exit(kritumi ? 1 : 0);
