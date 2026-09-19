# Testtexter

Fixturer för att se att verktyget skiljer på rätt saker. Kör dem efter varje
ändring i `slopkoll.py` eller `monster.json`.

| Fil | Ska ge |
|---|---|
| `ai-text.md` | Hög AI-lukt och flera regelfel |
| `mansklig-text.md` | 0 i AI-lukt och 0 regelfel |
| `streck-em.md` | 2 regelfel, ett per em-streck |
| `streck-tankstreck-matt.md` | Inget alls. Tankstreck i måttliga doser är korrekt svenska |
| `streck-tankstreck-overdos.md` | Inget regelfel, men ett AI-luktfynd för täthet |

Den viktigaste raden är `mansklig-text.md`. Ett verktyg som flaggar korrekt
mänsklig svenska är värre än inget verktyg.
