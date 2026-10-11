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

Kopiera mappen `skill/` till din skills-katalog och döp den till `svensk-humanizer`:

```
~/.claude/skills/svensk-humanizer/
```

Kräver Python 3.8 eller senare. Inga paket och ingen nätverkstrafik, mätdelen körs lokalt.

## Användning

Be om det i vanlig text, till exempel "humanisera den här texten" eller "låter det här som AI?".

Mätdelen går också att köra direkt:

```bash
python skill/scripts/slopkoll.py text.md --profil sajttext
```

Profiler: `kundmejl`, `sajttext`, `linkedin`, `myndighet`, `ansokan`, `rapport`, `allman`.

```bash
python skill/scripts/faktavakt.py original.md omskriven.md
```

## Begränsningar

- Trösklarna är inte kalibrerade. Hur det skulle gå till står i [`skill/KALIBRERING.md`](skill/KALIBRERING.md).
- Underlaget är tunt. Mycket av det svenskspecifika är iakttagelser, inte mätningar.
- Blindtestet gav ett delvis negativt resultat. Hela testet, inklusive det som underkändes, står i [`test/RESULTAT.md`](test/RESULTAT.md).
- Ingen har mätt hur AI-detektorer presterar på svensk text, och inte jag heller.
- Poängen är ett bearbetningsbehov, aldrig en sannolikhet.

Underlaget bakom mönstren ligger i [`skill/references/ai-drag.md`](skill/references/ai-drag.md). Jag har inte granskat det så noga att jag står för varje detalj.

## Licens

MIT. Se [LICENSE](LICENSE).

Byggd av Jude Hwaijeh.

---

# Humanizer for Swedish (English)

A Claude Skill that removes the AI smell from Swedish text. I built it for my own use and I am publishing it as is. It is not scientific: the thresholds are uncalibrated, and my own blind test (in `test/RESULTAT.md`) shows it catches obvious AI tone but not carefully written AI Swedish. It is a style editor, not a detector evasion tool. Documentation is in Swedish.

Install: copy `skill/` to `~/.claude/skills/svensk-humanizer/`. Requires Python 3.8+. MIT licensed.
