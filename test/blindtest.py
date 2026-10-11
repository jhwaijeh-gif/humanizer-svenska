#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
blindtest.py, mäter om slopkoll faktiskt skiljer mänsklig svenska från AI-svenska.

Uppställningen är kontrollerad för genre, ämne och längd. Tio riksdagsmotioner
skrivna av människor under riksmötet 2020/21, alltså före ChatGPT, mot tio
motioner på samma tio ämnen och med samma ordantal, skrivna nu av en modell som
aldrig sett verktyget.

Bara författaren varierar. Allt annat hålls fast.

    python test/blindtest.py
    python test/blindtest.py --profil rapport

Siffran som betyder mest är falska positiv: hur ofta verktyget pekar ut korrekt
mänsklig svenska som AI. Ett verktyg som gör det är värre än inget verktyg.
"""

import argparse
import glob
import json
import os
import statistics
import subprocess
import sys

HAR = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.dirname(HAR)
SLOPKOLL = os.path.join(ROT, "scripts", "slopkoll.py")


def kor(sokvag, profil):
    ut = subprocess.run(
        [sys.executable, SLOPKOLL, sokvag, "--profil", profil, "--json"],
        capture_output=True, text=True, encoding="utf-8")
    if ut.returncode != 0:
        raise RuntimeError("slopkoll fallerade på %s:\n%s" % (sokvag, ut.stderr))
    return json.loads(ut.stdout)


def samla(mapp, etikett, profil):
    rader = []
    for f in sorted(glob.glob(os.path.join(HAR, "korpus", mapp, "*.md"))):
        d = kor(f, profil)
        rader.append({
            "fil": os.path.basename(f),
            "etikett": etikett,
            "lukt": d["poang"]["ai_lukt"],
            "regelfel": d["poang"]["regelfel"],
            "ord": d["matt"]["antal_ord"],
            "median": d["matt"]["median_meningslangd"],
            "spridning": d["matt"]["spridning_meningslangd"],
            "mattr": d["matt"]["mattr"],
            "lix": d["matt"]["lix"],
            "delar": d["poang"]["delar"],
        })
    return rader


def basta_troskel(rader):
    """Den tröskel som ger flest rätt. Vid lika: den som ger färst falska positiv."""
    varden = sorted({r["lukt"] for r in rader if r["lukt"] is not None})
    basta = None
    for i in range(len(varden)):
        t = varden[i]
        fp = sum(1 for r in rader if r["etikett"] == "människa" and r["lukt"] >= t)
        fn = sum(1 for r in rader if r["etikett"] == "AI" and r["lukt"] < t)
        ratt = len(rader) - fp - fn
        nyckel = (ratt, -fp)
        if basta is None or nyckel > basta[0]:
            basta = (nyckel, t, fp, fn, ratt)
    return basta


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    p = argparse.ArgumentParser()
    p.add_argument("--profil", default="rapport")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    rader = samla("manniska", "människa", args.profil) + samla("ai", "AI", args.profil)
    if not rader:
        print("Inga texter i test/korpus/. Kör hämtningen först.")
        return 2

    manniska = [r for r in rader if r["etikett"] == "människa"]
    ai = [r for r in rader if r["etikett"] == "AI"]

    if args.json:
        print(json.dumps(rader, ensure_ascii=False, indent=2))
        return 0

    print()
    print("  BLINDTEST   profil: %s" % args.profil)
    print("  genre, ämnen och längd hålls fasta. Bara författaren varierar.")
    print("  " + "-" * 68)
    print()
    print("  %-14s %-10s %6s %5s %6s %6s %6s %5s" %
          ("fil", "vem", "lukt", "fel", "ord", "median", "sprid", "lix"))
    for r in sorted(rader, key=lambda r: (r["lukt"] if r["lukt"] is not None else -1)):
        print("  %-14s %-10s %6s %5d %6d %6.0f %6.1f %5s" %
              (r["fil"], r["etikett"],
               ("-" if r["lukt"] is None else r["lukt"]), r["regelfel"],
               r["ord"], r["median"], r["spridning"],
               ("-" if r["lix"] is None else r["lix"])))
    print()

    for namn, grupp in (("människa", manniska), ("AI", ai)):
        lukt = [r["lukt"] for r in grupp if r["lukt"] is not None]
        fel = [r["regelfel"] for r in grupp]
        if not lukt:
            continue
        print("  %-9s n=%d   lukt median %5.1f   spann %d till %d   regelfel totalt %d"
              % (namn, len(grupp), statistics.median(lukt), min(lukt), max(lukt), sum(fel)))
    print()

    m_lukt = [r["lukt"] for r in manniska if r["lukt"] is not None]
    a_lukt = [r["lukt"] for r in ai if r["lukt"] is not None]
    if m_lukt and a_lukt:
        overlapp = sum(1 for m in m_lukt if m >= min(a_lukt))
        print("  Överlapp: %d av %d människotexter ligger i eller över AI-spannet."
              % (overlapp, len(m_lukt)))

        res = basta_troskel(rader)
        if res:
            _, t, fp, fn, ratt = res
            print("  Bästa tröskel: lukt >= %d ger %d av %d rätt." % (t, ratt, len(rader)))
            print("    falska positiv  %d av %d människotexter utpekade som AI" % (fp, len(m_lukt)))
            print("    falska negativ  %d av %d AI-texter missade" % (fn, len(a_lukt)))
        print()
        print("  Falska positiv är den siffra som betyder något. Ett verktyg som")
        print("  flaggar korrekt svenska är värre än inget verktyg.")
    print()
    print("  Detta är 20 texter i en genre. Det är ett rimlighetstest, inte en")
    print("  kalibrering. Se KALIBRERING.md.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
