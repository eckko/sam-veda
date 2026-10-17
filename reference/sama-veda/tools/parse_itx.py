#!/usr/bin/env python3
"""Parse sv-kauthuma.itx (Sanskrit Documents, Anshuman Pandey) into the
FORMAT.md layout.  Source: S1 in sources.md.

Usage:
  python3 -I parse_itx.py SOURCE.itx --report            # analysis only
  python3 -I parse_itx.py SOURCE.itx --write OUTDIR       # write text/ and notes/

What it does (and does not do):
  * Reads mantra lines of the form  `A P R DDEE##x##  text`  (A = ārcika,
    P = prapāṭhaka, R = ardha, DD/EE = two 2-digit counters) and groups them
    into verses up to the line that ends with `|| <number>`.
  * Converts ITRANS to Devanagari with indic_transliteration.  Nothing is
    corrected by hand: where the source number is damaged the verse number is
    taken from the running count and the doubt is written to the issues list.
  * Headings (ārcika, kāṇḍa, prapāṭhaka/ardha, closing lines) are not written
    to text files; they go to the structure report used for toc.md.
  * Sūkta annotation lines of the Uttarārcika (ṛṣi, chandas, devatā) are
    written to notes/annotations.md keyed by the ID of the next verse.
"""
import argparse
import collections
import json
import re
import sys
import unicodedata
from pathlib import Path

from indic_transliteration import sanscript

MANTRA = re.compile(
    r"^(?P<lead>\s*(?:(?P<junk>[A-Za-z]+)\s+)?)"
    r"(?P<a>\d+) (?P<p>\d+) (?P<r>\d+) (?P<d>\d\d) ?(?P<e>\d\d)"
    r"##(?P<letter>[a-z])##\s+(?P<text>.*?)\s*$")
END_NUMBER = re.compile(r"\|\|\s*(?P<num>\S+)\s*$")
ARCIKA = {"pUrvArchikaH": 1, "AraNya ArchikaH": 2,
          "mahAnAmnya ArchikaH": 3, "uttara ArchikaH": 4}
KANDA = re.compile(r"^\s*(?P<name>\S+(?: \S+)?) kANDam\s*$")
PRAPATHAKA = re.compile(
    r"^\s*(?P<prap>\S+) prapAThakaH \|\s+(?P<ardha>\S+)\s*$")
CLOSING = re.compile(r"^\s*\|\|.*\|\|\s*$")


ORDINAL = {"prathamaH": 1, "prathama": 1, "prathamo.ardhaH": 1,
           "dvitIya": 2, "dvitIyo.ardhaH": 2, "tR^itIya": 3,
           "tR^itIyo.ardhaH": 3, "chaturtha": 4, "pa~nchama": 5,
           "ShaShTha": 6, "saptama": 7, "AShTama": 8, "navama": 9}


def to_devanagari(text):
    """ITRANS to Devanagari, NFC."""
    out = sanscript.transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    return re.sub(" +", " ", unicodedata.normalize("NFC", out))


def read_source(path):
    return Path(path).read_text(encoding="utf8").split("\n")


def parse(lines):
    """Return (verses, headings, annotations, issues)."""
    verses = []          # dicts
    headings = []        # (line_no, kind, text)
    annotations = []     # (line_no, raw, index of next verse)
    issues = []
    current = []         # mantra lines of the open verse
    ardha_heading = None
    kanda = None
    arcika_heading = None
    in_body = False
    expected = 0
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if "\\begin{document}" in line:
            in_body = True
            continue
        if "\\end{document}" in line:
            break
        if not in_body or not stripped or stripped.startswith("\\") or \
                stripped.startswith("%"):
            continue
        match = MANTRA.match(line)
        if match:
            if match.group("junk"):
                issues.append((number, "other",
                               f"stray text '{match.group('junk')}' before "
                               "the coordinates (ignored)"))
            if "  " in match.group("text"):
                issues.append((number, "other",
                               "double space in the source line; collapsed "
                               "to one space"))
            current.append({
                "line_no": number, "letter": match.group("letter"),
                "coord": (int(match.group("a")), int(match.group("p")),
                          int(match.group("r")), int(match.group("d")),
                          int(match.group("e"))),
                "raw": match.group("text")})
            end = END_NUMBER.search(match.group("text"))
            if end:
                expected += 1
                token = end.group("num")
                if token.isdigit():
                    source_number = int(token)
                else:
                    source_number = None
                if source_number != expected:
                    issues.append((number, "numbering",
                                   f"source number is {token!r}, running "
                                   f"count is {expected}; running count used"))
                first = current[0]["coord"]
                if ardha_heading and first[0] in (1, 4) and (
                        ORDINAL[ardha_heading[0]], ORDINAL[ardha_heading[1]]
                ) != first[1:3]:
                    issues.append((current[0]["line_no"], "numbering",
                                   f"verse {expected}: source coordinates say "
                                   f"prapAThaka {first[1]} ardha {first[2]} "
                                   "but the heading above it says "
                                   f"{ardha_heading}; heading used"))
                verses.append({
                    "n": expected, "source_number": token, "lines": current,
                    "ardha_heading": ardha_heading, "kanda": kanda,
                    "arcika_heading": arcika_heading})
                current = []
            continue
        # not a mantra line
        if current:
            issues.append((number, "other", "heading inside an open verse"))
        text = stripped
        if text in ARCIKA or text == "Chanda ArchikaH":
            if text in ARCIKA:
                arcika_heading = text
                kanda = None
            headings.append((number, "arcika", text))
        elif KANDA.match(line):
            kanda = KANDA.match(line).group("name")
            headings.append((number, "kanda", text))
        elif PRAPATHAKA.match(line):
            ardha_heading = (PRAPATHAKA.match(line).group("prap"),
                             PRAPATHAKA.match(line).group("ardha"))
            headings.append((number, "prapathaka", text))
        elif CLOSING.match(line):
            headings.append((number, "closing", text))
            if "samAptA" in text:
                break
        elif text.startswith("atha "):
            headings.append((number, "section", text))
        else:
            annotations.append((number, text, len(verses) + 1))
    if current:
        issues.append((current[0]["line_no"], "missing",
                       "mantra lines after the last verse end"))
    return verses, headings, annotations, issues


