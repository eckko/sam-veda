#!/usr/bin/env python3
"""Compare S1 verses 1-585 with the Purvarcika riks of S2
(github.com/Malolan05/samaveda, data/prakritiaranyakagana.json, accent-marked
text), ignoring accent signs, spaces, dandas and the chandrabindu/anusvara
difference.  Usage: crosscheck_s2.py BOOKDIR S2_JSON"""
import glob, json, re, sys, unicodedata
book, s2 = sys.argv[1], sys.argv[2]
ACCENT = re.compile("[॑-॔᳐-᳿꣠-ꣷ̀-ͯ]")
def norm(t):
    t = unicodedata.normalize("NFC", ACCENT.sub("", t))
    t = t.replace("ँ", "ं")  # then drop nasal marks below
    return re.sub("[\\sंँ।॥ऽ0-9०-९\\-\u200c\u200d]", "", t)
ours = {}
for f in sorted(glob.glob(f"{book}/text/*.md")):
    for line in open(f, encoding="utf8").read().split("\n"):
        if line:
            i, t = line.split(" | ", 1)
            v = int(re.match(r"\d\d\.\d\d\.(\d+)", i).group(1))
            ours.setdefault(v, []).append(t)
data = json.load(open(s2, encoding="utf8"))
riks = {r["global_no"]: r["samhita"] for c in data[:3]
        for s in c["sections"] for r in s["riks"]}
same, diff = 0, []
for n in range(1, 586):
    a, b = norm(" ".join(ours[n])), norm(riks.get(n, ""))
    if a == b:
        same += 1
    else:
        diff.append((n, a, b))
print("compared 585; identical after normalising:", same, "different:", len(diff))
import difflib, collections
per_chapter = collections.Counter()
out = ["# Cross-check S1 against S2 (verses 1-585)", "",
       "S1 = sv-kauthuma.itx; S2 = github.com/Malolan05/samaveda "
       "(accent-marked text). Compared after removing accent signs, spaces, "
       "dandas, anusvara/chandrabindu, avagraha and pluta marks. Nothing in "
       "the text files was changed because of this list.", "",
       "| Verse | Part.Chapter | S1 fragment | S2 fragment |", "|---|---|---|---|"]
chapter_of = {}
for f in sorted(glob.glob(f"{book}/text/ch01.*.md")):
    for line in open(f, encoding="utf8").read().split("\n"):
        if line:
            i = line.split(" | ")[0]
            chapter_of[int(i.split(".")[2].rstrip("abcdefgh"))] = i[:5]
for n, a, b in diff:
    sm = difflib.SequenceMatcher(None, a, b)
    ops = [(a[i1:i2], b[j1:j2]) for t, i1, i2, j1, j2 in sm.get_opcodes()
           if t != "equal"]
    per_chapter[chapter_of[n]] += 1
    shown = "; ".join(f"{x or '-'} / {y or '-'}" for x, y in ops[:4])
    out.append(f"| {n} | {chapter_of[n]} | "
               + " ; ".join(x or "-" for x, _ in ops[:4]) + " | "
               + " ; ".join(y or "-" for _, y in ops[:4]) + " |")
print("verses differing per chapter:", dict(per_chapter))
open(f"{book}/notes/crosscheck-s2.md", "w", encoding="utf8").write(
    "\n".join(out) + "\n")
