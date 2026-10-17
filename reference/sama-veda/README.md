# Sama Veda Samhita (Kauthuma Shakha): raw extracted source bank

Stage 1 (extraction) of a pipeline: verify, review, fix, proofread come next. This folder holds the raw text, not a finished edition. Nothing here has been proofread.

Read, in order: FORMAT.md (file and line format), toc.md (structure), STATUS.md (what is done), sources.md (where text came from), ISSUES.md (known doubts).

What is here: all 1875 verses of S1 (`sv-kauthuma.itx`) in 36 files under `text/`: part 01 Purvarcika (12 chapters), part 02 Aranya Arcika (`p02.md`), part 03 Mahanamnya Arcika (`p03.md`), part 04 Uttararcika (22 chapters). Chapter = ardha. Verse numbers run 1 to 1875 across the whole book, as in the file. Line letters a, b, c follow the order of the lines in the source (the source's own a/c/e markers are not used).

Extra files (beyond FORMAT.md): `notes/annotations.md` (rishi, chandas and devata lines the file prints before 8 suktas of the Uttararcika) and `notes/crosscheck-s2.md` (differences from a second text for verses 1-585). `tools/` holds the parser (`parse_itx.py`), the toc generator (`make_toc.py`) and the cross-check (`crosscheck_s2.py`). The original S1 file is not stored here (see sources.md).

Rules for anyone editing here:
- Text lines come only from sources listed in sources.md; never from memory.
- Do not rename files or change line IDs of finished chapters.
- Record every doubt in ISSUES.md; fix text only in a later, explicit proofreading stage.
- Run `python3 -I reference/tools/check_extraction.py reference/sama-veda` before every commit.
- Branch pattern: `docs/YYYY-MM-DD/version-N`; push new branches only; the owner merges.

How to continue: open STATUS.md and ISSUES.md; the Sanskrit is complete, so next are translations (Hindi, English) and verification against a second source.

## Layers
Word-split (`-sandhi`), Hindi (`-hindi`) and English (`-english`) files exist for parts 01, 02 and 03 (650 of 1875 verses) as reviewed AI drafts that no person has read. Part 04 has none. See STATUS.md, ISSUES.md and VERIFY.md.
