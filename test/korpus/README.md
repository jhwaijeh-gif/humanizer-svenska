# Testkorpus

Tre grupper, samma tio ämnen, samma genre, jämförbar längd. Bara författaren
och skrivsättet varierar.

| Mapp | Vad | Ursprung |
|---|---|---|
| `manniska/` | 10 riksdagsmotioner, motiveringsdelen | Riksdagens öppna data, riksmötet 2020/21. Publicerade 2020, alltså två år före ChatGPT. Varje fil har en `.meta.json` med dok-id och länk |
| `ai/` | 10 motioner på samma ämnen, skrivna med omsorg | Modell 2026, som fick ämne, genre och ordantal men aldrig sett det här verktyget |
| `ai-standard/` | 10 motioner på samma ämnen, standardregister | Samma modell, minimal prompt, ingen hantverksinstruktion. Formaliahuvudet bortklippt så att bara brödtexten jämförs |

Formaliahuvudet ("Motion till riksdagen", ledamotens namn, "Förslag till
riksdagsbeslut") är bortklippt ur alla tre grupperna. Annars mäter man format
i stället för språk.

Fyra av de första människotexterna kasserades på PDF-artefakter, delade ord
och mellanslag före punkt. Kassationen gjordes innan någon poäng räknades.

Resultatet står i `test/RESULTAT.md`. Det är ett negativt resultat och det
ligger kvar.
