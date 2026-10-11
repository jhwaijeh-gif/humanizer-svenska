# Vad vi inte vet

Den här filen finns för att vara ärlig om kunskapsläget. Inget här får styra en
omskrivning. Ett verktyg som handlar på otestade hypoteser gör text sämre, och
det är precis så humanizers får dåligt rykte.

## Hypoteser som låter rimliga och som ingen har mätt

### AI-svenska saknar talspråkspartiklar

Hypotesen: svensk AI-text saknar ju, väl, nog och faktiskt, och en enda
välplacerad partikel bryter AI-tonen.

**Status:** ingen källa, svensk eller engelsk, har mätt eller ens observerat
detta. Det som är belagt är att partiklarna finns och vad de gör. De hör
primärt hemma i talspråk och markerar talarens attityd till påståendet.
"Böcker är ju dyra" säger något annat än "Böcker är dyra".

Skrivrådsläget går dessutom emot dem. Chalmers skrivguide varnar för talspråk
i brukstext och listar just så, nog, väl, kanske och ju som ord att vara
försiktig med.

**Varför den är farlig:** att strö in partiklar är verktygets värsta felmod.
Resultatet läser som tillgjort och luktar mer AI än originalet, eftersom det
är precis vad en modell tror att mänskligt betyder. Därför står partiklarna på
förbudslistan i `omskrivning.md`.

**Hur den skulle testas:** ordräkning på egen AI-output mot ett svenskt
referensmaterial. En eftermiddags arbete. Ingen har gjort det.

### AI väljer av-konstruktion där svenskan bygger ihop ord

Hypotesen: AI skriver "utvecklingen av strategin" där en svensk skriver
"strategiutvecklingen".

**Status:** strukturskillnaden är belagd. Ett forskningsprojekt vid
Linnéuniversitetet studerar nominalfraser kontrastivt mellan engelska, svenska
och tyska, och svenskan löser kompression med sammansättning där engelskan
använder nominalfras. Det finns också en etablerad svensk språkvårdskritik mot
substantivsjuka.

**Vad som saknas:** att LLM-svenska gör detta oftare än mänsklig svenska. Ingen
har mätt det. Hypotesen är rimlig eftersom modellerna tränats på mer engelska,
men rimlig är inte sant.

**Extra skäl till försiktighet:** den krockar med Lix. Sänker du Lix trycker du
mot kortare ord, alltså mot av-konstruktioner, alltså mot det den här
hypotesen kallar ett AI-drag. Två råd som drar åt olika håll är ett tecken på
att minst ett av dem är fel.

### AI förväxlar sin, sitt, sina med hans, hennes, deras

**Status:** klassisk engelskinterferens hos människor som lär sig svenska.
Ingen källa kopplar den till LLM-output.

## Prövat och förkastat

### V2-ordföljden

Svenskan är ett V2-språk, engelskan inte, och hypotesen var att det skulle
läcka. Att V3 är den vanliga avvikelsen hos nya talare av svenska är belagt i
svensk forskning.

**Förkastad.** Moderna modeller klarar svensk ordföljd. Ordföljd är det första
en språkmodell lär sig. Draget togs medvetet bort ur verktyget.

### Engelska ordlistan i översättning

"Delve", "intricate", "meticulous", "testament", "realm", "tapestry". De är
välbelagda på engelska, med frekvensratio på mer än 25 gånger i vetenskapliga
abstracts.

**Går inte att översätta rakt av.** Svensk LLM-output genereras inte genom
ordbytesöversättning. De svenska ord som svenska praktiker faktiskt pekar ut
överlappar bara delvis med den engelska listan. Ingen svensk källa pekar ut
"testament", "sömlös" eller "dyka ner i".

Den som bygger en svensk ordlista genom att översätta den engelska jagar ord
som inte finns i svensk AI-output. Ordlistan i det här verktyget bygger på
svenska iakttagelser.

## Det som inte finns alls

| Letat efter | Status |
|---|---|
| Svensk frekvensstudie av överanvända ord i LLM-svenska | Finns inte. Varken Språkbanken Text, Isof eller DiVA har en korpusstudie som räknar ordfrekvenser i svensk AI-text mot svensk människotext |
| Isof-material om hur man känner igen AI-text | Finns inte. Isof har material om att *använda* AI för klarspråk, men pekar inte ut ett enda språkligt kännetecken |
| Mätning av anglicismer eller särskrivning i LLM-svenska | Finns inte. Bara iakttagelser |
| Svenska universitetsguider av typen "så känner du igen AI-text" | Finns knappt. Biblioteksguiderna handlar om etik och källhänvisning, inte om språk |
| KBLab-arbete om detektering av AI-genererad svenska | Finns inte. KBLab bygger språkmodeller, inte detektorer |
| Oberoende mätning av AI-detektorers träffsäkerhet på svensk text | **Finns inte.** Enda siffran som cirkulerar är en leverantörs egen marknadsföring |

Den sista raden är den största luckan i hela fältet. Se `KALIBRERING.md`.

## Källor

- https://writing.chalmers.se/se-upp-for-talsprak/
- https://spraktidningen.se/artiklar/partiklar/
- https://www.lnu.se/forskning/forskningsprojekt/projekt-att-oversatta-komplexitet-nominalfraser-i-engelsk-svensk-tysk-kontrast/
- https://spraknamnden.se/vad-ar-nominalisering/
- https://sv.wikipedia.org/wiki/V2-ordf%C3%B6ljd
- https://www.isof.se/download/18.6c60ddae17dc25fe7283e252/1643376647449/Rak%20och%20omv%C3%A4nd%20ordf%C3%B6ljd%20i%20f%C3%B6rortssvenska%20220118.pdf
- Kobak m.fl., Science Advances 2025, https://www.science.org/doi/10.1126/sciadv.adt3813
