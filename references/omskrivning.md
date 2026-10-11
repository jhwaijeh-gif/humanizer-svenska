# Hantverket: hur varje fynd rättas

Läs den här innan första omskrivningen. Den handlar om det svåra: att göra
texten bättre utan att göra den till någon annans.

## Grundhållningen

Du putsar. Du skriver inte om. En omskrivning där mer än hälften av orden är
utbytta är en ny text, och då har användaren förlorat sin egen röst utan att
ha bett om det. Faktavakten stoppar det vid 55 procent, men sikta mycket lägre.

**Ta bort och variera. Lägg aldrig till.**

Nästan varje fynd rättas genom strykning. Det är ingen slump. AI-text är sällan
fel, den är för mycket: en inledning före inledningen, en gardering före
påståendet, en sammanfattning efter slutet.

## De sju felmoderna, och hur du undviker dem

### 1. Fakta förvrängs

Det vanligaste allvarliga felet. "Senast 30 dagar" blir "inom en månad".
Ett "inte" försvinner. Ett "kan" blir "ska". Produktnamnet byts mot en
beskrivning.

Spärr: faktavakten. Kör den varje gång. Den kontrollerar tal, negationer,
modalverb, egennamn och kontaktuppgifter.

### 2. Rösten plattas ut

Verktyget får en egen husstil och trycker in varje text i den. Alla blir
korthuggna med du-tilltal och inga listor.

Spärr: mät textens egen baslinje först och flytta bara det som ligger utanför
bandet för genren. Är medianmeningen 17 ord i en rapport där bandet slutar vid
23, rör den inte. Rader som `granska` inte flaggat får inte röras.

### 3. Tillgjord slarvighet

Modellen strör in "ju", "väl", "faktiskt", "ärligt talat", medvetna småfel och
meningsfragment för att låta mänsklig. Resultatet luktar mer AI än originalet,
eftersom det är exakt vad en modell tror att mänskligt betyder.

Spärr: förbjudet att lägga till. Se listan sist i den här filen.

### 4. Bra text blir sämre

Ingen kontrollerar att resultatet faktiskt blev bättre.

Spärr: kör `granska` på resultatet. Är AI-lukten inte tydligt lägre, lämna
tillbaka originalet och säg att texten redan var bra.

### 5. Husstilen syns i andra omgången

Kör du `humanisera` två gånger ska den andra omgången ge noll ändringar.
Gör den inte det har verktyget en egen stil, och då är det trasigt.

### 6. Variationen höjs genom termbyte

Du ska höja ordvariationen och samtidigt inte byta termer. Det ser ut som en
motsägelse och är det inte.

Höj variationen genom att **stryka utfyllnad**: adjektiv som inte bär,
garderingar, upprepade övergångsord. Byt **aldrig** en fackterm, ett
produktnamn eller ett ord som betecknar samma sak genom texten.

### 7. Automatiska tecken-fixar förstör

Decimalkomma-regeln vill rätta `version 1.5`. Tusentalsmellanslag vill rätta
årtal och organisationsnummer. Genitivregeln vill rätta `McDonald's`.
Rubrikregeln vill göra `Google Workspace` till `google workspace`.

Spärr: skriptet hoppar över kodblock, URL:er, mejladresser och tabeller.
Rubrikversaler rättas alltid för hand, aldrig automatiskt.

---

## Fynd för fynd

### "i en värld där", "i dagens digitala landskap"

Stryk hela inledningen. Börja på den första meningen som säger något.

> **Före:** I en alltmer digitaliserad värld har AI blivit en integrerad del av
> hur moderna företag arbetar.
> **Efter:** (borttaget, texten börjar på nästa mening)

### "det är viktigt att notera att X"

Stryk inledningen, behåll X.

> **Före:** Det är viktigt att notera att deadline är den 5 maj.
> **Efter:** Deadline är 5 maj.

### "inte bara X utan också Y"

Välj den starkare halvan och stryk den andra, eller gör två meningar. Båda
halvorna bär sällan lika mycket.

> **Före:** Det handlar inte bara om effektivitet, utan också om hållbarhet.
> **Efter:** Det handlar om hållbarhet.

### "sammanfattningsvis"

Stryk hela sista stycket om det bara upprepar. Sluta på den sista konkreta
punkten, eller på en uppmaning.

### Urvattning

Ta bort ett av två osäkerhetsord, eller precisera.

> **Före:** Det kan potentiellt vara så att detta i många fall fungerar.
> **Efter:** Det kan fungera i många fall.

Undantag: myndighetstext och rapport, där förbehållet kan vara rättsligt
nödvändigt. Låt det stå och säg varför.

### För långa meningar

Leta efter **som**, **vilket**, **vilken** och **och som**. Där sitter skarven.
Dela där.

> **Före:** Många gånger går det att effektivisera processer som tidigare krävde
> omfattande manuellt arbete, vilket i sin tur leder till att medarbetarna kan
> fokusera på mer strategiska initiativ.
> **Efter:** Processer som tidigare krävde omfattande manuellt arbete går att effektivisera. Medarbetarna kan då fokusera på mer strategiska initiativ.

### Jämn puls

Skriv om en av tre meningar till en kort. Inte varannan, då blir rytmen lika
mekanisk åt andra hållet.

### Punktlista med fet ingress

Gör om till löptext, eller behåll listan men ta bort fetstilen och kolonet.

> **Före:** - **Datakvalitet**: En robust datagrund är en förutsättning.
> **Efter:** - Datagrunden måste vara städad innan ni börjar.

### För mycket punktlista

Två punkter är två meningar. En punkt är en mening. Behåll listan bara när den
har tre eller fler jämbördiga poster och ordningen inte spelar roll.

### Inget avsändar-vi

Skriv om passiva konstruktioner till aktiva med ett vi.

> **Före:** Kontakt tas inom ett dygn.
> **Efter:** Vi ringer upp inom ett dygn.

Gäller inte rapport och jobbansökan, där en annan avsändare är rätt.

### Frågerubrik

Skriv svaret i rubriken.

> **Före:** Hur fungerar det?
> **Efter:** Så går en beställning till

### Anglicism

Se tabellen i `ai-drag.md`. Regeln är alltid densamma: skriv det svenska ordet
för samma sak, eller stryk frasen helt om den inte bär något.

---

## Förbjudet att lägga till

Dessa får aldrig sättas in i en text som inte redan hade dem. Undantaget är
`lär-röst`, och bara när skribentens egna texter bevisligen innehåller dem.

- Talspråkspartiklar: ju, väl, nog, faktiskt, liksom, alltså, typ
- Inledningar: ärligt talat, för att vara helt ärlig, sanningen är att
- Avsiktliga stavfel eller grammatikfel
- Meningsfragment utan verb, om originalet inte har dem
- Utrop, emoji, versaler för betoning
- Personliga anekdoter eller exempel som inte fanns i originalet
- Siffror, källor, namn eller påståenden som inte fanns i originalet

Skälet är enkelt: ingen har mätt att dessa drag gör svensk text mer mänsklig.
Det är en hypotes, och den ligger i `vad-vi-inte-vet.md`. Att handla på en
otestad hypotes är precis hur en humanizer gör text sämre.
