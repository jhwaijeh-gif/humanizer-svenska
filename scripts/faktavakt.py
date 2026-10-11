#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
faktavakt.py, spärren mot att en omskrivning ändrar innehållet.

Körs EFTER varje omskrivning, aldrig före. Den läser originalet och den nya
texten och kontrollerar att inget som bär betydelse har försvunnit eller
ändrats. Fallerar den kasseras omskrivningen.

    python faktavakt.py original.md omskriven.md
    python faktavakt.py original.md omskriven.md --json

Vakten bryr sig om:

  tal          belopp, antal, procent, årtal, tider. Ett tal som ändrats
               eller försvunnit är det värsta som kan hända en omskrivning.
  negationer   inte, aldrig, ingen, varken. Ett tappat inte vänder meningen.
  modalitet    kan, ska, måste, bör. Skillnaden mellan ett erbjudande och
               ett löfte, och ibland mellan giltigt och ogiltigt avtal.
  namn         egennamn, produktnamn, versaler mitt i mening.
  kontakt      mejladresser, telefonnummer, länkar.
  omfång       hur stor andel av texten som ändrats.

Utgångskod 0 = godkänd, 1 = underkänd.
"""

import argparse
import json
import os
import re
import sys
import unicodedata

# Över detta har omskrivningen gått för långt. Den ska putsa, inte skriva om.
MAX_ANDRINGSANDEL = 0.55

NEGATIONER = ["inte", "aldrig", "ingen", "inget", "inga", "varken", "utan",
              "icke", "knappast", "saknas", "saknar"]
MODALVERB = ["kan", "kunde", "ska", "skall", "skulle", "måste", "bör", "borde",
             "får", "fick", "behöver", "krävs"]

UNDANTAG_VERSAL = {
    "Jag", "Vi", "Du", "Ni", "Det", "Den", "De", "Han", "Hon", "Man", "Här",
    "Där", "Att", "Och", "Men", "Om", "När", "Hur", "Var", "Vad", "Så", "För",
    "Efter", "Innan", "Genom", "Med", "Utan", "Alla", "Många", "Detta", "Dessa",
}


def las(sokvag):
    with open(sokvag, encoding="utf-8-sig") as f:
        return unicodedata.normalize("NFC", f.read())


def utan_kod(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


# ----------------------------------------------------------------------------

def plocka_tal(text):
    """
    Alla tal, normaliserade så att 1 500 och 1500 räknas som samma sak.
    Årtal, belopp, procent, antal.
    """
    ute = []
    for m in re.finditer(r"\d[\d  .,:]*\d|\d", text):
        rå = m.group(0)
        if re.match(r"^\d{1,2}[.:]\d{2}$", rå):      # klockslag
            ute.append(("tid", rå))
            continue
        if re.match(r"^\d{4}-\d{2}-\d{2}$", rå.replace(" ", "")):
            ute.append(("datum", rå))
            continue
        rent = rå.replace(" ", "").replace(" ", "")
        rent = rent.rstrip(".,:")
        if not rent:
            continue
        ute.append(("tal", rent))
    return ute


def plocka_negationer(text):
    lag = text.lower()
    return {o: len(re.findall(r"\b" + o + r"\b", lag)) for o in NEGATIONER}


def plocka_modalitet(text):
    lag = text.lower()
    return {o: len(re.findall(r"\b" + o + r"\b", lag)) for o in MODALVERB}


def plocka_namn(text):
    """Versala ord som inte står först i en mening. Egennamn och produktnamn."""
    namn = set()
    for stycke in text.split("\n"):
        stycke = re.sub(r"^\s{0,3}#{1,6}\s+", "", stycke)
        stycke = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", stycke)
        for m in re.finditer(r"([.!?:]\s+|\A\s*)?([A-ZÅÄÖ][A-Za-zÅÄÖåäö\-]{1,})", stycke):
            if m.group(1) is not None:
                continue          # står först, versalen säger inget
            ord_ = m.group(2)
            if ord_ in UNDANTAG_VERSAL:
                continue
            namn.add(ord_)
    return namn


def plocka_kontakt(text):
    ute = set()
    ute |= set(re.findall(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", text))
    ute |= set(re.findall(r"https?://\S+|\bwww\.\S+", text))
    for m in re.finditer(r"\b0[\d\s\-]{7,}\d\b", text):
        ute.add(re.sub(r"[\s\-]", "", m.group(0)))
    return ute


def ord_lista(text):
    return re.findall(r"[A-Za-zÅÄÖåäö]+", text.lower())


def andringsandel(a, b):
    """Grov andel ändrade ord, via mängdöverlapp. Räcker för en spärr."""
    oa, ob = ord_lista(a), ord_lista(b)
    if not oa:
        return 0.0
    from collections import Counter
    ca, cb = Counter(oa), Counter(ob)
    kvar = sum((ca & cb).values())
    return 1.0 - (kvar / len(oa))


# ----------------------------------------------------------------------------

def granska(original, ny):
    o, n = utan_kod(original), utan_kod(ny)
    fel, varningar = [], []

    # Tal
    from collections import Counter
    tal_o = Counter(plocka_tal(o))
    tal_n = Counter(plocka_tal(n))
    for nyckel, antal in tal_o.items():
        sort, varde = nyckel
        saknas = antal - tal_n.get(nyckel, 0)
        if saknas > 0:
            fel.append({
                "typ": "tal",
                "vad": varde,
                "text": "%s %s finns %d gång(er) i originalet och %d i den nya texten."
                        % (sort.capitalize(), varde, antal, tal_n.get(nyckel, 0)),
            })
    for nyckel, antal in tal_n.items():
        if nyckel not in tal_o:
            fel.append({
                "typ": "tal",
                "vad": nyckel[1],
                "text": "Talet %s finns i den nya texten men inte i originalet. Påhittade siffror är det allvarligaste felet som finns."
                        % nyckel[1],
            })

    # Negationer
    neg_o, neg_n = plocka_negationer(o), plocka_negationer(n)
    for ord_, antal in neg_o.items():
        if neg_n[ord_] < antal:
            fel.append({
                "typ": "negation",
                "vad": ord_,
                "text": "Negationen %s förekom %d gång(er), nu %d. Ett tappat %s vänder betydelsen."
                        % (ord_, antal, neg_n[ord_], ord_),
            })

    # Modalitet
    mod_o, mod_n = plocka_modalitet(o), plocka_modalitet(n)
    for ord_, antal in mod_o.items():
        if mod_n[ord_] != antal and abs(mod_n[ord_] - antal) >= 1:
            varningar.append({
                "typ": "modalitet",
                "vad": ord_,
                "text": "%s: %d i originalet, %d nu. Kontrollera att ett kan inte blivit ett ska."
                        % (ord_, antal, mod_n[ord_]),
            })

    # Namn
    namn_o, namn_n = plocka_namn(o), plocka_namn(n)
    for namn in sorted(namn_o - namn_n):
        fel.append({
            "typ": "namn",
            "vad": namn,
            "text": "Namnet %s finns inte kvar. Produktnamn och egennamn får aldrig skrivas om." % namn,
        })

    # Kontaktuppgifter
    kon_o, kon_n = plocka_kontakt(o), plocka_kontakt(n)
    for k in sorted(kon_o - kon_n):
        fel.append({
            "typ": "kontakt",
            "vad": k,
            "text": "Kontaktuppgiften %s saknas i den nya texten." % k,
        })

    # Omfång
    andel = andringsandel(o, n)
    if andel > MAX_ANDRINGSANDEL:
        fel.append({
            "typ": "omfang",
            "vad": "%.0f %%" % (andel * 100),
            "text": "%.0f %% av orden är utbytta. Gränsen är %.0f %%. Det här är inte en putsning, det är en ny text. Skriv om mindre."
                    % (andel * 100, MAX_ANDRINGSANDEL * 100),
        })

    return {
        "godkand": not fel,
        "fel": fel,
        "varningar": varningar,
        "andringsandel": round(andel, 3),
    }


def skriv(res, ut):
    ut.append("")
    ut.append("  FAKTAVAKT")
    ut.append("  " + "-" * 60)
    ut.append("")
    ut.append("  %s" % ("GODKÄND" if res["godkand"] else "UNDERKÄND"))
    ut.append("  %.0f %% av orden ändrade" % (res["andringsandel"] * 100))
    ut.append("")
    if res["fel"]:
        ut.append("  Fel, omskrivningen ska kasseras:")
        for f in res["fel"]:
            ut.append("    [%s] %s" % (f["typ"], f["text"]))
        ut.append("")
    if res["varningar"]:
        ut.append("  Kontrollera för hand:")
        for v in res["varningar"]:
            ut.append("    [%s] %s" % (v["typ"], v["text"]))
        ut.append("")
    if res["godkand"] and not res["varningar"]:
        ut.append("  Alla tal, negationer, namn och kontaktuppgifter är kvar.")
        ut.append("")
    return ut


def main():
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    p = argparse.ArgumentParser(
        description="Kontrollerar att en omskrivning inte ändrat innehållet.")
    p.add_argument("original")
    p.add_argument("ny")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    for sokvag in (args.original, args.ny):
        if not os.path.exists(sokvag):
            sys.stderr.write("Hittar inte %s\n" % sokvag)
            return 2

    res = granska(las(args.original), las(args.ny))

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write("\n".join(skriv(res, [])))

    return 0 if res["godkand"] else 1


if __name__ == "__main__":
    sys.exit(main())
