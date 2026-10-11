#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slopkoll.py, mätdelen av svensk-humanizer.

Räknar det som går att räkna i en svensk text och håller sig borta från det
som kräver omdöme. Inga beroenden utanför standardbiblioteket.

    python slopkoll.py text.md
    python slopkoll.py text.md --profil kundmejl
    python slopkoll.py text.md --json
    type text.md | python slopkoll.py -

TVÅ AXLAR, som aldrig blandas ihop:

  Korrekthet   brott mot svenska skrivregler. Rätt eller fel svenska, helt
               oberoende av vem som skrivit texten. Ska vara 0.

  AI-lukt      0 till 100, lägre är bättre. Drag som gör att texten läser
               som AI. Varje fynd bär sin bevisgrad:
                 [mätt]        uppmätt i en svensk studie. Bara tre saker
                               kvalificerar: meningslängd, ordvariation,
                               avsändar-vi.
                 [observerat]  flera oberoende svenska källor pekar ut draget,
                               ingen har mätt frekvensen.

VAD VERKTYGET FÅNGAR, OCH VAD DET INTE FÅNGAR

Det fångar den uppenbara AI-tonen: chattregistret, marknadsföringsslopet,
de översatta konstruktionerna. Det är vad de flesta menar när de säger att en
text låter som AI, och det är vad verktyget är byggt för.

Det fångar INTE svenska som en modell skrivit med omsorg. Mätt i ett blindtest
mot tio riksdagsmotioner från 2020: AI-texter skrivna med omsorg fick samma
median som människorna. Se test/RESULTAT.md. Verktyget är en stilredigerare,
ingen detektor, och det säger aldrig hur sannolikt det är att en text är
AI-genererad.

Rytmtrösklarna sänktes efter ett rimlighetstest på tio texter i en genre.
Resten är riktvärden. Se KALIBRERING.md.
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HAR = os.path.dirname(os.path.abspath(__file__))
MONSTERFIL = os.path.join(HAR, "monster.json")

# Referensvärden ur Arifovic, LiU 2025 (57 mänskliga mot 57 AI-texter,
# lärarstudenters matematikdidaktiska svar mot Gemini 2.5 Pro).
# En texttyp, en modell. Referens, inte facit.
MANSKLIG_TYPVARDE = 19
AI_TYPVARDE = 28
MANSKLIG_MEDIAN = 20
AI_MEDIAN = 23

MIN_ORD_FOR_POANG = 80      # under detta är all statistik brus
MIN_ORD_FOR_VARIATION = 200  # ordvariation kräver mer text än så

FORKORTNINGAR = {
    "t.ex", "bl.a", "dvs", "d.v.s", "osv", "o.s.v", "m.m", "m.fl", "etc",
    "kl", "ca", "nr", "fr.o.m", "t.o.m", "s.k", "resp", "jfr", "enl",
    "inkl", "exkl", "st", "kr", "milj", "mdr", "obs", "dr", "prof",
    "fig", "tab", "ev", "bl", "e.d", "p.g.a", "s", "sid", "kap", "avd",
    "f.d", "m.a.o", "i.o.m", "u.a", "vol", "nr", "ref", "resp",
}

# Versala ord som inte ska flaggas mitt i mening.
EGENNAMN_UNDANTAG = {
    "AI", "EU", "FN", "SEO", "VD", "IT", "PDF", "API", "USA", "GDPR", "SaaS",
    "Sverige", "Sveriges", "Stockholm", "Göteborg", "Malmö", "Jönköping",
    "Uppsala", "Lund", "Norden", "Europa", "Skandinavien",
    "Google", "Microsoft", "OpenAI", "Anthropic", "Claude", "ChatGPT",
    "Gemini", "Excel", "Word", "LinkedIn", "Facebook", "Instagram", "TikTok",
    "Isof", "Språkrådet", "SCB", "UKÄ", "Skatteverket", "Bolagsverket",
    "Workspace", "Teams", "Drive", "Docs", "Sheets", "Windows", "Office",
}

# Ord som gör ett versalt nationalitetsord till ett egennamn. "Europeiska
# unionen" och "Svenska kyrkan" ska ha versal, till skillnad från "en europeisk
# fråga". Hittat genom blindtestet, där verktyget flaggade EU som fel.
EGENNAMNSFORTSATTNING = (
    "unionen", "unionens", "kommissionen", "rådet", "rådets", "parlamentet",
    "domstolen", "kyrkan", "kyrkans", "akademien", "akademin", "institutet",
    "kanalen", "centralbanken", "handelskammaren", "samarbetet",
)

# Namn där apostrof-s är korrekt, eftersom de inte är svenska ord.
UTLANDSKA_NAMN = re.compile(
    r"^(Mc|Mac|O')|^(McDonald|Levi|Kellogg|Hershey|Wendy|Applebee|Dunkin|Sainsbury|Macy|Lloyd|Moody|Standard)",
    re.IGNORECASE)

