# AI-drag i svensk text, med bevisgrad

Varje drag har en gradering. Graderingen styr vad du får göra med fyndet.

- **[mätt]** uppmätt i en svensk studie. Rättas.
- **[observerat]** flera oberoende svenska källor pekar ut draget, ingen har
  mätt frekvensen. Föreslås, med skäl.

Det som ingen har mätt eller observerat står i `vad-vi-inte-vet.md` och
används inte.

---

## [mätt] De tre drag som faktiskt är uppmätta på svensk AI-text

Det här är hela den svenska evidensbasen. Tre studier, alla små.

### 1. Meningslängd

Arifovic, Linköpings universitet 2025. 57 texter av svenska lärarstudenter mot
57 texter från Gemini 2.5 Pro.

| Mått | Människa | AI |
|---|---|---|
| Vanligaste meningslängd | 19 ord | 28 ord |
| Median | 20 ord | 23 ord |

**Det viktiga är inte medellängden utan variationen.** Mänsklig svenska hoppar
mellan korta och långa meningar. AI håller jämn puls. En mening på sex ord
efter en på tjugofem är den mänskliga signaturen.

Observera att låg spridning i en text av genomgående korta meningar inte är ett
AI-tecken. Det är matematik. Verktyget flaggar bara jämn puls när meningarna
samtidigt är långa.

Begränsning som författaren själv skriver ut: en texttyp, en modell. Inte
generaliserbart till all svensk text.

https://www.diva-portal.org/smash/get/diva2:1971262/FULLTEXT01.pdf

### 2. Ordvariation

Samma studie. AI-texterna använde 4 468 unika ord mot människornas 4 861,
trots att AI-materialet var 25 procent större. Shannonentropi 9,1598 mot
9,3233, statistiskt säkerställt, p ungefär 0,000004.

**Höj variationen genom att stryka utfyllnad, aldrig genom att byta termer.**
Synonymväxling på facktermer bryter textbindningen och är i sig ett AI-drag
som svenska språkkonsulter pekar ut. Samma sak ska heta samma ord.

Mäts inte på texter under 200 ord. Där är siffran brus.

### 3. Avsändar-vi saknas

Lundberg, Lunds universitet 2024. Sex klarspråksanpassade myndighetstexter,
tre av ChatGPT-4 och tre av mänskliga språkkonsulter.

Resultatet är kontraintuitivt: skillnaderna var i huvudsak individuella, inte
mellan grupperna. Alla sex texter klarade samtliga klarspråksråd. En enda
skillnad gick rakt igenom, och uppsatsen formulerar den så:

> "Att det saknas vi-perspektiv i de AI-genererade texterna är den enda
> otvetydiga skillnaden mellan grupperna."

Alla texter, både AI och människa, tilltalade läsaren med du. Bara de
mänskliga hade ett vi från avsändaren.

Uppsatsen refererar också Janouch 2023, där formuleringar med ordet vi bidrog
till att läsare trodde att en text var skriven av en människa.

**Åtgärden:** skriv vad ni gör, inte vad som görs. "Vi ringer upp inom ett
dygn", inte "Kontakt tas inom ett dygn".

Begränsning: sex texter, en genre. Verktyget kräver därför bara vi i de
profiler där en avsändare rimligen ska synas.

https://lup.lub.lu.se/student-papers/record/9159126/file/9159139.pdf

---

## [observerat] Drag som svenska källor pekar ut men ingen mätt

Fyra oberoende svenska källor. Överlappet mellan dem är det som väger. Ingen
frekvensmätning finns.

### Anglicismer, den verkliga svenska AI-lukten

Svensk AI-text är oftast tänkt på engelska. Det syns i konstruktionen före det
syns i ordvalet, och detta är sannolikt mer träffsäkert än ordlistan nedan.

| Skriver | Betyder egentligen | Skriv i stället |
|---|---|---|
| i en värld där, i dagens digitala landskap | in a world where | stryk inledningen |
| på daglig basis | on a daily basis | dagligen |
| i termer av | in terms of | när det gäller, eller stryk |
| när det kommer till | when it comes to | vad gäller |
| adressera problemet | address the issue | ta itu med, hantera |
| spelar en avgörande roll | plays a crucial role | säg vad saken gör |
| ta det till nästa nivå | take it to the next level | säg vad som blir bättre |
| lås upp din potential | unlock your potential | säg vad läsaren får |
| är här för att stanna | is here to stay | stryk |
| det rekommenderas att | it is recommended | vi rekommenderar |
| ha en inverkan på | have an impact on | påverkar |
| skräddarsydda lösningar | tailored solutions | säg vad ni gör annorlunda |

### Ordlistan

Utpekade av SEO.se och SprayPassagen: banbrytande, oumbärligt, navigera,
avgörande, noggrann, korrekt, utforska, upptäck, vital, välrenommerad,
designad för att, välinformerad, idealiskt.

