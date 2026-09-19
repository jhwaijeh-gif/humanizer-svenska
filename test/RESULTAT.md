# Blindtest 2026-09-19

Verktyget testades mot riktig svenska. Resultatet är delvis negativt och det
ligger kvar här i sin helhet, eftersom ett verktyg som bara visar upp sina
träffar inte går att lita på.

## Uppställningen

Trettio texter i en genre, riksdagsmotioner, närmare bestämt den argumenterande
motiveringsdelen. Ämne, genre och ungefärlig längd hölls fasta. Bara
författaren och skrivsättet varierade.

| Grupp | n | Ursprung |
|---|---|---|
| Människa | 10 | Riksdagens öppna data, riksmötet 2020/21. Publicerade 2020, två år före ChatGPT. Både datum och mänskligt upphov är säkert |
| AI omsorgsfull | 10 | Modell från 2026 som fick ämne, genre och ordantal men aldrig sett verktyget, och uttryckligen instruerades att inte följa några skrivregler från projektet |
| AI standardregister | 10 | Samma modell, minimal prompt, inga hantverksinstruktioner. Det en vanlig användare får |

Formaliahuvudet klipptes bort ur alla tre grupperna. Annars hade testet mätt
dokumentformat i stället för språk. Fyra människotexter kasserades på
PDF-artefakter innan någon poäng räknades.

## Resultat

Profil `rapport`, efter omviktningen som testet föranledde.

| Grupp | Median AI-lukt | Alla värden | Regelfel |
|---|---|---|---|
| Människa | 0 | 0, 0, 0, 0, 0, 0, 8, 10, 12, 12 | 0 |
| AI omsorgsfull | 0 | 0, 0, 0, 0, 0, 0, 3, 6, 8, 23 | 0 |
| AI standardregister | 7 | 0, 0, 0, 3, 6, 8, 9, 9, 15, 25 | 0 |

## Vad som underkändes

**Verktyget skiljer inte AI-skriven svenska från mänsklig svenska i den här
genren.** AI-texter skrivna med omsorg fick samma median som människorna.
Mot standardregistret ger bästa möjliga tröskel 13 rätt av 20, mot 10 för ren
slump. Det är inte en detektor och ska aldrig användas som en.

**Rytmsignalen vände.** Verktyget byggde på Arifovic, LiU 2025, som fann att
AI-svenska hade längre och jämnare meningar än mänsklig svenska. Den studien
använde Gemini 2.5 Pro. Mot en modell från 2026 replikerade fyndet inte:

| | Medianmening | Spridning | Lix |
|---|---|---|---|
| Människa | 18,5 | 7,4 | 50 |
| AI omsorgsfull | 17,0 | **9,7** | 42 |
| AI standardregister | 14,0 | 6,5 | 53 |

De omsorgsfulla AI-texterna varierade mer i meningslängd än
riksdagsledamöterna. Rytmen vägde tyngst av alla komponenter, 25 av 100, och
är efter testet nedflyttad till 12.

**Ordlistan träffade ingenting.** En riksdagsmotion innehåller inte ”lås upp
din potential”. Ordlistan är byggd för marknadsföringstext och testades på
formell sakprosa. Det är en begränsning i testet lika mycket som i verktyget.

## Vad som godkändes

**Noll regelfel på trettio texter.** Verktyget larmar inte på korrekt svenska.
Det var den viktigaste frågan, eftersom ett verktyg som flaggar välskriven
svenska är värre än inget verktyg.

**Den uppenbara AI-tonen fångas.** Det är vad verktyget faktiskt är till för.

| Text | AI-lukt | Regelfel |
|---|---|---|
| Svensk text i chattregister, med marknadsföringsslop | **85** | 6 |
| Svensk text skriven av en människa | **0** | 0 |

Skillnaden mellan 85 och 0 är verklig och det är den skillnaden användare
menar när de säger att något låter som AI.

## Tre fel som testet avslöjade, alla åtgärdade

1. **”Europeiska unionen”** flaggades som nationalitetsord med felaktig versal.
   Det är ett egennamn. Undantagslista tillagd.
2. **Oxfordkomma** hade tre falska larm av fem träffar. Regeln flaggade komma
   mellan huvudsatser, vilket är korrekt svenska. Ett reguljärt uttryck kan
   inte skilja en uppräkning från två satser. Regeln är flyttad från
   korrekthetsaxeln till AI-lukt som ett fynd märkt ”kontrollera själv”.
3. **”många gånger”** flaggades som urvattning i meningen ”skiftar många gånger
   från dag till dag”, alltså bokstavlig betydelse. Frasen är borttagen ur
   regeln.

Rättningarna gjordes efter att testet körts och redovisats, inte under tiden.

## Vad testet inte visar

- En genre. Riksdagsmotioner är inte vad verktyget främst är byggt för.
  Kundmejl, sajttext och LinkedIn-inlägg är otestade, och det är där
  ordlistan bor.
- Trettio texter. Litet.
- En modellfamilj på AI-sidan.
- Omskrivningsläget är inte testat alls. Bara diagnosen.

Nästa test ska göras i rätt genre. Det svåra där är att hitta svensk
människotext som säkert är skriven före november 2022.

## Så kör du om det

```bash
python test/blindtest.py --profil rapport
```

Korpusen ligger i `test/korpus/` med källhänvisning per människotext.
