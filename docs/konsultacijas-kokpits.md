# Volko kalkulators — konsultācijas kokpits: analīze un plāns

Sagatavots: 02.07.2026 (Toms + Claude). Mērķis: klienta sarunas laikā ievadi datus → uzreiz redzi AR cenu, vajadzīgos papildpakalpojumus AR pamatojumu un legalizācijas ceļu.

## Analīzes secinājumi (02.07.2026)

**Struktūra:** viens index.html (~400 KB), cilnes AR/BK/NOD + 3 soļu vednis + Projekta pase + "Konsultācijas skats".
Lēmumu dzinējs (grp/docTypeFor/pathReason/determineServices) verificēts pret MK529 (sk. claude-skills
`volko-shared/references/ieceres_dokumenti_MK529.md` + `legalizacijas_cels.py` — 1:1 tā pati loģika).

**Problēmas dzīvai konsultācijai (konstatētas praksē):**
1. Dublēti ievades lauki (wiz-* vs ar-*) — dati viena skata neredzēja otru. ✅ IZLABOTS 02.07 (divvirzienu sync + prefill)
2. Rezultāts izkaisīts 3 vietās (vedņa 3. solis / ar-svc-auto / pase) no 3 datu struktūrām (TYPE_INFO/STEPS_DATA/PASSPORT_DATA)
3. Cenu nekonsekvence legalizācijai (sk. tabulu zemāk) — NEIZLABOTS, vajag Vladimira lēmumu
4. Dzīvokļa jautājumi (nesošās/ZG) bija tikai detalizētajā skatā. ✅ IZLABOTS (vednī)
5. Nebija izejas klientam/Claude. ✅ IZLABOTS (izdruka + kopēšana)

## Izdarīts 02.07.2026 (1. + 3. fāze)

- **Kokpits vedņa 2. solī:** rezultāti (ceļš+cena+pakalpojumi+soļi) renderējas DZĪVI zem ievades laukiem ar katru taustiņu;
  3. solis paliek kā pilnekrāna rezultāts ("Pilnekrāna rezultāts →").
- **Divvirzienu sinhronizācija** wiz ↔ ar lauki (wizPrefill + wizSync) — vairs nav "Ievadi platību iepriekšējā solī".
- **Dzīvokļa jautājumi vednī:** "Darbi skar nesošās konstrukcijas" + "Mērķis — ieraksts zemesgrāmatā" (rādās, kad izvēlēta dzīvokļa funkcija).
- **🖨 Kopsavilkums klientam:** drukas versija (objekts, dokuments+pamatojums, cenu tabula ar kopsummu, pakalpojumi ar kāpēc,
  soļi, disclaimers) — @media print, tikai kopsavilkums.
- **📋 Kopēt Claude:** strukturēts teksts starpliktuvē (kopsavilkums.md / piedāvājumam / volko-price ievadei).

## PALIKUŠAIS DARBS

### 2. fāze — cenu likmes legalizācijai (VAJAG VLADIMIRA LĒMUMU)

Šobrīd vednī "Uzbūvēts BEZ atļaujas" VIENMĒR lieto rekonstrukcijas likmi. Reālā pārdošanā (Tumšupa 1, dzīvokļu
apvienošana 115 m²) lietota izmaiņu likme → kalkulators rāda ~65% dārgāk nekā pārdots.

AR likmes (€/m², bez koeficientiem) pa platībām:

| Platība | izmaiņu | vienk. atjaunošana | rekonstrukcija | jaunbūve |
|---|---|---|---|---|
| 60 m² | 20 → 1200 € | 19 → 1140 € | 28 → 1680 € | 30 → 1800 € |
| 115 m² | 16 → 1840 € | 15 → 1725 € | 24 → 2760 € | 26 → 2990 € |
| 150 m² | 15 → 2250 € | 14 → 2100 € | 22 → 3300 € | 24 → 3600 € |
| 250 m² | 11 → 2750 € | 10 → 2500 € | 17 → 4250 € | 19 → 4750 € |

(Gala cenā vēl funkcijas/grupas/pašvaldības koeficienti. Tumšupa 1 pārdots: AR 2200 €.)

**Jautājumi Vladimiram:**
1. Vai legalizācijas cenas likme jāizvēlas pēc DARBU RAKSTURA (dzīvokļa apvienošana → izmaiņu; pilna pārbūve → rekonstrukcija),
   nevis vienmēr rekonstrukcija?
2. Vai dzīvoklim (telpu grupai) vajag savu likmju rindu (mazāks apjoms nekā ēkai ar to pašu m²)?
3. Ja jā — kartējums: legaliz+dzīvoklis→izmaiņu; legaliz+ēka bez apjoma maiņas→izmaiņu; legaliz+apjoma maiņa/nesošās→rekonstrukcija?

### 4. fāze — datu struktūru apvienošana (tehniskais parāds)
- TYPE_INFO / STEPS_DATA / PASSPORT_DATA → viens datu avots (PASSPORT_DATA kā kodols); vedņa renderis un pase lasa no viena.
- STEPS_DATA la/lbv/lbp/lc satur novecojušus tekstus (piem. "III grupai PR nav pietiekams") — pārskatīt pret centrālo tabulu.
- NOD soļos visur pielikt "(atsevišķs līgums)" marķējumu.

### Idejas vēlāk
- Query-string prefill (?platiba=115&funkcija=apartment...) — Claude var atvērt kalkulatoru ar aizpildītiem datiem.
- Kopsavilkuma PDF ar logo (ne tikai window.print).
- Konsultācijas vēsture (localStorage) — pēdējie 10 aprēķini.
