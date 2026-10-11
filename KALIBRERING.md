# Kalibrering: varför siffrorna är riktvärden

**Inget är kalibrerat mot en svensk korpus. Rytmtrösklarna sänktes efter ett
rimlighetstest på tio texter i en genre. Allt annat är riktvärden.**

Den 19 september 2026 kördes ett blindtest mot tio riksdagsmotioner från 2020.
Lägsta spridning i meningslängd bland dem var 5,5 ord, och verktygets tröskel
låg på 6,0 till 7,0 beroende på profil. Den flaggade alltså korrekt mänsklig
svenska. Trösklarna sänktes till 5,0. Samma test visade att LiU-mätningens
rytmfynd inte replikerar mot en modell från 2026, varför rytmen vägdes ner från
25 till 12 poäng. Se `../test/RESULTAT.md`.

Det står i utdatan varje gång verktyget körs, och det står här. Det är den
viktigaste begränsningen och den ska inte döljas.

## Vad som är sant och vad som är gissat

De tre drag som är märkta `[mätt]` bygger på riktiga svenska studier. Men
studierna ger **riktning**, inte trösklar.

| Vad vi vet | Vad verktyget gör med det |
|---|---|
| AI-texternas typvärde låg på 28 ord, människornas på 19 (57 mot 57 texter, en texttyp, en modell) | Sätter olika tak per profil: 14 för LinkedIn, 23 för rapport. **Talen är valda, inte mätta.** |
| AI-texter använde färre unika ord | Flaggar under 0,70 i rullande fönster. **Tröskeln är vald, inte mätt.** |
| AI-texter saknade avsändar-vi (sex myndighetstexter) | Kräver vi i tre av sju profiler (kundmejl, sajttext och myndighet). **Urvalet är omdöme, inte mätning.** |

Viktningen i poängen är också vald. Att anglicismer får högst 20 poäng och
tilltal högst 12 bygger på en bedömning av hur mycket de stör en svensk läsare,
inte på data.

## Hur det ska mätas in

En dags arbete, och det skulle göra talen sanna.

1. **Samla mänskliga svenska texter, 50 per profil.** Från källor som säkert
   är skrivna före november 2022: riksdagsmotioner, myndigheters egna sidor
   från arkiv, tidningsartiklar, personliga bloggar. Datumet är viktigt, allt
   efter det kan vara AI-bearbetat.
2. **Samla AI-texter, 50 per profil, från minst tre olika modeller.** Samma
   uppgifter, samma ämnen. Tre modeller eftersom vissa drag är modellspecifika
   snarare än språkspecifika. Det är belagt för tankstreck, där frekvensen
   varierar från 0,0 till 9,1 per tusen ord beroende på modell.
3. **Kör `slopkoll.py --json` på allt.**
4. **Sätt trösklarna där de faktiskt skiljer.** Målet är att nästan alla
   mänskliga texter ska hamna lågt. Ett verktyg som flaggar korrekt mänsklig
   svenska är värre än inget verktyg.
5. **Skriv upp den falska positiv-andelen per profil** och publicera den.

## Varför det här spelar större roll än det låter

Liang m.fl. publicerade i Patterns 2023 att AI-detektorer flaggade i genomsnitt
61,22 procent av texter skrivna av personer med engelska som andraspråk som
AI-genererade, mot 5,19 procent för amerikanska högstadieelever. 97,80 procent
flaggades av minst en av sju detektorer.

Svensk text löper med all sannolikhet samma risk, och **ingen har mätt det.**
Enda siffran som cirkulerar för svenska är en leverantörs egen marknadsföring.

Det betyder två saker. Att det finns ett verkligt hål i kunskapsläget som
någon borde fylla. Och att varje verktyg i den här kategorin, inklusive det
här, ska vara försiktigt med att påstå något om hur AI-lik en text är.

https://www.cell.com/patterns/fulltext/S2666-3899(23)00130-7

## Tills dess

Verktyget säger vad det vet och hur det vet det. Ett fynd märkt `[observerat]`
säger att svenska språkarbetare pekat ut draget, inte att någon räknat. Ett tal
kallas bearbetningsbehov, aldrig sannolikhet.

Det är inte en brasklapp. Det är skillnaden mellan ett verktyg som går att lita
på och ett som låter säkrare än det är.
