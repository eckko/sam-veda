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
- Layers (2026-10-17), owner chose parts 03 + 02 as the pilot (65 verses, 2 chunks). Draft and independent review by separate agents on the strongest model; check_chunk and apply_review run. Part 03: 24 patches (3 error, 18 minor). Part 02: 34 patches (3 error, 19 minor). Written: text/p02-{sandhi,hindi,english}.md and p03-*. check_extraction: 0 errors, 0 warnings. Reviewed AI drafts: no person has read them. Open for a person: 03 verse 648 (finite verb vs infinitive in the last clause), 02 verse 588 (supplied noun ऐश्वर्य in Hindi). Low-confidence units: 02: 588, 606, 611; 03: 642. Parts 01 and 04 not layered; no feed built yet (waiting for the owner's sample check).
- Layers part 01 (Pūrvārcika, 585 verses, 12 chunks): drafted and independently reviewed on Sonnet 5.5 at the owner's request ("continue with sonnet 5.5"); review fixes per chunk: 29, 75, 29, 53, 30, 72, 99, 87, 114, 96, 88, 110 patches. One cleanup pass removed parentheses from 22 Hindi lines of 01.04 (verified by script). Written as text/ch01.NN-{sandhi,hindi,english}.md; check_extraction 0 errors, 0 warnings. 5 Hindi lines still have parentheses or placeholder text (listed in ISSUES.md). Reviewed AI drafts; no person has read them. Parts 02, 03 drafted on Fable; part 04 not started; no feed built.