**Enstaka förekomst är aldrig ett fel.** Flera av orden är helt normal svenska.
Upptäck är standard i svensk e-handel. Avgörande och noggrann skriver folk hela
dagarna. Bara täthet räknas, och bara när flera olika ord ur listan uppträder
tillsammans.

### Fraserna

- "sammanfattningsvis", "sammanfattningsvis kan vi konstatera", "avslutningsvis"
- "det är viktigt att notera", "det är värt att notera"
- "inte bara X utan också Y", den mest igenkända AI-satsbyggnaden som finns
- "det handlar inte om X, det handlar om Y"
- "det råder ingen tvekan om att"
- "låt oss titta närmare på"
- "hitta balansen mellan", "å ena sidan, å andra sidan"
- "två sidor av myntet"
- "det återstår att se"
- "i den här artikeln kommer vi att"
- "här är X saker du behöver veta"

### Urvattning

Utpekat av SEO.se: "det kan bli si och så", "många gånger går det att",
"det är alltid bäst att". Konstruktionen gör påståendet obestridligt och
därmed innehållslöst.

Räknas inte i myndighetstext och rapport, där förbehåll ofta är nödvändiga.

### Ordval som glider bort från etablerad term

Svenska språkkonsulter pekar ut ett mönster som engelska listor saknar: AI
byter ut vedertagna termer mot vagare eller ovanligare ord. Deras exempel är
att "dö" blev "omkomma". De pekar också ut onödig synonymväxling som förstör
textbindningen, att samma sak omväxlande kallas finansiering, medel och stöd.

Detta är motsatsen till det engelska problemet. Där handlar det om överanvända
ord, här om onödig variation som bryter mot klarspråksprincipen att samma sak
ska heta samma sak.

### Struktur

- Punktlista där varje punkt börjar med ett fetstilt ord och kolon
- Punktlistor i stället för formulerade samband
- Tomma frågerubriker, "Hur fungerar det?" i stället för "Så ansöker du"
- Uppräkningar genomgående i grupper om tre
- Positivt laddade adjektiv före ämnet: fantastiska, imponerande, magnifika
- Ekoavslutning: sista stycket upprepar inledningens ord

### Metatext

Rester från chattfönstret: "Här är en omskriven version", "Hoppas detta
hjälper", "Som en AI-språkmodell". Ska aldrig finnas i en färdig text.

---

## Vad en ordlista inte kan

Mattias Wahde, som byggt den svenska klassificerare som fann att 9,4 procent
av riksdagsmotionerna 2025/26 innehöll minst ett stycke med AI-assisterat
innehåll, säger
uttryckligen att "det går inte att säga att enskilda ord är AI-ord, det är
mer komplext än så".

En humanizer som bara byter ut ord på en svartlista flyttar problemet, den
löser det inte. Meningslängdsvariationen och vi-perspektivet är de två ingrepp
som har mätstöd. Resten är omdöme.

https://arxiv.org/abs/2606.14209

Citatet och siffran 9,4 procent står på Chalmers nyhetssida om studien:
https://www.chalmers.se/aktuellt/nyheter/me-riksdagspolitiker-tar-hjalp-av-ai-nar-de-skriver-motioner-utan-att-redovisa-det/

---

## Källor

**Svenska mätningar**
- Arifovic, LiU 2025, https://www.diva-portal.org/smash/get/diva2:1971262/FULLTEXT01.pdf
- Lundberg, LU 2024, https://lup.lub.lu.se/student-papers/record/9159126/file/9159139.pdf
- Suvanto m.fl., Chalmers och Edinburgh Napier 2026, preprint, https://arxiv.org/abs/2606.14209

**Svenska iakttagelser**
- https://sprakkonsulterna.se/kvalitetssakra-dina-ai-texter-5-rad/
- https://pedagog.malmo.se/bloggposter/kan-man-upptacka-ai-genererade-texter/
- https://seo.se/upptack-ai-text/
- https://spraypassagen.se/artiklar/humanize-ai-text-svenska
- https://aikompassen.com/artiklar/ai-korrekturlasning-svenska-texter/
- https://www.grundskoleboken.se/wiki/Bed%C3%B6m_om_en_text_%C3%A4r_skriven_av_en_AI
- https://www.realtid.se/karriar-ledarskap/tre-ord-forstor-din-jobbansokan-nu-avslojas-ai-tricken/

**Engelsk forskning, för sammanhang**
- Kobak m.fl., Science Advances 2025, https://www.science.org/doi/10.1126/sciadv.adt3813
- Liang m.fl., https://arxiv.org/abs/2404.01268
- Juzek & Ward, COLING 2025, https://aclanthology.org/2025.coling-main.426.pdf

**Om källkvalitet:** SEO.se, SprayPassagen och AIkompassen är kommersiella
sajter som säljer tjänster i närheten av ämnet. Deras iakttagelser räknas som
observerade när flera av dem säger samma sak oberoende, aldrig som mätning.
Språkkonsulterna och Pedagog Malmö är yrkesverksamma språkarbetare utan
produkt i frågan och väger något tyngre.
