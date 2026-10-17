#!/usr/bin/env python3
"""Generate toc.md for sama-veda from the parsed structure of S1.
Usage: python3 -I make_toc.py SOURCE.itx OUT_toc.md"""
import collections
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parse_itx as P

verses, headings, annotations, issues = P.parse(P.read_source(sys.argv[1]))
P.assign_units(verses)
units = collections.OrderedDict()
for v in verses:
    units.setdefault((v["part"], v["chapter"]), []).append(v)

PARTS = {
 1: ("पूर्वार्चिकः", "Purvarcika (first book of hymns)",
     "the first collection of mantras, arranged in three kandas: Agneya, "
     "Aindra and Pavamana (inferred from the kanda names)"),
 2: ("आरण्य आर्चिकः", "Aranya Arcika (forest book)",
     "a short collection set apart in the file under its own heading "
     "(inferred from the heading)"),
 3: ("महानाम्न्य आर्चिकः", "Mahanamnya Arcika",
     "a short collection set apart in the file under its own heading, "
     "ending with the five purishapadas (inferred from the headings)"),
 4: ("उत्तरार्चिकः", "Uttararcika (second book of hymns)",
     "the second collection of mantras, in prapathakas and ardhas, "
     "arranged in groups of three verses (inferred from the coordinates)"),
}
ORD = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9"}
KANDA_EN = {"AgneyaM": "Agneya", "aindra": "Aindra", "pAvamAna": "Pavamana",
            "AraNya": "Aranya"}
FILES = {}
for (p, c), items in units.items():
    FILES[(p, c)] = (f"text/p{p:02d}.md" if p in (2, 3)
                     else f"text/ch{p:02d}.{c:02d}.md")

out = []
out.append("# Sama Veda Samhita, Kauthuma Shakha (सामवेदसंहिता, कौथुमशाखा)\n")
out.append("- Author / compiler: none named; Vedic Samhita of the Sama Veda, "
           "Kauthuma recension (the file's title names the Kauthuma Shakha)")
out.append("- Subject and purpose of the book: the collection of verses "
           "(mantras) that are sung in the Sama Veda; the file arranges them "
           "in two main books (Purvarcika and Uttararcika) with two short "
           "books between them (inferred from the file's own headings)")
out.append("- Base edition: sv-kauthuma.itx, Sanskrit Documents, typed and "
           "proofread by Anshuman Pandey, latest update 28 August 2021 "
           "(source S1 in sources.md). The printed edition behind it is not "
           "stated in the file")
out.append("- Mapping: part = arcika (as headed in the file), chapter = ardha "
           "(half of a prapathaka; one chapter for the two short books), "
           "verse = mantra, numbered continuously 1 to 1875 as in the file")
total = len(verses)
out.append(f"- Totals: 4 parts, {len(units)} chapters, {total} verses "
           "extracted (traditional: 1875)\n")
out.append("Notes on the structure:\n")
out.append("- Kanda boundaries do not fall on chapter boundaries. Agneya "
           "verses 1-114 (chapters 01.01 to 01.03), Aindra 115-466 "
           "(01.03 to 01.10), Pavamana 467-585 (01.10 to 01.12); the "
           "Aranya book (part 02) is headed `AraNya kANDam`.")
out.append("- The file groups verses in tens (Purvarcika, Aranya, Mahanamnya: "
           "coordinate `DDEE`) and in threes (Uttararcika: sukta `DD`, verse "
           "`EE`). These groupings are not written into the text files.")
out.append("- Uttararcika prapathakas 1-5 have two ardhas each, "
           "prapathakas 6-9 have three (the file says `tR^itIyo.ardhaH`).")
out.append("- The rishi, chandas and devata lines that the file prints "
           "before the first eight suktas of the Uttararcika are kept in "
           "`notes/annotations.md` (key: the first line of the verse that "
           "follows).\n")

for p in (1, 2, 3, 4):
    sa, en, purpose = PARTS[p]
    out.append(f"## Part {p:02d}: {sa} ({en})\n")
    out.append(f"Purpose: {purpose} (source: inferred)\n")
    out.append("| Part | Chapter | Sanskrit name | English name | Purpose | "
               "Verses (extracted) | Verses (traditional) | File | Status |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for (pp, c), items in units.items():
        if pp != p:
            continue
        first = items[0]
        head = first["ardha_heading"]
        if p in (2, 3):
            sk = {2: "आरण्यकाण्डम्", 3: "महानाम्न्य आर्चिकः"}[p]
            sk = P.to_devanagari({2: "AraNya kANDam",
                                  3: "mahAnAmnya ArchikaH"}[p])
            en_name = {2: "Aranya kanda", 3: "Mahanamnya"}[p]
            ranges = f"verses {first['n']}-{items[-1]['n']}"
        else:
            sk = P.to_devanagari(f"{head[0]} prapAThakaH | {head[1]}")
            prap, ardha = P.ORDINAL[head[0]], P.ORDINAL[head[1]]
            en_name = f"Prapathaka {prap}, ardha {ardha}"
            ranges = f"verses {first['n']}-{items[-1]['n']}"
        kandas = sorted({KANDA_EN.get(v["kanda"], "") for v in items} - {""})
        purpose_row = ranges + (f"; kanda {' / '.join(kandas)}"
                                if kandas and p == 1 else "")
        out.append(f"| {p:02d} | {c:02d} | {sk} | {en_name} | {purpose_row} | "
                   f"{len(items)} | unknown | {FILES[(pp, c)]} | pending |")
    out.append("")
open(sys.argv[2], "w", encoding="utf8").write("\n".join(out) + "\n")
print("toc written", len(units), "units")
