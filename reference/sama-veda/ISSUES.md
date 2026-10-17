# Issues: sama-veda

Nothing in the text files was changed because of these. Line IDs are the new IDs (PP.CC.V + line letter).

| Line ID | Kind | What | Source(s) | Suggested check |
|---|---|---|---|---|
| 01.06.243a | numbering | Source coordinates give verse 243 prapathaka 3, ardha 1, but the heading above it starts ardha 2 (and S2 also puts it in ardha 2). Heading used, so 243 is the first verse of 01.06 | S1, S2 | check printed edition |
| 04.07.1035b | other | Source line has a stray `rm` before its coordinates; the verse text is unaffected | S1 | none needed |
| 04.09.1179b | numbering | Source prints `1181` here and again at 04.09.1181b; the running count (1179) is used as the verse number | S1 | check printed edition |
| 04.09.1211b | numbering | Source verse number is damaged (`121chlsdir`); the running count (1211) is used; the garbled token is not in the text | S1 | check printed edition |
| 01.08.387b | other | Double space before the closing danda in the source; collapsed to one space | S1 | none needed |
| 04.17.1620b | other | Same: double space before the closing danda collapsed | S1 | none needed |
| 04.01.666a | numbering | Source coordinates repeat `06 03` for verses 666, 667 and 668 (not used in IDs) | S1 | none needed |
| 01.01.2a | other | `.N` in ITRANS is converted to chandrabindu (ँ), e.g. यज्ञानाँ; it occurs 885 times and `M` gives anusvara. Check whether the typist meant `.N` as chandrabindu everywhere | S1 | compare with S3/S4 or the printed edition |
| 01.01-01.12 | variant | 105 of verses 1-585 differ from S2 by one fragment (spelling, an extra or missing sign); full list in notes/crosscheck-s2.md, keyed by verse number | S1, S2 | compare with S3/S4 or the printed edition |
| 01.09.391a | order | Chapter boundaries inside the Purvarcika differ from S2 at prapathaka 5 and 6 (S1: 46+50 and 58+41 verses; S2: 45+50 and 60+40). Kanda totals agree (Agneya 114, Aindra 352, Pavamana 119) | S1, S2 | check printed edition |
| 01.02.82b | possible-typo | S1 has `ष` at the end of `आनुषक्षर्म`; S2 reads `आनुषक् शर्म` (word split and श) | S1, S2 | check printed edition |
| 01.02.85a | possible-typo | S1 reads `विष`, S2 reads `विश` | S1, S2 | check printed edition |
| 01.03.110a | possible-typo | S1 reads `एशः`, S2 reads `एषः` | S1, S2 | check printed edition |
| 04.20.1788b | possible-typo | `पनिष्तम` (source `paniShtama`): ष्त is not a valid conjunct here; AI proposes `पनिष्टम` | S1 | check printed edition |
| 04.10.1312a | possible-typo | `पवमान्` before a space (source `pavamAn`); AI proposes `पवमान` | S1 | check printed edition |
| 04.08.1127b | possible-typo | `पस्यति` (source `pasyati`); AI proposes `पश्यति` | S1 | check printed edition |
| 04.05.952a | possible-typo | `हरिह` (source `hariha`) is not a recognised form; AI is unsure and gives no suggestion | S1 | check printed edition |

## Verification summary (2026-10-17)

- Structure: no gaps or truncated part; 4 parts, 36 chapters, 1875 verse numbers; toc and text agree (structure_check.py).
- Word checker: 0 stray characters; 7 typo candidates, all read by the AI pass and judged regular forms except 04.10.1312a; the metre table (1090 of 3715 lines outside 15-17/22-23 aksharas) is not meaningful for Vedic chandas and was not sent to the AI pass. Second edition: skipped.
- AI proofreading: 165 items read (7 typo candidates and a fixed-seed sample of 158 ordinary lines, one in 25), 4 proposals (3 errors, 1 unsure). Sample error rate 2 of 158 lines (1.3%). This covers about 4% of the 3715 lines; the other lines were not read by the AI pass or by a person. Nothing in text/ was changed.
| 03.01.648 | layer-decision | last clause: finite "you take up" (kept) or infinitive "to take up" | layers | person to decide |
| 02.01.588 | layer-decision | Hindi supplies ऐश्वर्य for rantyam bṛhat; English brackets "(domain)" | layers | person to decide |
| 02.01.586 | possible-typo | `पुपुरि` vs RV `पप्री`-type reading (draft flag "possible", Rigveda parallel) | layers | check printed edition |
