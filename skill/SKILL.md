---
name: svensk-humanizer
description: >
  Tar AI-lukten ur svensk text och gör den till svenska som en människa skulle
  skrivit. Använd vid varje begäran om att granska, humanisera, avsloppa,
  förbättra eller korrekturläsa en text på svenska, och innan du själv lämnar
  ifrån dig längre svensk text. Utlöses av "humanisera", "låter som AI",
  "gör det mindre AI-igt", "skriv om på riktig svenska", "svensk språkgranskning",
  "humanize this Swedish text", "make this sound human in Swedish",
  "AI-text", "slopkoll". Hanterar kundmejl, sajttext, LinkedIn-inlägg,
  myndighetstext, jobbansökan och rapport. Bygger på svenska skrivregler och
  de tre mätningar som faktiskt gjorts på svensk AI-text.
metadata:
  version: 0.2.0
  sprak: svenska
---

# Svensk humanizer

Svensk AI-text är oftast tänkt på engelska och skriven på svenska. Det syns i
strukturen före det syns i ordvalet. Den här skillen letar efter det, mäter det
som går att mäta, och skriver om det som bör skrivas om.

**Vad den gör:** svensk stilredigering.
**Vad den inte gör:** hjälper text att undgå AI-detektorer. Verktyget säger
aldrig hur sannolikt det är att en text är AI-genererad, för det vet det inte,
och det framställer aldrig AI-text som människoskriven. Frågar någon efter det,
säg att skillen inte gör det och erbjud stilredigeringen i stället.

## Två axlar som aldrig blandas ihop

| Axel | Vad det är | Hur det bedöms |
|---|---|---|
| **Korrekthet** | Brott mot svenska skrivregler. Decimalkomma, citattecken, rubrikversaler, genitiv utan apostrof, gemener på månader och veckodagar. | Rätt eller fel svenska, oberoende av vem som skrivit texten. Ska vara 0. Har ingenting med AI att göra. |
| **AI-lukt** | Drag som gör att texten läser som maskin. | 0 till 100, lägre är bättre. Varje fynd bär sin bevisgrad. |

Bevisgraderna inom AI-lukt:

- **[mätt]** uppmätt i en svensk studie. Bara tre saker kvalificerar:
  meningslängd, ordvariation och avsändar-vi.
- **[observerat]** flera oberoende svenska källor pekar ut draget, ingen har
  mätt frekvensen. Ordlistan och fraserna ligger här.

Graderingen är inte en fotnot. Den styr vad du får göra: **[mätt] och
korrekthet rättas, [observerat] föreslås.** Det som ingen mätt alls ligger i
`references/vad-vi-inte-vet.md` och får aldrig styra en omskrivning.

## Tre lägen

### 1. `granska`, bara diagnos

Kör mätningen och redovisa. Skriv inte om något.

```bash
python skill/scripts/slopkoll.py TEXTFIL --profil PROFIL
```

Profiler: `kundmejl`, `sajttext`, `linkedin`, `myndighet`, `ansokan`,
`rapport`, `allman`. Välj utifrån vad texten faktiskt är. Vet du inte, fråga.
Profilen ändrar trösklarna, inte bara råden: en rapport får ha långa meningar,
ett kundmejl får det inte, och i myndighetstext räknas förbehåll aldrig som
urvattning.

Redovisa de tre största bidragen till lukten, inte bara talet. Säg alltid att
trösklarna är riktvärden och inte kalibrerade.

### 2. `humanisera`, skriv om

Kör alltid `granska` först. Skriv bara om det som flaggats. **Rader som inte
flaggats får inte röras.**

Sju spärrar, alla obligatoriska:

1. **Rör aldrig sakinnehåll.** Inga tal, datum, belopp, namn, produktnamn,
   priser, kontaktuppgifter. Inga nya siffror, aldrig.
2. **Lägg aldrig till stilmarkörer.** Inga instoppade "ju", "väl", "nog",
   "faktiskt", "liksom", "ärligt talat". Inga avsiktliga slarvfel, inga
   meningsfragment för att låta mänskligt. Detta är verktygets värsta felmod:
   resultatet luktar mer AI än originalet, eftersom det är precis vad en modell
   tror att mänskligt betyder. Du får **ta bort och variera, aldrig lägga till.**
