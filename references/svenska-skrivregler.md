# Svenska skrivregler: korrekthetsaxeln

Allt på den här sidan är rätt eller fel svenska. Det har ingenting med AI att
göra. En människa som skriver fel gör samma fel. Skälet att det ändå hör hemma
i en humanizer är att felen nästan alltid är engelsk sättning som följt med in
i texten, och då är de samtidigt ett tecken på att texten tänkts på engelska.

Rätta alltid. Fråga inte.

## Skiljetecken

| Fel | Rätt | Varför |
|---|---|---|
| `—` em-streck | tankstreck `–` med mellanslag runt, eller komma | Em-strecket finns inte i svensk typografi. Det är amerikansk sättning. |
| `--` | tankstreck eller komma | Skrivmaskinsknep, inget svenskt skiljetecken. |
| `"citat"` engelska | `”citat”` | På svenska ser tecknet likadant ut i båda ändar. Engelskan vänder dem åt olika håll. |
| `"citat"` raka | `”citat”` | Raka citattecken pekas ut som tecken på att texten klistrats in direkt ur ett AI-svar. |
| `X, Y, och Z` | `X, Y och Z` | Oxfordkomma är engelsk standard. Svenskan sätter inget komma före och. |

## De två strecken, och varför de behandlas olika

Detta är den vanligaste förväxlingen i hela ämnet, så den får en egen rubrik.

| Tecken | Namn | Hur verktyget behandlar det |
|---|---|---|
| `—` | em-streck, långt | **Alltid fel.** Regelfel, varje förekomst räknas |
| `–` | tankstreck, kort | **Tillåtet.** Flaggas bara vid överanvändning, och då som AI-lukt, inte som fel |

**Det långa em-strecket finns inte i svensk typografi.** Det är amerikansk
sättning. Hittar du det i en svensk text har det kommit dit via engelska, och
det är därför det är den enskilt mest igenkända AI-markören i väst.

**Det korta tankstrecket är korrekt svenska** och har alltid funnits här.
Svenska skrivregler tillåter det med mellanslag runt. Att förbjuda det vore att
tvinga på läsaren en stilregel i språkregelns namn.

**Men täthet räknas.** En svensk rekryterare på Manpower Matchning formulerar
tröskeln så här: två eller tre gånger i en text går bra, men vid femte
förekomsten vet man att texten sannolikt är AI-skriven. Rekryteraren talar om
det långa strecket. Verktyget lånar tröskeln för det korta tankstrecket, vilket
är ett eget val och inte uppmätt. Det tillåter tre, eller tre per tusen ord i
längre texter (det större av de två), och flaggar däröver som AI-lukt.

Källorna går isär om det korta strecket. Språkkonsulterna och Frankly Media
räknar överanvändning som ett AI-drag. Please Copy Me argumenterar tvärtom att
det svenska tankstrecket inte är någon indikator alls. Den enda mätning som
finns gäller engelska och visar 0,0 till 9,1 per tusen ord beroende på modell,
alltså är frekvensen modellspecifik snarare än språkspecifik.

Vill du förbjuda även det korta strecket är det ett stilval, inte en språkregel,
och då kör du `--inga-tankstreck`.

## Tal

| Fel | Rätt |
|---|---|
| `3.14` | `3,14` (komma är decimaltecken) |
| `1,500` | `1 500` (hårt mellanslag, inte komma) |
| `85%` | `85 %` (mellanslag före tecknet) |
| `2:00 PM` | `kl. 14.00` (24-timmarsklocka, punkt) |
| `September 19, 2026` | `19 september 2026` eller `2026-09-19` |

Fyrsiffriga tal skrivs utan mellanslag när de är årtal: `2026`, inte `2 026`.
Postnummer, organisationsnummer och telefonnummer följer sina egna format och
ska lämnas i fred.

## Versaler

Svenskan skriver med **liten** bokstav det som engelskan versaliserar:

- Månader: januari, februari, mars
- Veckodagar: måndag, tisdag, onsdag
- Språk: svenska, engelska, tyska
- Nationalitetsord: svensk, amerikansk, nordisk

**Rubriker:** bara första ordet och egennamn får versal. `Så kommer du igång`,
inte `Så Kommer Du Igång`. Title Case är engelsk standard och är ett av de
mest tillförlitliga tecknen på översatt struktur, eftersom det är ett rent
regelbrott och inte en smaksak.

Rubriker rättas för hand. Ett skript kan inte veta vad som är egennamn.

## Genitiv

Svenskan skriver `Judes bok`, inte `Jude's bok`. Apostrofen är engelsk.

Undantag: namn som slutar på s, x eller z tar apostrof utan s, `Lars' bok`.
Utländska varumärken behåller sin egen stavning, `McDonald's`.

## Bestämd form

Engelskan har ingen bestämd ändelse, svenskan har det, och det läcker.

- Fel: `det dagliga arbete`
- Rätt: `det dagliga arbetet`

## Särskrivning

Svenskan bygger ihop ord. Engelskan gör det inte.

- Fel: `AI lösningar`, `arbets flöden`, `Content marketing strategi`
- Rätt: `AI-lösningar`, `arbetsflöden`, `contentmarketingstrategi`

Ett skript kan inte hitta särskrivningar utan ordlista. Läs efter för hand,
särskilt i sammansättningar med engelska lånord.

## Tilltal

Du eller ni, konsekvent genom hela texten. Växling mellan dem i samma text är
ett vanligt fel i AI-översatt svenska.

Du är säkrare. Myndigheternas skrivregler konstaterar att du är det normala
tilltalet i allmän information riktad till stora grupper. Få störs av du, fler
störs av ni.

## Källor

- Svenska skrivregler via Chalmers skrivguide,
  https://writing.chalmers.se/chalmers-skrivguide/skrivregler-och-stil/832-2/
- Myndigheternas skrivregler, Ds 2009:38,
  https://www.riksdagen.se/sv/dokument-och-lagar/dokument/departementsserien/myndigheternas-skrivregler_gxb438/html/
- Om citattecken, Ulrika Gotthardsson,
  https://se.linkedin.com/pulse/word-hack-5-f%C3%B6rsvenska-dina-citattecken-ulrika-gotthardsson
- Om du-tilltal, https://www.iklartext.se/anvand-du-tilltal/
- Om tankstrecket, båda hållningarna:
  https://sprakkonsulterna.se/kvalitetssakra-dina-ai-texter-5-rad/ och
  https://pleasecopyme.se/2025/09/tankstrecket-gor-comeback-men-har-ju-alltid-varit-har/
- Modellskillnader i tankstreck, Freeburg 2026, https://arxiv.org/abs/2603.27006
- Särskrivning och engelskinfluerad kommatering,
  https://aikompassen.com/artiklar/ai-korrekturlasning-svenska-texter/