def assign_units(verses):
    """Part and chapter numbers from the source's own coordinates."""
    chapter_numbers = {}
    for verse in verses:
        a, p, r = verse["lines"][0]["coord"][:3]
        if verse["ardha_heading"] and a in (1, 4):
            p = ORDINAL[verse["ardha_heading"][0]]
            r = ORDINAL[verse["ardha_heading"][1]]
        verse["part"] = a
        key = (a, p, r)
        per_part = [k for k in chapter_numbers if k[0] == a]
        if key not in chapter_numbers:
            chapter_numbers[key] = len(per_part) + 1
        verse["chapter"] = chapter_numbers[key]
        verse["ardha_key"] = key
    return chapter_numbers


def line_ids(verse):
    """IDs and Devanagari text for the lines of one verse."""
    count = len(verse["lines"])
    ids, texts = [], []
    for position, item in enumerate(verse["lines"]):
        raw = item["raw"]
        if position == count - 1:
            raw = END_NUMBER.sub("||", raw)
        suffix = "" if count == 1 else "abcdefgh"[position]
        ids.append(f"{verse['part']:02d}.{verse['chapter']:02d}."
                   f"{verse['n']}{suffix}")
        texts.append(to_devanagari(raw))
    return ids, texts


def report(verses, headings, annotations, issues):
    print("verses:", len(verses))
    lines_per = collections.Counter(len(v["lines"]) for v in verses)
    print("lines per verse:", dict(lines_per))
    chapters = assign_units(verses)
    counts = collections.Counter(v["ardha_key"] for v in verses)
    for key, number in chapters.items():
        first = min(v["n"] for v in verses if v["ardha_key"] == key)
        last = max(v["n"] for v in verses if v["ardha_key"] == key)
        kandas = {v["kanda"] for v in verses if v["ardha_key"] == key}
        print(f"  part {key[0]} ardha-key {key} -> ch {number:02d}: "
              f"{counts[key]} verses {first}-{last} kanda {sorted(kandas)}")
    ranges = collections.OrderedDict()
    for v in verses:
        key = (v["part"], v["kanda"])
        low, high = ranges.get(key, (v["n"], v["n"]))
        ranges[key] = (min(low, v["n"]), max(high, v["n"]))
    print("kanda ranges:", dict(ranges))
    print("annotation lines:", len(annotations))
    print("issues:", len(issues))
    for item in issues:
        print("  ", item)


def write_files(verses, annotations, issues, out):
    out = Path(out)
    (out / "text").mkdir(parents=True, exist_ok=True)
    (out / "notes").mkdir(parents=True, exist_ok=True)
    assign_units(verses)
    by_unit = collections.OrderedDict()
    for verse in verses:
        by_unit.setdefault((verse["part"], verse["chapter"]), []).append(verse)
    per_part = collections.defaultdict(list)
    for (part, chapter), items in by_unit.items():
        per_part[part].append((chapter, items))
    layout = {}
    verse_line_ids = {}
    for part, chapters in per_part.items():
        total = sum(len(v["lines"]) for _, items in chapters for v in items)
        if total < 1000:
            name = f"p{part:02d}.md"
            body = []
            for chapter, items in chapters:
                for verse in items:
                    ids, texts = line_ids(verse)
                    verse_line_ids[verse["n"]] = ids[0]
                    body.extend(f"{i} | {t}" for i, t in zip(ids, texts))
                layout[(part, chapter)] = f"text/{name}"
            (out / "text" / name).write_text("\n".join(body) + "\n",
                                             encoding="utf8")
        else:
            for chapter, items in chapters:
                name = f"ch{part:02d}.{chapter:02d}.md"
                body = []
                for verse in items:
                    ids, texts = line_ids(verse)
                    verse_line_ids[verse["n"]] = ids[0]
                    body.extend(f"{i} | {t}" for i, t in zip(ids, texts))
                (out / "text" / name).write_text("\n".join(body) + "\n",
                                                 encoding="utf8")
                layout[(part, chapter)] = f"text/{name}"
    notes = ["# Sūkta annotation lines (Uttarārcika), from S1", "",
             "Each line is `ID | annotation`; ID is the first line of the "
             "verse that follows the annotation in the source.", ""]
    for number, raw, next_verse in annotations:
        target = verse_line_ids.get(next_verse, "?")
        notes.append(f"{target} | {to_devanagari(raw)}")
    (out / "notes" / "annotations.md").write_text("\n".join(notes) + "\n",
                                                 encoding="utf8")
    summary = {f"{p:02d}.{c:02d}": {
        "file": layout[(p, c)], "verses": len(items),
        "first": items[0]["n"], "last": items[-1]["n"],
        "lines": sum(len(v["lines"]) for v in items),
        "kanda": sorted({v["kanda"] for v in items})}
        for (p, c), items in by_unit.items()}
    (out / "notes" / "layout.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--write")
    args = parser.parse_args()
    verses, headings, annotations, issues = parse(read_source(args.source))
    if args.report or not args.write:
        report(verses, headings, annotations, issues)
    if args.write:
        summary = write_files(verses, annotations, issues, args.write)
        print("written", len(summary), "units")
        json.dump([list(i) for i in issues],
                  open(Path(args.write) / "notes" / "issues.json", "w"),
                  ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.exit(main())
