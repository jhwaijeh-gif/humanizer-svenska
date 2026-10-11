# Humanizer för svenska

En Claude Skill som tar bort AI-lukten ur svensk text. Jag har byggt den för eget bruk.

> **Det här är ett verktyg för eget bruk, inte forskning.** Jag publicerar det som det är. Trösklarna är riktvärden som inte är kalibrerade mot någon svensk korpus. Mina egna tester ligger i [`test/`](test/) och visar att verktyget fångar den uppenbara AI-tonen men inte svenska som en modell skrivit med omsorg. Se det som en stilhjälp, inte som en dom över om en text är skriven av AI.

## Vad den gör

Hittar sådant som får svensk text att låta översatt eller maskinskriven: engelsk typografi (citattecken, decimalpunkt, rubriker med stora bokstäver), översatta konstruktioner, tomma formuleringar och jämn maskinrytm. Den förklarar varje fynd och kan skriva om texten.

Tre lägen:

1. **granska**: bara diagnos, ingen omskrivning
2. **humanisera**: skriver om det som flaggats, med spärrar så att texten inte blir sämre och inget sakinnehåll ändras
3. **lär-röst**: läser tre texter du själv skrivit och siktar på din rytm

Det finns också en faktavakt som kontrollerar att tal, negationer, namn och kontaktuppgifter finns kvar efter en omskrivning.

## Vad den inte gör

Den hjälper inte text att undgå AI-detektorer, den anger aldrig hur sannolikt det är att en text är AI-genererad, och den framställer inte AI-text som människoskriven. Det är ett verktyg för att skriva bättre svenska.

## Installation

Skillen heter `svensk-humanizer`. Den behöver Python 3.8 eller senare för mätdelen. Skripten har inga beroenden och gör inga nätverksanrop. I Claude Code och Codex körs de på din dator, i Claude.ai och ChatGPT i tjänstens egen miljö. Texten du ber om hjälp med går alltid till modellen.

### Claude (Claude.ai och Claude Desktop)

Ladda ner `svensk-humanizer.zip` från [Releases](https://github.com/jhwaijeh-gif/humanizer-svenska/releases/latest). Gå till **Customize > Skills**, tryck på **+**, välj **+ Create skill**, sedan **Upload a skill**, och välj ZIP-filen. Kräver att *Code execution and file creation* är på under Settings > Capabilities.

Det finns också en genväg som inte är beskriven som installationsväg i Anthropics hjälpartiklar. Skriv i en chatt:

```
Make this a skill and name it svensk-humanizer: https://github.com/jhwaijeh-gif/humanizer-svenska
```

Jag har provat det här på ett Max-konto: Claude hämtade filerna från GitHub och visade ett kort med knappen **Save skill**, som man trycker på själv. Därefter låg skillen kvar under Customize > Skills och syntes som `/svensk-humanizer` i en ny chatt. Uppladdning av ZIP är den väg som Anthropic dokumenterar.

### Claude Code

```
/plugin marketplace add jhwaijeh-gif/humanizer-svenska
/plugin install svensk-humanizer@humanizer-svenska
```

Eller med Skills CLI:

```
npx skills add jhwaijeh-gif/humanizer-svenska --global --agent claude-code
```

### ChatGPT

Enligt OpenAIs hjälpsida finns skills i ChatGPT för Business, Enterprise, Healthcare och Edu, inte för vanliga privatkonton. Gå till **Plugins > Skills > Create > Upload from your computer** och ladda upp `svensk-humanizer.zip`. Om ditt konto saknar det valet går det inte att installera där.

### Codex och andra agenter

```
npx skills add jhwaijeh-gif/humanizer-svenska --global --agent codex
```

Eller kopiera filerna till agentens skills-mapp och döp mappen till `svensk-humanizer`.

## Vad jag testat

Allt som inte står som testat är ej testat.

| Väg | Status |
|---|---|
| Mätdelen på lokala texter (`python scripts/slopkoll.py`) | Testat, se [`test/`](test/) |
| Claude.ai, uppladdning av ZIP | Ej testat |
| Claude.ai, via chatten | Testat 2026-10-11 på ett Max-konto: hämtades från GitHub, sparades och syntes som `/svensk-humanizer` |
| Claude Code, plugin | Manifesten godkända av `claude plugin validate`, installationen ej testad |
| `npx skills add` | Ej testat |
| ChatGPT | Ej testat, och kräver ett konto där skills finns |

## Användning

Be om det i vanlig text, till exempel "humanisera den här texten" eller "låter det här som AI?". Eller skriv `/svensk-humanizer`.

Mätdelen går också att köra direkt från repots rot:

```bash
python scripts/slopkoll.py text.md --profil sajttext
python scripts/faktavakt.py original.md omskriven.md
```

Profiler: `kundmejl`, `sajttext`, `linkedin`, `myndighet`, `ansokan`, `rapport`, `allman`.

## Begränsningar

- Trösklarna är inte kalibrerade. Hur det skulle gå till står i [`KALIBRERING.md`](KALIBRERING.md).
- Underlaget är tunt. Mycket av det svenskspecifika är iakttagelser, inte mätningar.
- Blindtestet gav ett delvis negativt resultat. Hela testet, inklusive det som underkändes, står i [`test/RESULTAT.md`](test/RESULTAT.md).
- Ingen har mätt hur AI-detektorer presterar på svensk text, och inte jag heller.
- Poängen är ett bearbetningsbehov, aldrig en sannolikhet.

Underlaget bakom mönstren ligger i [`references/ai-drag.md`](references/ai-drag.md). Jag har inte granskat det så noga att jag står för varje detalj.

## Säkerhet

Skripten i `scripts/` läser bara de textfiler du pekar ut och skriver till terminalen. De gör inga nätverksanrop och skriver inga filer. Läs dem gärna innan du installerar, det är vanlig Python utan beroenden. `test/blindtest.py` är bara till för mina egna tester.

## Licens

MIT. Se [LICENSE](LICENSE).

Byggd av Jude Hwaijeh.

---

# Humanizer for Swedish (English)

A Claude Skill that removes the AI smell from Swedish text. I built it for my own use and I am publishing it as is. It is not scientific: the thresholds are uncalibrated, and my own blind test (in `test/RESULTAT.md`) shows it catches obvious AI tone but not carefully written AI Swedish. It is a style editor, not a detector evasion tool. Documentation is in Swedish.

Install: download `svensk-humanizer.zip` from Releases and upload it as a skill, or in Claude Code run `/plugin marketplace add jhwaijeh-gif/humanizer-svenska`. Requires Python 3.8+. MIT licensed.
