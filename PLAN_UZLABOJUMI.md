# Kalkulatora uzlabojumu plāns — 2026-06-10

> Avots: Toma konsultācijas pārskats + juridiskā verifikācija (likumi.lv caur aģentiem).
> Lēmumi: 20% nost tikai AR · apakštabi = "Jaunbūve" (tikai jaunbūve+tipveida) / "Legalizācija" (viss esošais) · pilns Excel klons · dublikātus dzēst.

## FĀZE A — Ātrie labojumi (šī sesija)

1. **20% rezerve nost AR projektam** (papildpakalpojumiem paliek):
   - `calcAR`: totCli = arInt (AR bez uzcenojuma); ar-hint bez "rezerve"
   - passport AR rinda: data-cli = data-int
   - `I_FIXED` mazēku fiksētās cenas atstāj kā ir (atsevišķi noteiktas, ne formulas)
   - Jaunbūves pakešu cenas neaiztiek — tās pārbūvēs Fāze B
   - AI smadzenes: "AR cena bez rezerves; papildpakalpojumiem +20%"
2. **ESI badge mīkstināt** (la: critical→recommended; teksti "sarežģītiem projektiem — neskaidra zona, aizsargjoslas, kopīpašums, funkcijas maiņa"; pre-checklist/TYPE_INFO/steps "OBLIGĀTI ESI" mīkstināt)
3. **Atļaujas veids pēc grupas+funkcijas** (nevis tikai 200 m²):
   - I gr. → paziņojums/paskaidrojuma raksts
   - II gr. viena dzīvokļa (individuālā/vasarnīca) ≤200 m² → paskaidrojuma raksts (MK 529 7.2.1.)
   - II gr. viena dzīvokļa >200 m² → būvprojekts
   - II gr. palīgēka/saimniecības → paskaidrojuma raksts
   - II gr. daudzdzīvokļu/publiska/birojs/tirdzniecība → būvprojekts
   - III gr. → būvprojekts vienmēr
4. **Juridiskās korekcijas**: lc bez pārbūves → paskaidrojuma raksts (7.2.7., atteikums tikai ja TIAN neatļauj — 52. p.); LEG_BASIS sodi diferencēti pēc BL 25. p. (bez paskaidrojuma raksta ≤75/100 EUR; bez būvatļaujas ≤2000/20000 EUR); TAA = "būvvalde parasti pieprasa" (MK 500 38.6. "ja nepieciešams"); 2025. grozījumi MK 529 (spēkā 01.01.2026) par bez dokumentiem realizētu ieceru sakārtošanu — vispārīga atsauce BEZ punkta numura, kamēr nav manuāli pārlasīts
5. **Apakštabi pēc Toma definīcijas**: Jaunbūve = jaunbūve, tipveida; Legalizācija = optgroup "Nereģistrēta būvniecība" (la, lbv, lbp, lc) + "Plānoti darbi esošā ēkā" (izmaiņu, rekonstrukcija, vienk, nojaukšana). `isLegal()` NEMAINĀS (cenu loģika tikai la/lbv/lbp/lc)
6. **Grupu loģikas caurspīdīgums**: ja `grp()` (juridiskā) ≠ `grpPrice()` (cenas) — breakdown rindā paskaidrot. ATVĒRTS CENU JAUTĀJUMS Tomam: vai 26–60 m² vienstāva mazēkām dot I grupas cenu (tagad cenu "bedre" — juridiski I gr., cena II gr. ×1.20)
7. **Dzēst dublikātus**: legalizacija-paketes karte (A/B/C), ar-solution-paths (⚡💰🏆), auto-ieteikumi panelis (passport tabula to aizstāj; getRecs() paliek — passport lieto)
8. **AI smadzeņu sinhronizācija** ar visu augstāk

## FĀZE B — Konfigurators pēc Excel ✅ IZDARĪTS 2026-06-10 (commit 28ac44f)

- Avots: `Cena_21.03.2025_VV_.xlsm` lapas 1./2./3.līmenis (likme 30 €/h; Sheet1 ar 25 €/h ignorēt)
- Ekstrakts → JS dati: ~150 pozīcijas, katrai {fāze: SKICE/VR/MBP/BP, nosaukums, stundas}
- Kopējais bloks "Visos līmeņos jaunbūvēm" (vienmēr cenā): konsultācijas, piedāvājums, līgums, analīze+PU, paraksti, saziņa
- 4 līmeņi (I–IV) + MIX režīms (brīvi ķeksēt pāri līmeņiem)
- Cena = stundas × 30 × platības koef. (0.7 <60 / 0.8 60-100 / 0.9 100-160 / 1.0 160-250 / 1.1 250-400 / 1.3 400-700 / 2.0 700-1200 / 3.0 >1200)
- Inženiertīkli ar manuālu cenas ievadi: TI, GI, UKT, UK, AVK, ELT, EL, ESS, T, TS-CD, TS-L, UPP (3. gr.) + papildu sadaļas
- AU (autoruzraudzība) un EKSP (ekspertīzes labojumi) — opcionāli manuāli
- UI: fāžu sekcijas sakļaujamas, pozīciju ķeksīši, cena reāllaikā; bez 20% (Excel GALA CENA tiešā)

