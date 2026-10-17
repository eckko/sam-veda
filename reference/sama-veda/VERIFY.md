# Verification log: sama-veda

Dated log of the verify-vedic-book-reference stage. Append only.

## 2026-10-17
- Branch: docs/2026-10-17/version-1 (continued from the extraction stage).
- Inventory: Devanagari base is `text/` (36 files, FORMAT.md layout). Other files are from the extraction stage: `notes/` (annotations, cross-check with S2), `tools/` (parser, toc generator, cross-check), `reference/tools/check_extraction.py`. Original ITRANS source is not in the repo (owner decision).
- Owner answers: second edition for the word checker: skip (no complete second edition available).
- structure_check.py: no flags (4 parts, 36 chapters, 1875 verse numbers, no gaps, toc and text agree). check_extraction.py: 0 errors, 0 warnings.
- word_check.py (second edition skipped): 0 stray characters; 7 typo candidates (all around the word पवमान, which has many case forms, plus धारयापो and हवामह); metre table not used for AI packing, because the verse lines are Vedic chandas (mostly 8-, 11- and 12-akshara padas), so the table's 15-17/22-23 range flags 1090 of 3715 lines without meaning anything.
- Proofreading pack: 7 typo candidates plus a fixed-seed sample of ordinary lines (one in 25, seed 7) for the error rate; metre lines not packed.
- AI proofreading (3 packs, 165 items, strongest available model, one agent per pack): 4 proposals, sample error rate 2 of 158 (1.3%). All four trace to the ITRANS source's own typing; see ISSUES.md. About 4% of lines read; no person has read the rest.