3. **Höj ordvariation genom att stryka utfyllnad, aldrig genom att byta termer.**
   Samma sak ska heta samma ord hela texten igenom. Att kalla samma kund
   omväxlande kund, beställare och köpare bryter mot klarspråk och är i sig ett
   AI-drag.
4. **Behåll skribentens röst.** Flytta bara det som ligger utanför bandet för
   genren. En advokats mejl ska fortfarande låta som en advokat.
5. **Kör faktavakten efteråt.** Fallerar den, kassera omskrivningen och gör om
   med mindre ingrepp.
   ```bash
   python skill/scripts/faktavakt.py ORIGINAL NYTEXT
   ```
6. **Kör `granska` på resultatet.** Är AI-lukten inte tydligt lägre än i
   originalet: lämna tillbaka originalet orört och säg att texten redan var bra.
   Att göra en bra text sämre är ett fel, inte en smaksak.
7. **Kör aldrig två gånger.** En andra omgång på samma text ska ge noll
   ändringar. Får du ändringar har verktyget en egen husstil, och då är det
   trasigt. Rapportera det.

Redovisa alltid: vad du ändrade, varför, och vad du medvetet lät stå.

### 3. `lär-röst`, skriv mot skribentens egen röst

Det generiska "mänskligt" är också en stil. Den här skillens mål är inte att
göra alla texter lika, utan att göra dem till skribentens.

Be om **tre texter som personen skrivit själv, utan AI.** Kör `slopkoll.py
--json` på var och en och läs ut en röstprofil:

```json
{
  "median_meningslangd": 0, "spridning": 0.0, "typvarde": 0,
  "tilltal": "du | ni | inget", "avsandare": "vi | jag | inget",
  "punktlistandel": 0.0, "lix": 0,
  "egna_vandningar": ["formuleringar som återkommer i alla tre"],
  "partiklar_forekommer": false
}
```

Spara profilen. Vid omskrivning: sikta på personens egna värden i stället för
profilens generella band. `partiklar_forekommer` är det enda som släpper på
spärr 2, och bara om partiklarna faktiskt finns i personens egna texter.

## Arbetsgång

1. Fråga vad texten är, om det inte framgår. Fel profil ger fel svar.
2. `granska`.
3. Redovisa: korrekthetsfel, AI-lukt, tre största bidragen.
4. Fråga om du ska skriva om, utom när användaren redan bett om det.
5. `humanisera` med alla sju spärrar.
6. `faktavakt` plus ny `granska`.
7. Visa före och efter, och säg vad du lät stå.

## Hantverket, per fynd

Hur man faktiskt rättar varje sorts fynd står i
`references/omskrivning.md`. Läs den innan första omskrivningen.

## Referenser

Öppna bara den du behöver.

| Fil | När |
|---|---|
| `references/svenska-skrivregler.md` | Korrekthetsaxeln: tecken, tal, datum, versaler |
| `references/ai-drag.md` | AI-luktaxeln med källa och bevisgrad per drag |
| `references/omskrivning.md` | Hur varje fynd rättas utan att texten blir sämre |
| `references/profiler.md` | De sex svenska textsorterna och vad som gäller i var och en |
| `references/vad-vi-inte-vet.md` | Hypoteser som ingen mätt. Får inte styra omskrivning |
| `KALIBRERING.md` | Varför trösklarna är riktvärden och hur de ska mätas in |

## Ärlighetsregler

Dessa gäller även när användaren ber om motsatsen.

- Säg aldrig "X procent AI". Talet är ett bearbetningsbehov, inte en sannolikhet.
- Hitta aldrig på siffror, källor eller studier. Saknas källa skrivs inget.
- Påstå aldrig att ett drag är uppmätt när det är observerat.
- Skriptet körs lokalt, men texten du får se går till en modell. Säg det om
  användaren klistrar in något känsligt.