## FĀZE C — Vairākas ēkas ✅ IZDARĪTS 2026-06-10

- "➕ Pievienot ēku" — katrai: tips, platība, stāvi, funkcija → sava cena
- Kopsumma + juridiskā piezīme: viena iecere, piemēro augstākās grupas kārtību (MK 500 7. p.)
- Aizstāj pašreizējo "Ēku skaits ×n" (kas der tikai vienādām ēkām)

## FĀZE D — Pašvaldību dati

- Research aģenti pa pašvaldībām (sāk ar TOP ~15): TIAN links (geolatvija/teritorijasplanojums.lv), būvvaldes kontakti, nodevas apmērs, legalizācijas pastiprinātā nodeva (5× Rīgā — katrai pašvaldībai savs saistošo noteikumu Nr.), īpatnības (RVC, GNP, kāpu zona)
- Struktūra: MUNI_INFO pārbūve no koef-grupām uz konkrētām pašvaldībām; pārējām fallback + atruna

## FĀZE E — Kadastra Nr. + skillu integrācija ✅ IZDARĪTS 2026-06-10 (prompta ģenerators)

- Kalkulatorā lauks "Kadastra Nr." + poga "📋 Izpētes uzdevums" → noģenerē gatavu promptu (kadastrs.lv, zemesgrāmata, TIAN, aizsargjoslas) → Toms ielīmē Claude sesijā
- volko-research skill papildināt ar "kadastra izpētes" režīmu → mini-ESI atskaite klienta mapē

## FĀZE F — Likumu sargs v2 ✅ IZDARĪTS 2026-06-10 (scheduled task SKILL.md v2)

- Papildināt scheduled task `kalkulators-likumu-verifikacija`:
  1. Skenēt GAIDĀMOS grozījumus (pieņemti, vēl nav spēkā) — BL, MK 500, MK 529, LBN; likumi.lv "Saistītie dokumenti"/grozījumu saraksts
  2. Paziņojums Tomam (PushNotification + atskaite): kas mainās / no kura datuma / links
  3. Saturisko nosacījumu pārbaude (200 m² 7.2.1., funkcijas maiņa 7.2.7., grupas MK 500 1. piel.), ne tikai atsauču numuri
  4. Manuāli pārlasīt un apstiprināt: MK 529 "7.7." normu (aģenta atradums, vēl neverificēts cilvēkam)

## Juridiskā bāze (verificēta 2026-06-10, aģentu izvilkumi)

- BL 18. p. 2. d. — patvaļīgas būvniecības definīcija (5 veidi, t.sk. ekspluatācija neatbilstoši lietošanas veidam)
- BL 18. p. 5. d. — būvvaldes 2 lēmumi: atjaunot iepriekšējo stāvokli VAI atļaut būvniecību pēc prasību izpildes (=legalizācija)
- BL 18. p. 11. d. — lēmums izpildāms nekavējoties, apstrīdēšana neaptur
- BL 25. p. — sodi diferencēti pa pārkāpuma veidiem (≤15/20 vienības bez paskaidrojuma raksta; ≤400/4000 bez būvatļaujas; 1 vienība = 5 EUR)
- MK 529 7.2.1. — paskaidrojuma raksts: I gr. ēkas; II gr. VIENA DZĪVOKĻA māja ≤200 m²; palīgēkas; lauksaimniecības ēkas
- MK 529 7.2.7. — lietošanas veida maiņa bez pārbūves → paskaidrojuma raksts; 52. p. — atsaka tikai ja TIAN neatļauj
- MK 529 7.3. — pārējie → būvprojekts (t.sk. divu+ dzīvokļu, publiskās II gr.)
- MK 500 1. piel. 2.1.1. — I gr. = vienstāva ≤60 m²; 2.2. — III gr. kritēriji; 2.3. — II gr. pārējais
- MK 500 38.6. — TAA esošai būvei "ja nepieciešams" (praksē būvvaldes legalizācijai pieprasa)
- MK 500 7. p. — vairākas būves vienā iesniegumā → augstākās grupas kārtība
- 5× nodeva — pašvaldību saistošie noteikumi (katrai pašvaldībai savi)