PROFILER = {
    "allman": {
        "namn": "allmän text",
        "max_median_mening": 22,
        "min_spridning": 5.0,
        "max_punktlistandel": 0.30,
        "kraver_vi": False,
        "kraver_du": False,
        "vag_hedging": True,
        "lix_band": (30, 50),
        "om": "Grundläget. Används när ingen profil anges. Breda band, grov poäng.",
    },
    "kundmejl": {
        "namn": "kundmejl",
        "max_median_mening": 16,
        "min_spridning": 5.0,
        "max_punktlistandel": 0.20,
        "kraver_vi": True,
        "kraver_du": True,
        "vag_hedging": True,
        "lix_band": (25, 42),
        "om": "Mejl till kund eller prospekt. Kort, ett ärende, ett tilltal.",
    },
    "sajttext": {
        "namn": "sajttext",
        "max_median_mening": 16,
        "min_spridning": 5.0,
        "max_punktlistandel": 0.35,
        "kraver_vi": True,
        "kraver_du": True,
        "vag_hedging": True,
        "lix_band": (25, 42),
        "om": "Webbsida som ska sälja eller förklara. Avsändaren ska synas.",
    },
    "linkedin": {
        "namn": "LinkedIn-inlägg",
        "max_median_mening": 14,
        "min_spridning": 5.0,
        "max_punktlistandel": 0.40,
        "kraver_vi": False,
        "kraver_du": False,
        "vag_hedging": True,
        "lix_band": (20, 40),
        "om": "Socialt inlägg. Korta stycken, personlig röst, ingen rapportton.",
    },
    "myndighet": {
        "namn": "myndighetstext",
        "max_median_mening": 20,
        "min_spridning": 5.0,
        "max_punktlistandel": 0.45,
        "kraver_vi": True,
        "kraver_du": True,
        "vag_hedging": False,
        "lix_band": (28, 45),
        "om": ("Text från myndighet eller offentlig verksamhet. Språklagen 2009:600 kräver "
               "vårdat, enkelt och begripligt språk. Förbehåll och reservationer räknas inte "
               "som urvattning här, de är ofta rättsligt nödvändiga."),
    },
    "ansokan": {
        "namn": "jobbansökan",
        "max_median_mening": 18,
        "min_spridning": 5.0,
        "max_punktlistandel": 0.25,
        "kraver_vi": False,
        "kraver_du": False,
        "vag_hedging": True,
        "lix_band": (25, 45),
        "om": "Personligt brev. Klichéer väger tyngre här, avsändaren ska säga jag.",
    },
    "rapport": {
        "namn": "rapport",
        "max_median_mening": 23,
        "min_spridning": 5.0,
        "max_punktlistandel": 0.35,
        "kraver_vi": False,
        "kraver_du": False,
        "vag_hedging": False,
        "lix_band": (35, 55),
        "om": "Utredning eller rapport. Formell ton är rätt här, inte ett fel.",
    },
}


class Traff:
    def __init__(self, rad, axel, bevis, rubrik, varfor, istallet,
                 utdrag="", vikt=0, grupp=""):
        self.rad = rad
        self.axel = axel          # "korrekthet" eller "ai"
        self.bevis = bevis        # "matt", "observerat" eller ""
        self.rubrik = rubrik
        self.varfor = varfor
        self.istallet = istallet
        self.utdrag = utdrag
        self.vikt = vikt
        self.grupp = grupp

    def som_dict(self):
        return {k: getattr(self, k) for k in
                ("rad", "axel", "bevis", "rubrik", "varfor", "istallet",
                 "utdrag", "vikt", "grupp")}


# ----------------------------------------------------------------------------
# Textberedning
# ----------------------------------------------------------------------------

def las_monster():
    with open(MONSTERFIL, encoding="utf-8") as f:
        return json.load(f)


