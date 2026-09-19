# Svensk humanizer

**Tar AI-lukten ur svensk text.** 66 mönster, 6 svenska textsorter och en
mätdel som körs lokalt utan beroenden. Byggd på svenska skrivregler och de tre
mätningar som faktiskt gjorts på svensk AI-text, inte på en översatt engelsk
ordlista.

Svensk AI-text är oftast tänkt på engelska och skriven på svenska. Det syns i
strukturen före det syns i ordvalet. Det är det här verktyget letar efter.

## Vad den gör och inte gör

**Gör:** svensk stilredigering. Hittar engelsk typografi, översatta
konstruktioner, maskinrytm och tomma formuleringar. Förklarar varför varje
fynd är ett fynd, och skriver om det på begäran.

**Gör inte:** hjälper text att undgå AI-detektorer. Verktyget säger aldrig hur
sannolikt det är att en text är AI-genererad, för det vet det inte, och det
framställer aldrig AI-text som människoskriven.

## Det som skiljer den från en översatt engelsk ordlista

Det mesta som avslöjar svensk AI-text finns inte på någon engelsk lista, för
reglerna existerar inte på engelska:

- Svenska citattecken, `”så här”`, samma tecken i båda ändar
- De två strecken hålls isär: `—` är alltid fel på svenska, `–` är tillåtet och
  flaggas bara vid överanvändning
- Decimalkomma, hårt mellanslag i tusental, mellanslag före procenttecken
- Rubriker med bara första ordet versalt, inte Title Case
- Gemener på månader, veckodagar, språk och nationaliteter
- Genitiv utan apostrof: `Judes bok`, inte `Jude's bok`
- Inget oxfordkomma
- Du eller ni, konsekvent
- Avsändar-vi, det enda drag som faktiskt uppmätts skilja svensk AI-text från
  svensk människotext
- Lix, inte engelska läsbarhetsmått
- Anglicismerna: ”på daglig basis”, ”i termer av”, ”adressera problemet”,
  ”det rekommenderas att”

## Varje påstående är graderat

Ingen annan humanizer, på något språk, redovisar hur den vet det den påstår.
Den här gör det, och graderingen styr vad verktyget får göra:

| Gradering | Betyder | Vad verktyget gör |
|---|---|---|
| **Korrekthet** | Brott mot svenska skrivregler | Rättas. Har ingenting med AI att göra |
| **[mätt]** | Uppmätt i en svensk studie. Tre saker kvalificerar | Rättas |
| **[observerat]** | Flera oberoende svenska källor, ingen mätning | Föreslås, med skäl |
| Otestat | Rimligt men ingen har mätt | Används inte. Dokumenteras i `vad-vi-inte-vet.md` |

Vi utelämnar med flit sådant som låter rimligt men är ogrundat. Att strö in
”ju” och ”väl” för att låta mänsklig är den vanligaste orsaken till att en
humanizer gör text sämre.

## Installation

Kopiera `skill/` till din skills-katalog:

```
~/.claude/skills/svensk-humanizer/
```

Kräver Python 3.8 eller senare. Inga paket, inga beroenden, ingen
nätverkstrafik. Mätdelen körs lokalt.

## Användning

Be om det på svenska eller engelska: ”humanisera den här texten”, ”låter det
här som AI?”, ”make this sound human in Swedish”.

Eller kör mätdelen direkt:

```bash
python skill/scripts/slopkoll.py text.md --profil sajttext
```

Profiler: `kundmejl`, `sajttext`, `linkedin`, `myndighet`, `ansokan`,
`rapport`, `allman`.

### Så ser det ut

```
  Korrekthet   6 fel mot svenska skrivregler
  AI-lukt      82/100   lägre är bättre
  Läser tydligt som AI-genererad svenska.

  Vad lukten består av:
    anglicismer          20.0  ####################
    ord och fraser       20.0  ####################
    struktur             15.0  ###############
    meningsrytm          13.2  #############

  rad 13      Månad med stor bokstav
              ”...en studie från September 2025 uppger 67% av svens...”
              Svenskan skriver september med liten bokstav. Engelskan
              versaliserar. Ett av de tydligaste tecknen på att texten
              tänkts på engelska.
              → september
```

Samma verktyg på en text skriven av en människa ger `0 fel` och `AI-lukt 0`.

### Faktavakten

Körs efter varje omskrivning och kontrollerar att inget som bär betydelse
försvunnit:

```bash
python skill/scripts/faktavakt.py original.md omskriven.md
```

Den fångar tappade tal, borttagna negationer (ett förlorat ”inte” vänder
meningen), ändrade produktnamn och kontaktuppgifter, och stoppar omskrivningar
som bytt ut mer än 55 procent av orden. Utgångskod 1 betyder att
omskrivningen ska kasseras.

## Tre lägen

1. **granska**, bara diagnos, ingen omskrivning
2. **humanisera**, skriver om det som flaggats, med sju spärrar mot att
   texten blir sämre
3. **lär-röst**, läser tre texter du själv skrivit och siktar på din rytm i
   stället för på ett generellt band

## Begränsningar, uttalade

**Trösklarna är riktvärden, inte kalibrerade mot en svensk korpus.** De tre
svenska studierna ger riktning, inte gränser. Hur det ska mätas in står i
[skill/KALIBRERING.md](skill/KALIBRERING.md).

**Underlaget är tunt.** Det finns tre svenska mätningar på AI-svenska. Den
största bygger på 57 texter av en texttyp från en modell. Resten av det
svenskspecifika är yrkesobservationer från språkkonsulter och lärare.

**Ingen har mätt hur AI-detektorer presterar på svensk text.** Det är den
största luckan i hela fältet.

**Poängen är ett bearbetningsbehov, aldrig en sannolikhet.**

## Källor

Varje påstående i verktyget har en källa, listade i
[`skill/references/ai-drag.md`](skill/references/ai-drag.md). De tre svenska
mätningarna:

- Arifovic, Linköpings universitet 2025, meningslängd och entropi,
  [DiVA](https://www.diva-portal.org/smash/get/diva2:1971262/FULLTEXT01.pdf)
- Lundberg, Lunds universitet 2024, klarspråk och avsändar-vi,
  [LUP](https://lup.lub.lu.se/student-papers/record/9159126/file/9159139.pdf)
- Suvanto m.fl., Chalmers och Edinburgh Napier 2026, klassificerare på
  riksdagsmotioner, [arXiv](https://arxiv.org/abs/2606.14209)

## Licens

MIT. Se [LICENSE](LICENSE).

Byggd av Jude Hwaijeh.

---

# Swedish humanizer (English)

Removes the AI smell from Swedish text. 66 patterns, 6 Swedish text types, and
a local scoring engine with zero dependencies.

Swedish AI text is usually thought in English and written in Swedish. It shows
in the structure before it shows in the word choice. This tool looks for that.

Most of what gives away Swedish AI text does not appear on any English list,
because the rules do not exist in English: Swedish quotation marks use the same
character at both ends, decimals use a comma, thousands use a hard space,
percent takes a space, headings capitalise only the first word, months and
weekdays and nationalities are lowercase, and the genitive takes no apostrophe.

**This is a style editor, not a detector evasion tool.** It never states a
probability that a text is AI generated, and it does not help present AI text
as human written.

Every claim is graded by evidence: measured in a Swedish study, observed by
several independent Swedish sources, or untested. Untested hypotheses are
documented and deliberately not acted on.

Requires Python 3.8+. Copy `skill/` into your skills directory. Documentation
is in Swedish, which is the point.

MIT licensed.
