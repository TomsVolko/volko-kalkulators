# Kalkulatora uzlabojumi — vakara sesija

> Sesija sākta: 2026-06-08. Avots: `Cena_21.03.2025_VV_.xlsm` + `index.html` (271KB).

---

## Prioritātes (secībā)

### 🔴 1. Stingra būves grupas noteikšana pēc MK Nr. 529

**Problēma:** Pašreizējā funkcija ir nepareiza:
```js
function grp(a,f){ if(a<=25&&f<=1)return"I"; if(a>1500||f>=4)return"III"; return"II"; }
```
Viss no 26m² iet II grupā — bet individuālā dzīvojamā māja ≤60m², 1 stāvs var būt I grupā.

**Uzdevums:**
- Izpētīt MK Nr. 529 "Ēku būvnoteikumi" konkrētus pantus
- Ieviest loģiku kas ņem vērā: platība + stāvi + **ēkas funkcija**
- Ja neskaidrs gadījums → jautā precizēt papildlauki
- Grupas noteikšanu parādīt ar paskaidrojumu (kāpēc šī grupa)

---

### 🔴 2. Pašvaldību autocomplete (visi Latvijas novadi)

**Problēma:** 20 fiksētas `<option>` — nav meklēšanas.

**Uzdevums:**
- Text input + live filtrēšana rakstot
- Visi 43 novadi + 9 pilsētas = 52 vienības
- Katrai saglabāt `{p: koef, s: koef}` struktūru (kā pašlaik)
- Grupēt: Rīga / Rīgas apkārtne / Pierīga / Reģionālie centri / Citi novadi

---

### 🟡 3. Papildpakalpojumi ar "Ieteicams" badges

**Uzdevums:**
- Balstoties uz projekta tipu + grupu → automātiski iezīmēt ieteicamās
- Katrai pozīcijai: `why` (kāpēc vajadzīgs) + `when_required` (kad obligāts)
- Cena mainās reāllaikā no checkboxiem
- Struktūra jau daļēji ir — vajag paplašināt

---

### 🟡 4. Dokumentu checklist

**Uzdevums:**
- Dinamisks saraksts atkarībā no projekta tipa + grupas
- Statuss: ✓ parasti ir / ⚠️ bieži trūkst / ✗ reti ir
- Lai klientam tikšanās laikā var izskaidrot ko nest

---

### 🟡 5. Risinājuma ceļi — 3 varianti

**Uzdevums:**
- Ātrākais / Lētākais / Pilnīgākais (vai līdzīga struktūra)
- Ieteicamais iezīmēts ar "IETEICAMS" badge
- Katram solim: nedēļas, cena, kas dara (Volko / Klients / Iestāde)
- Vizuāls timeline vai soļu kārtne

---

### 🟢 6. Jaunbūve — 3 paketes ar checkbox pozīcijām

**Excel avots:** lapas `1.līmenis`, `2.līmenis`, `3.līmenis`

**Uzdevums:**
- 3 paketes (L1 / L2 / L3) ar checkbox katrai pozīcijai
- Noķeksējot → cena mainās reāllaikā
- Ja noķeksē obligātu pozīciju → modāls: "Šo nevar izņemt, jo..."
- Pozīciju saraksts no Excel (SKICE, VR, MBP, BP fāzes)

**Excel cenas struktūra:**
- Likme: 30 EUR/h
- Koeficients pēc platības grupas (0.7 → 3.0)
- Inženiertīkli: TI, GI, UKT, UK, AVK, ELT, EL, ESS, T, TS-CD, TS-L, UPP (manuāli)

---

### 🟢 7. Legalizācijas process ar likuma pantiem

**Uzdevums:**
- Pilns process solis pa solim
- Katram solim: konkrēts MK/Likuma pants (ne tikai "pēc likuma")
- Lai tikšanās laikā var izskaidrot ar pareiziem pantiem
- Jānošķir pēc grupas: I / II / III — process atšķiras

---

## Tehniskie fakti (izpētīts)

### Faili
- `index.html` — 271KB, viens fails, GitHub Pages
- `ar-section.html`, `bk-ai-section.html` — atsevišķas sadaļas
- Python skripti (`build_index.py` u.c.) — nav tracked

### Pašreizējās pašvaldības (20 opcijas):
Rīga (×1.20) / Mārupes, Ķekavas, Salaspils, Ādažu/Ropažu/Olaines, Stopiņu/Garkalnes/Babītes (×1.10) /
Jūrmala, Sigulda, Jelgava, Ogre, Saulkrasti/Limbaži, Tukums/Cēsis, Dobele/Bauska/Kandava (×1.00) /
Valmiera, Talsi, Saldus/Kuldīga, Jēkabpils/Madona (×1.02) /
Liepāja, Ventspils, Daugavpils, Rēzekne (×1.05)

### Grupas koeficienti (GC):
```js
const GC = { "I": 0.7, "II": 1.0, "III": 1.5 }
```

### Excel koeficienti (platības grupas, Sheet1):
```
<60m²: 0.7  |  60-100m²: 0.8  |  100-160m²: 0.9  |  160-250m²: 1.0
250-400m²: 1.1  |  400-700m²: 1.3  |  700-1200m²: 2.0  |  >1200m²: 3.0
```

---

## Sākšanas instrukcija (citā datorā)

```
1. git pull origin main
2. Atvērt index.html lokāli vai live server
3. Sākt ar uzdevumu #1 — MK Nr. 529 izpēte + grp() funkcija
4. Pārbaudīt: https://tomsvolko.github.io/volko-kalkulators/
```

**Parole:** 22!Deamontools