def dela_rader(text):
    if text.startswith("﻿"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def maska(rader):
    """
    Ersätter kodblock, inline-kod, URL:er, mejladresser och länkmål med
    blanksteg. Radnummer och kolumner bevaras.
    """
    ute = []
    i_block = False
    for rad in rader:
        if rad.strip().startswith("```") or rad.strip().startswith("~~~"):
            i_block = not i_block
            ute.append("")
            continue
        if i_block or re.match(r"^\s{4,}\S", rad):
            ute.append("")
            continue
        for rx in (r"`[^`]*`",
                   r"https?://\S+",
                   r"\bwww\.\S+",
                   r"\b[\w.+-]+@[\w-]+\.[\w.]+\b",
                   r"\]\([^)]*\)",
                   r"\b[\w-]+\.(py|js|md|json|html|css|txt|csv|pdf|docx?|xlsx?)\b"):
            rad = re.sub(rx, lambda m: " " * len(m.group(0)), rad)
        ute.append(rad)
    return ute


def ar_rubrik(rad):
    return bool(re.match(r"^\s{0,3}#{1,6}\s+\S", rad))


def ar_punkt(rad):
    return bool(re.match(r"^\s*([-*+]|\d+[.)])\s+\S", rad))


def ar_tabell(rad):
    s = rad.strip()
    return s.startswith("|") and s.count("|") >= 2


def ar_citat(rad):
    return rad.strip().startswith(">")


def matbara_rader(rader):
    """Rader som ska mätas: prosa och punkter. Inte rubrik, tabell, citat."""
    ute = []
    for nr, rad in enumerate(rader, 1):
        if not rad.strip() or ar_rubrik(rad) or ar_tabell(rad) or ar_citat(rad):
            continue
        ute.append((nr, rad))
    return ute


def prosarader(rader):
    """Bara löptext. Punkter räknas inte som meningar."""
    return [(nr, r) for nr, r in matbara_rader(rader) if not ar_punkt(r)]


def rensa_markdown(rad):
    rad = re.sub(r"^\s{0,3}#{1,6}\s+", "", rad)
    rad = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", rad)
    rad = re.sub(r"\*\*(.+?)\*\*", r"\1", rad)
    rad = re.sub(r"\*(.+?)\*", r"\1", rad)
    rad = re.sub(r"\[([^\]]*)\]", r"\1", rad)
    return rad


def dela_meningar(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    bitar, start = [], 0
    for m in re.finditer(r"[.!?]+[\)\"”»]?(\s+|$)", text):
        slut = m.end()
        fore = text[start:m.start()]
        sista = re.search(r"([A-Za-zÅÄÖåäö.]+)$", fore)
        if sista and sista.group(1).lower().rstrip(".") in FORKORTNINGAR:
            continue
        if m.start() > 0 and text[m.start() - 1].isdigit() and text[slut:slut + 1].isdigit():
            continue
        bit = text[start:slut].strip()
        if bit:
            bitar.append(bit)
        start = slut
    rest = text[start:].strip()
    if rest:
        bitar.append(rest)
    return [b for b in bitar if re.search(r"[A-Za-zÅÄÖåäö]", b)]


ORD_RE = re.compile(r"[A-Za-zÅÄÖÉÈÜåäöéèü][A-Za-zÅÄÖÉÈÜåäöéèü\-']*")


def orden(text):
    return ORD_RE.findall(text)


def klipp(rad, pos, bredd=34):
    start = max(0, pos - bredd // 2)
    slut = min(len(rad), pos + bredd)
    bit = rad[start:slut].strip()
    if start > 0:
        bit = "..." + bit
    if slut < len(rad):
        bit += "..."
    return bit


# ----------------------------------------------------------------------------
# Axel 1: svenska skrivregler
# ----------------------------------------------------------------------------

def K(rad, rubrik, varfor, istallet, utdrag, vikt):
    return Traff(rad, "korrekthet", "", rubrik, varfor, istallet, utdrag, vikt, "skrivregel")


def kolla_skrivregler(rader, data, strikt_tankstreck):
    t = []
    manader = set(data["manader"])
    veckodagar = set(data["veckodagar"])
    sprakord = set(data["sprak_nationalitet"])

    for nr, rad in enumerate(rader, 1):
        if not rad.strip() or ar_tabell(rad):
            continue
        naken = rensa_markdown(rad)

        # Varje förekomst räknas. Em-strecket är verktygets tydligaste regel
        # och då ska antalet stämma.
        for m in re.finditer("—", rad):
            t.append(K(nr, "Långt tankstreck (em-streck)",
                       "Em-strecket finns inte i svensk typografi. Det är engelsk sättning som följt med in. Det korta tankstrecket är tillåtet, det långa är det inte.",
                       "Svenskt tankstreck med mellanslag runt, eller komma.",
                       klipp(rad, m.start()), 4))

        if strikt_tankstreck and "–" in rad:
            t.append(K(nr, "Tankstreck",
                       "Svenska skrivregler tillåter tankstreck. Den här flaggan är påslagen med --inga-tankstreck, alltså en stilregel du valt, inte ett språkfel.",
                       "Komma, kolon eller punkt.",
                       klipp(rad, rad.index("–")), 1))

        if re.search(r"(?<!-)--(?!-)", rad):
            t.append(K(nr, "Dubbelt bindestreck som tankstreck",
                       "Två bindestreck är ett skrivmaskinsknep, inte ett svenskt skiljetecken.",
                       "Tankstreck eller komma.", klipp(rad, rad.find("--")), 2))

        if "“" in rad:
            t.append(K(nr, "Engelska citattecken",
                       "På svenska ser tecknet likadant ut i början och i slutet. Engelskan vänder dem åt olika håll.",
                       "Använd ” i båda ändar, eller »».",
                       klipp(rad, rad.index("“")), 3))

        if '"' in naken:
            t.append(K(nr, "Raka citattecken",
                       "Raka citattecken pekas ut som ett tecken på att texten klistrats in direkt ur ett AI-svar.",
                       "Byt till ” i båda ändar.", klipp(rad, naken.index('"')), 1))

        for m in re.finditer(r"\b([A-Za-zÅÄÖåäö]{2,})['’´]s\b", naken):
            if UTLANDSKA_NAMN.match(m.group(1)):
                continue
            t.append(K(nr, "Genitivapostrof",
                       "Svenskan skriver " + m.group(1) + "s utan apostrof. Apostrofen är engelsk. Kontrollera att det inte är ett utländskt varumärke.",
                       m.group(1) + "s", klipp(naken, m.start()), 3))

        for m in re.finditer(r"\b\d{1,3}(?:,\d{3})+\b", naken):
            t.append(K(nr, "Engelsk tusentalsavgränsare",
                       "Svenskan skiljer tusental med mellanslag, inte komma.",
                       m.group(0).replace(",", " "), klipp(naken, m.start()), 3))

        for m in re.finditer(r"(?<![\d.,:/\-])(\d+)\.(\d+)(?![\d.,:/\-])", naken):
            heltal, dec = m.group(1), m.group(2)
            fore = naken[max(0, m.start() - 14):m.start()].lower()
            if "kl" in fore or "klockan" in fore or "version" in fore or "v." in fore:
                continue
            # Produkt- och versionsnummer: Python 3.8, Windows 3.1. Ett tal
            # efter ett versalt ord är nästan aldrig ett decimaltal.
            forra_ordet = re.search(r"([A-Za-zÅÄÖåäö]+)\s*$", naken[:m.start()])
            if forra_ordet and forra_ordet.group(1)[0].isupper():
                continue
            efter = naken[m.end():m.end() + 10]
            enhet = re.match(r"\s*(%|kr|procent|miljon|miljard|mil\b|km|kg|tim|sek|SEK)", efter)
            if len(dec) == 2 and int(heltal) <= 23 and not enhet:
                continue  # kan vara ett klockslag, svenskan skriver 14.00
            t.append(K(nr, "Decimalpunkt",
                       "Svenskan använder komma som decimaltecken.",
                       heltal + "," + dec, klipp(naken, m.start()), 3))

        for m in re.finditer(r"(\d+(?:[.,]\d+)?)%", naken):
            t.append(K(nr, "Procenttecken utan mellanslag",
                       "Svenska skrivregler sätter mellanslag mellan tal och procenttecken.",
                       m.group(1) + " %", klipp(naken, m.start()), 2))

        for m in re.finditer(r"\b(\d{1,2}):(\d{2})\s?(AM|PM|am|pm)\b", naken):
            t.append(K(nr, "Engelskt klockslag",
                       "Svenskan använder 24-timmarsklocka: kl. 14.00.",
                       "kl. " + m.group(1) + "." + m.group(2), klipp(naken, m.start()), 3))

        for m in re.finditer(r"\b([A-ZÅÄÖ][a-zåäö]+)\b", naken):
            ord_, lag = m.group(1), m.group(1).lower()
            if lag not in manader and lag not in veckodagar and lag not in sprakord:
                continue
            if ord_ in EGENNAMN_UNDANTAG:
                continue
            fore = naken[:m.start()].rstrip()
            if not fore or fore[-1] in ".!?:" or ar_rubrik(rad) and not fore:
                continue
            efter = naken[m.end():m.end() + 26].lstrip().lower()
            if any(efter.startswith(o) for o in EGENNAMNSFORTSATTNING):
                continue
            sort = ("Månad" if lag in manader else
                    "Veckodag" if lag in veckodagar else
                    "Språk eller nationalitet")
            t.append(K(nr, sort + " med stor bokstav",
                       "Svenskan skriver " + lag + " med liten bokstav. Engelskan versaliserar. Ett av de tydligaste tecknen på att texten tänkts på engelska.",
                       lag, klipp(naken, m.start()), 3))

        for m in re.finditer(r"\b([A-ZÅÄÖ][a-zåäö]+)\s+(\d{1,2}),\s*(\d{4})\b", naken):
            if m.group(1).lower() not in manader:
                continue
            t.append(K(nr, "Engelskt datumformat",
                       "Svenskan skriver 19 september 2026 eller 2026-09-19.",
                       m.group(2) + " " + m.group(1).lower() + " " + m.group(3),
                       klipp(naken, m.start()), 3))

    t.extend(kolla_rubrikversaler(rader))
    t.extend(kolla_oxfordkomma(rader))
    return t


def kolla_rubrikversaler(rader):
    t = []
    for nr, rad in enumerate(rader, 1):
        if not ar_rubrik(rad):
            continue
        text = re.sub(r"[*_`]", "", re.sub(r"^\s{0,3}#{1,6}\s+", "", rad).strip())
        ord_lista = text.split()
        if len(ord_lista) < 3:
            continue
        svans = ord_lista[1:]
        versala = [o for o in svans
                   if re.match(r"^[A-ZÅÄÖ][a-zåäö]", o)
                   and o.strip(".,:;") not in EGENNAMN_UNDANTAG]
        if len(versala) >= 2 and len(versala) >= len(svans) * 0.5:
            t.append(K(nr, "Rubrik med engelsk versalisering",
                       "Svenska rubriker versaliserar bara första ordet och egennamn. Title Case är engelsk standard.",
                       "Gemener på allt utom första ordet och egennamn. Rätta för hand, ett skript kan inte veta vad som är egennamn.",
                       text, 3))
    return t


FINITA_VERB = {
    "har", "hade", "är", "var", "blir", "blev", "kan", "kunde", "ska",
    "skall", "skulle", "måste", "bör", "borde", "får", "fick", "finns",
    "gör", "gjorde", "vill", "ville", "behöver", "krävs", "saknas", "går",
    "ligger", "står", "sker", "gäller", "innebär", "leder",
}


def har_finit_verb(led):
    """
    Grov gissning: bär ledet ett eget verb är det en sats och inte ett
    uppräkningsled. Komma mellan huvudsatser före och är korrekt svenska.

    Utan syntaxanalys går det inte att göra bättre, och hellre missad träff
    än falskt larm. Blindtestet gav tre falska larm av fem på den här regeln.
    """
    for o in led.lower().split():
        if o in FINITA_VERB:
            return True
        if len(o) > 4 and (o.endswith("ade") or o.endswith("de") or o.endswith("te")):
            return True
        if len(o) > 4 and o.endswith("s") and not o.endswith("ns"):
            return True
    return False


def kolla_oxfordkomma(rader):
    t = []
    for nr, rad in matbara_rader(rader):
        naken = rensa_markdown(rad)
        # Bara äkta uppräkningar. Led med eget verb är satser, inte led.
        for m in re.finditer(
                r"\b(\w+(?:\s+\w+){0,2}),\s+(\w+(?:\s+\w+){0,2}),\s+(och|eller|samt)\s+\w+",
                naken):
            if har_finit_verb(m.group(1)) or har_finit_verb(m.group(2)):
                continue
            # Ligger på AI-luktaxeln, inte bland regelfelen. Komma mellan
            # huvudsatser före och ÄR korrekt svenska, och ett regex kan inte
            # avgöra vilket fall det är. Ett osäkert fynd får inte räknas in i
            # ett tal som ska vara objektivt.
            t.append(Traff(nr, "ai", "observerat", "Möjligt oxfordkomma",
                           "Komma före och i en uppräkning är engelsk standard, inte svensk. Men komma mellan två huvudsatser är korrekt svenska, och det går inte att skilja dem åt utan att läsa. Kontrollera själv.",
                           "Är det en uppräkning: ta bort kommat före " + m.group(3) + ". Är det två satser: låt stå.",
                           klipp(naken, m.start()), 1, "struktur"))
    return t


# ----------------------------------------------------------------------------
# Axel 2: AI-lukt
# ----------------------------------------------------------------------------

def kolla_monster(rader, data, profil):
    t = []
    for post in data["monster"]:
        rx = re.compile(post["re"], re.IGNORECASE)
        grupp = post["grupp"]
        vikt = post.get("vikt", 1)
        if grupp == "hedging" and not profil["vag_hedging"]:
            vikt = 0
        for nr, rad in matbara_rader(rader):
            m = rx.search(rensa_markdown(rad))
            if not m:
                continue
            naken = rensa_markdown(rad)
            t.append(Traff(nr, "ai", "observerat", post["visa"], post["varfor"],
                           post["istallet"], klipp(naken, m.start()), vikt, grupp))
    return t


def kolla_struktur(rader, matt, profil):
    t = []
    for nr, rad in enumerate(rader, 1):
        if re.match(r"^\s*[-*+]\s+\*\*[^*]{2,60}\*\*\s*[:–-]", rad):
            t.append(Traff(nr, "ai", "observerat", "Punktlista med fet ingress",
                           "Punkt som börjar med ett fetstilt ord och kolon är det mest igenkända AI-formatet som finns.",
                           "Skriv punkten som en mening, eller gör om listan till löptext.",
                           rad.strip()[:60], 3, "struktur"))

    if matt["punktlistandel"] > profil["max_punktlistandel"] and matt["punktrader"] >= 4:
        t.append(Traff(0, "ai", "observerat", "För mycket punktlista",
                       "%d av %d innehållsrader är punkter (%.0f %%). Bandet för %s slutar vid %.0f %%. Listor används när ett samband inte formulerats."
                       % (matt["punktrader"], matt["innehallsrader"], matt["punktlistandel"] * 100,
                          profil["namn"], profil["max_punktlistandel"] * 100),
                       "Skriv om minst en lista till löptext. Två punkter är två meningar.",
                       "", 3, "struktur"))

    for nr, rad in enumerate(rader, 1):
        if ar_rubrik(rad):
            txt = re.sub(r"^\s{0,3}#{1,6}\s+", "", rad).strip().rstrip("*_`")
            if txt.endswith("?") and len(txt.split()) <= 6:
                t.append(Traff(nr, "ai", "observerat", "Frågerubrik utan innehåll",
                               "Tomma frågerubriker berättar inte vad avsnittet säger.",
                               "Skriv svaret i rubriken i stället för frågan.",
                               txt, 2, "struktur"))
    return t


def kolla_tankstreckstathet(rader, matt):
    """
    Det korta tankstrecket är korrekt svenska och flaggas inte som fel. Men
    överanvändning är ett igenkänt AI-drag. En svensk rekryterare på Manpower
    formulerar tröskeln så här: två eller tre gånger i en text är okej, vid
    femte förekomsten vet man att det sannolikt är AI-skrivet.

    Det långa em-strecket hanteras separat och är alltid fel på svenska.
    """
    antal = 0
    for nr, rad in matbara_rader(rader):
        antal += rensa_markdown(rad).count("–")
    if antal == 0:
        return []

    tillatet = max(3, round(3 * matt["antal_ord"] / 1000.0))
    if antal <= tillatet:
        return []

    return [Traff(0, "ai", "observerat", "Tankstreck %d gånger" % antal,
                  "Tankstrecket är korrekt svenska och inget fel i sig. Men %d gånger i en text på %d ord är för tätt. Svenska rekryterare pekar ut just det som en AI-flagga: två eller tre gånger går bra, vid femte vet man."
                  % (antal, matt["antal_ord"]),
                  "Behåll de två eller tre som bär, byt resten mot komma, kolon eller punkt.",
                  "", 3, "struktur")]


def kolla_rytm(matt, profil):
    """De tre enda drag som är uppmätta på svensk AI-text."""
    t = []
    if matt["antal_meningar"] < 5 or matt["antal_ord"] < MIN_ORD_FOR_POANG:
        return t

    if matt["median_meningslangd"] >= profil["max_median_mening"]:
        t.append(Traff(0, "ai", "matt", "För långa meningar",
                       "Medianmeningen är %.0f ord, typvärdet %d. Bandet för %s slutar vid %d. I den enda svenska mätning som finns låg AI-texternas typvärde på %d ord och människornas på %d."
                       % (matt["median_meningslangd"], matt["typvarde"], profil["namn"],
                          profil["max_median_mening"], AI_TYPVARDE, MANSKLIG_TYPVARDE),
                       "Dela de längsta meningarna. Leta efter som, vilket och vilken.",
                       "", 4, "rytm"))

    # Jämn puls är bara ett tecken när meningarna också är långa. En text av
    # korta huggna meningar har låg spridning av rent matematiska skäl, och
    # den läser som en människa, inte som en maskin.
    if (matt["spridning_meningslangd"] < profil["min_spridning"]
            and matt["median_meningslangd"] >= 12):
        t.append(Traff(0, "ai", "matt", "Jämn puls",
                       "Meningslängden varierar med %.1f ord i standardavvikelse. Under %.1f läser texten som maskin. Mänsklig svenska hoppar mellan korta och långa meningar."
                       % (matt["spridning_meningslangd"], profil["min_spridning"]),
                       "Lägg in en mening på fem ord efter en på tjugofem. Variationen är signaturen, inte medellängden.",
                       "", 4, "rytm"))

    if matt["andel_over_25"] > 0.30:
        t.append(Traff(0, "ai", "matt", "Många långa meningar",
                       "%.0f %% av meningarna är över 25 ord." % (matt["andel_over_25"] * 100),
                       "Dela hälften av dem.", "", 2, "rytm"))

    if matt["langsta_mening"] >= 45:
        t.append(Traff(matt["langsta_rad"], "ai", "observerat",
                       "Enskild mening på %d ord" % matt["langsta_mening"],
                       "Bisats på bisats är ett av de drag svenska språkkonsulter pekar ut.",
                       "Dela i två eller tre meningar.", matt["langsta_utdrag"], 2, "rytm"))

    if matt["mattr"] is not None and matt["mattr"] < 0.70:
        t.append(Traff(0, "ai", "matt", "Låg ordvariation",
                       "Andelen unika ord i rullande fönster är %.2f. Att AI-svenska använder färre unika ord är uppmätt. Tröskeln 0,70 är däremot ett riktvärde, inte kalibrerad."
                       % matt["mattr"],
                       "Stryk utfyllnad. Byt ALDRIG facktermer mot synonymer, samma sak ska heta samma sak hela vägen.",
                       "", 3, "rytm"))
    return t


def kolla_tilltal(rader, profil, matt):
    t = []
    if matt["antal_ord"] < MIN_ORD_FOR_POANG:
        return t
    text = " ".join(rensa_markdown(r) for _, r in matbara_rader(rader)).lower()

    vi = len(re.findall(r"\b(vi|oss|vår|vårt|våra)\b", text))
    du = len(re.findall(r"\b(du|dig|din|ditt|dina)\b", text))
    ni = len(re.findall(r"\b(ni|er|ert|era)\b", text))

    if profil["kraver_vi"] and vi == 0:
        t.append(Traff(0, "ai", "matt", "Inget vi från avsändaren",
                       "Detta är den enda otvetydiga skillnad som uppmätts mellan svensk AI-text och svensk människotext. I studien saknade samtliga AI-texter avsändarens vi, medan människornas hade det. Mätt på myndighetstext, sex texter.",
                       "Skriv vad ni gör, inte vad som görs. Vi ringer upp inom ett dygn, inte Kontakt tas inom ett dygn.",
                       "", 5, "tilltal"))

    if profil["kraver_du"] and du == 0 and ni == 0:
        t.append(Traff(0, "ai", "observerat", "Inget tilltal till läsaren",
                       "Texten talar om läsaren i stället för till läsaren. Du-tilltal är normen i svensk företags- och myndighetskommunikation.",
                       "Byt kunden och man mot du.", "", 3, "tilltal"))

    if du >= 2 and ni >= 2:
        t.append(Traff(0, "ai", "observerat", "Växling mellan du och ni",
                       "Texten använder både du (%d) och ni (%d). Blandat tilltal i samma text pekas ut som ett vanligt fel i AI-svenska." % (du, ni),
                       "Välj ett. Du är säkrare: få störs av du, fler störs av ni.",
                       "", 3, "tilltal"))
    return t


# ----------------------------------------------------------------------------
# Mått
# ----------------------------------------------------------------------------

def rakna_matt(rader):
    meningar = []
    for nr, rad in prosarader(rader):
        for m in dela_meningar(rensa_markdown(rad)):
            # Hälsningsfraser och signaturrader är inte meningar och skulle
            # dra ner både median och spridning i mejl och inlägg.
            if not re.search(r"[.!?]\s*$", m) and len(orden(m)) < 4:
                continue
            meningar.append((nr, m))

    langder = [n for n in (len(orden(m)) for _, m in meningar) if n > 0]

    alla_ord = []
    for _, rad in matbara_rader(rader):
        alla_ord.extend(orden(rensa_markdown(rad)))

    innehall = [r for r in rader if r.strip() and not ar_tabell(r)]
    punkter = [r for r in innehall if ar_punkt(r)]

    langsta, langsta_rad, langsta_utdrag = 0, 0, ""
    for nr, m in meningar:
        n = len(orden(m))
        if n > langsta:
            langsta, langsta_rad = n, nr
            langsta_utdrag = m[:60] + ("..." if len(m) > 60 else "")

    return {
        "antal_ord": len(alla_ord),
        "antal_meningar": len(langder),
        "median_meningslangd": statistics.median(langder) if langder else 0,
        "medel_meningslangd": statistics.mean(langder) if langder else 0,
        "typvarde": typvarde(langder),
        "spridning_meningslangd": statistics.pstdev(langder) if len(langder) > 1 else 0.0,
        "andel_over_25": (sum(1 for l in langder if l > 25) / len(langder)) if langder else 0.0,
        "langsta_mening": langsta,
        "langsta_rad": langsta_rad,
        "langsta_utdrag": langsta_utdrag,
        "innehallsrader": len(innehall),
        "punktrader": len(punkter),
        "punktlistandel": (len(punkter) / len(innehall)) if innehall else 0.0,
        "mattr": rakna_mattr(alla_ord),
        "lix": rakna_lix(alla_ord, len(langder)),
    }


def typvarde(langder):
    """Vanligaste meningslängden, avrundad till närmaste tvåtal. Det Arifovic mätte."""
    if not langder:
        return 0
    hink = {}
    for l in langder:
        k = (l // 2) * 2
        hink[k] = hink.get(k, 0) + 1
    return max(hink.items(), key=lambda kv: (kv[1], -kv[0]))[0]


def rakna_mattr(ord_lista, fonster=50):
    """Moving Average Type-Token Ratio, längdoberoende till skillnad från TTR."""
    if len(ord_lista) < MIN_ORD_FOR_VARIATION:
        return None
    ordf = [o.lower() for o in ord_lista]
    kvoter = [len(set(ordf[i:i + fonster])) / fonster
              for i in range(len(ordf) - fonster + 1)]
    return sum(kvoter) / len(kvoter)


def rakna_lix(ord_lista, antal_meningar):
    """Lix enligt Björnsson. Rapporteras som sammanhang, poängsätts aldrig."""
    if not ord_lista or antal_meningar == 0:
        return None
    langa = sum(1 for o in ord_lista if len(o) > 6)
    return round(len(ord_lista) / antal_meningar + langa * 100 / len(ord_lista))


# ----------------------------------------------------------------------------
# Poäng
# ----------------------------------------------------------------------------

def rakna_poang(traffar, matt):
    regelfel = sum(1 for t in traffar if t.axel == "korrekthet")

    if matt["antal_ord"] < MIN_ORD_FOR_POANG:
        return {"regelfel": regelfel, "ai_lukt": None, "delar": {},
                "for_kort": True}

    per_tusen = 1000.0 / max(matt["antal_ord"], 1)

    def summa(*grupper):
        return sum(t.vikt for t in traffar if t.grupp in grupper)

    # Viktningen är omgjord efter blindtestet 2026-09-19. Rytmen vägde tyngst
    # av allt och byggde på LiU-mätningen från 2025, där AI-svenska hade
    # längre och jämnare meningar än mänsklig svenska. Mot en modell från 2026
    # replikerade det inte: AI-texterna varierade MER än riksdagsledamöterna.
    # Rytmen är därför nedflyttad till en biroll. Det som faktiskt fångar den
    # uppenbara AI-tonen är anglicismerna, fraserna och strukturen, och de har
    # fått vikten i stället. Se test/RESULTAT.md.
    delar = {
        "anglicismer": min(25.0, summa("anglicism", "metatext") * per_tusen * 1.7),
        "ord och fraser": min(25.0, summa("ord", "fras", "hedging") * per_tusen * 1.4),
        "struktur": min(18.0, summa("struktur") * 1.8),
        "meningsrytm": min(12.0, summa("rytm") * 1.6),
        "tilltal": min(12.0, summa("tilltal") * 2.0),
        "engelsk typografi": min(8.0, summa("skrivregel") * per_tusen * 1.2),
    }
    return {
        "regelfel": regelfel,
        "ai_lukt": round(min(100.0, sum(delar.values()))),
        "delar": {k: round(v, 1) for k, v in delar.items()},
        "for_kort": False,
    }


def omdome(ai_lukt, regelfel):
    if ai_lukt is None:
        return "För kort text för att mäta. Läs fynden rad för rad i stället."
    if regelfel == 0 and ai_lukt <= 15:
        return "Läser som svenska skriven av en människa."
    if ai_lukt <= 30:
        return "Mestadels bra. Några enskilda ställen drar ner."
    if ai_lukt <= 55:
        return "Känns igen som AI-text av en van läsare."
    return "Läser tydligt som AI-genererad svenska."


# ----------------------------------------------------------------------------
# Utskrift
# ----------------------------------------------------------------------------

BEVISTEXT = {"matt": "mätt", "observerat": "observerat", "": ""}


def skriv_rapport(traffar, matt, poang, profil, filnamn):
    u = []
    u.append("")
    u.append("  SLOPKOLL  " + (filnamn or "stdin") + "   profil: " + profil["namn"])
    u.append("  " + "-" * 66)
    u.append("")
    u.append("  Korrekthet   %d fel mot svenska skrivregler%s"
             % (poang["regelfel"], "" if poang["regelfel"] else "   (rent)"))
    if poang["ai_lukt"] is None:
        u.append("  AI-lukt      mäts inte, texten är under %d ord" % MIN_ORD_FOR_POANG)
    else:
        u.append("  AI-lukt      %d/100   lägre är bättre" % poang["ai_lukt"])
    u.append("  %s" % omdome(poang["ai_lukt"], poang["regelfel"]))
    u.append("")

    if poang["delar"]:
        u.append("  Vad lukten består av:")
        for namn, v in sorted(poang["delar"].items(), key=lambda kv: -kv[1]):
            if v <= 0:
                continue
            u.append("    %-19s %5.1f  %s" % (namn, v, "#" * int(min(28, round(v)))))
        u.append("")

    u.append("  Mått:")
    u.append("    ord %d, meningar %d" % (matt["antal_ord"], matt["antal_meningar"]))
    if matt["antal_meningar"]:
        u.append("    meningslängd: median %.0f, typvärde %d, spridning %.1f"
                 % (matt["median_meningslangd"], matt["typvarde"], matt["spridning_meningslangd"]))
        u.append("      svensk referens: människa typvärde %d, AI typvärde %d (LiU 2025, en studie)"
                 % (MANSKLIG_TYPVARDE, AI_TYPVARDE))
    if matt["lix"] is not None:
        u.append("    lix %d (band för %s: %d till %d). Sammanhang, ingår inte i poängen."
                 % (matt["lix"], profil["namn"], profil["lix_band"][0], profil["lix_band"][1]))
    if matt["mattr"] is not None:
        u.append("    ordvariation %.2f" % matt["mattr"])
    else:
        u.append("    ordvariation mäts inte under %d ord" % MIN_ORD_FOR_VARIATION)
    u.append("    punktlistandel %.0f %%" % (matt["punktlistandel"] * 100))
    u.append("")

    if not traffar:
        u.append("  Inga fynd.")
        u.append("")
        return "\n".join(u)

    for axel, rubrik in (("korrekthet", "SVENSKA SKRIVREGLER   rätt eller fel, oberoende av AI"),
                         ("ai", "AI-LUKT   bevisgrad inom hakparentes")):
        i_axel = [t for t in traffar if t.axel == axel]
        if not i_axel:
            continue
        u.append("  " + rubrik)
        u.append("  " + "-" * 66)
        i_axel.sort(key=lambda t: (t.rad == 0, t.rad, -t.vikt))
        for t in i_axel:
            plats = ("rad %d" % t.rad) if t.rad else "hela texten"
            markning = (" [%s]" % BEVISTEXT[t.bevis]) if t.bevis else ""
            u.append("  %-11s %s%s" % (plats, t.rubrik, markning))
            if t.utdrag:
                u.append("              ”%s”" % t.utdrag)
            u.append("              %s" % t.varfor)
            u.append("              → %s" % t.istallet)
            u.append("")

    u.append("  Trösklarna i verktyget är riktvärden, inte kalibrerade mot en svensk korpus.")
    u.append("  Poängen är ett bearbetningsbehov, aldrig en sannolikhet för att texten är AI.")
    u.append("")
    return "\n".join(u)


# ----------------------------------------------------------------------------

def analysera(text, profilnamn="allman", strikt_tankstreck=False):
    data = las_monster()
    profil = PROFILER.get(profilnamn, PROFILER["allman"])
    rader = maska(dela_rader(unicodedata.normalize("NFC", text)))

    matt = rakna_matt(rader)
    traffar = []
    traffar += kolla_skrivregler(rader, data, strikt_tankstreck)
    traffar += kolla_monster(rader, data, profil)
    traffar += kolla_struktur(rader, matt, profil)
    traffar += kolla_tankstreckstathet(rader, matt)
    traffar += kolla_rytm(matt, profil)
    traffar += kolla_tilltal(rader, profil, matt)

    return traffar, matt, rakna_poang(traffar, matt), profil


def satt_utdata_till_utf8():
    """
    Windows-konsolen kör cp1252 som standard och kvävs av svenska citattecken
    och pilar. Utan det här kraschar verktyget på den vanligaste maskinen.
    """
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    satt_utdata_till_utf8()
    p = argparse.ArgumentParser(description="Mäter svenska skrivregler och AI-drag i en text.")
    p.add_argument("fil", nargs="?", default="-", help="textfil, eller - för stdin")
    p.add_argument("--profil", default="allman", choices=sorted(PROFILER.keys()))
    p.add_argument("--json", action="store_true")
    p.add_argument("--inga-tankstreck", action="store_true",
                   dest="strikt", help="flagga även vanligt tankstreck. Stilval, inte språkregel.")
    p.add_argument("--profiler", action="store_true", help="lista profilerna och sluta")
    args = p.parse_args()

    if args.profiler:
        for nyckel, prof in sorted(PROFILER.items()):
            print("%-11s %s" % (nyckel, prof["om"]))
        return 0

    if args.fil == "-":
        text, filnamn = sys.stdin.read(), None
    else:
        with open(args.fil, encoding="utf-8-sig") as f:
            text = f.read()
        filnamn = os.path.basename(args.fil)

    traffar, matt, poang, profil = analysera(text, args.profil, args.strikt)

    if args.json:
        print(json.dumps({"fil": filnamn, "profil": args.profil, "poang": poang,
                          "matt": matt, "traffar": [t.som_dict() for t in traffar]},
                         ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(skriv_rapport(traffar, matt, poang, profil, filnamn))
    return 0


if __name__ == "__main__":
    sys.exit(main())
