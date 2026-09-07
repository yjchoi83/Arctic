# build.md — rendering MANUSCRIPT.md for two journal styles

`MANUSCRIPT.md` is written in Pandoc-flavoured Markdown with author-year citations that resolve to
`references.bib`. Both target styles are produced from the same source; only the CSL file changes.

## Prerequisites

    pandoc >= 3.1
    # CSL styles, fetched once:
    curl -sLo elsevier-harvard.csl https://www.zotero.org/styles/elsevier-harvard
    curl -sLo ieee.csl            https://www.zotero.org/styles/ieee

Pandoc is not installed in the analysis environment used to produce this draft, so the commands below are
recorded but have not been executed here.

## Remote Sensing of Environment version (author-year, Elsevier Harvard)

    pandoc MANUSCRIPT.md \
      --from=markdown+pipe_tables+tex_math_dollars \
      --citeproc --bibliography=references.bib --csl=elsevier-harvard.csl \
      --resource-path=.:figures \
      --metadata title="Hazard-timescale observability of Arctic shipping chokepoints: what Sentinel-1 could and could not see" \
      --number-sections \
      -o MANUSCRIPT_RSE.docx

    # PDF variant
    pandoc MANUSCRIPT.md --from=markdown+pipe_tables+tex_math_dollars \
      --citeproc --bibliography=references.bib --csl=elsevier-harvard.csl \
      --resource-path=.:figures --number-sections \
      --pdf-engine=xelatex -V geometry:margin=25mm -V fontsize=11pt \
      -o MANUSCRIPT_RSE.pdf

## IEEE version (numeric)

    pandoc MANUSCRIPT.md \
      --from=markdown+pipe_tables+tex_math_dollars \
      --citeproc --bibliography=references.bib --csl=ieee.csl \
      --resource-path=.:figures --number-sections \
      -o MANUSCRIPT_IEEE.docx

Switching to IEEE changes only the CSL. In-text author-year forms such as "Korosov and Rampal (2017)" that are
written as prose rather than as `[@korosov2017combination]` will not be renumbered automatically; before an IEEE
submission those prose forms should be converted to bracketed citation syntax. The current draft uses prose
citations throughout because the primary target is RSE.

## Reference counts by venue

| Venue | Count |
|---|---|
| other journals | 15 |
| The Cryosphere | 13 |
| Remote Sensing of Environment | 9 |
| IEEE Trans. Geosci. Remote Sens. | 9 |
| J. Geophys. Res. Oceans | 7 |
| IEEE J. Sel. Top. Appl. Earth Obs. | 5 |
| Marine Policy | 4 |
| IGARSS (conference) | 3 |
| MDPI journals | 2 |
| Annals / J. Glaciology | 2 |
| grey literature | 2 |
| Cold Reg. Sci. Technol. | 2 |
| books and chapters (Feller, Cox, Geiger and Drinkwater) | 3 |
| Earth Syst. Sci. Data | 1 |
| Geophys. Res. Lett. | 1 |
| **Total** | **78** |

Targets set for this bibliography were: Remote Sensing of Environment >= 8, IEEE TGRS >= 6, IEEE JSTARS >= 4,
The Cryosphere >= 6, at most 5 MDPI items, and at least 45 verified references overall. All are met.

## Submission items

| Item | File | Requirement |
|---|---|---|
| Highlights | `HIGHLIGHTS.md` | 5 bullets, ≤ 85 characters each including spaces; verified in-file |
| Graphical abstract | specification in `HIGHLIGHTS.md` | single landscape panel, ≥ 1600 × 900 px, TIFF or EPS at submission |
| Supplementary material | `SUPPLEMENTARY.md` | Supplementary Table S1, the Section 3.6 matcher parameters; cited from §3.6 and Data availability |
| Word count | see `NUMBERS_TRACE.md` §"Word budget and trims" | main text ≤ 9,500 words excluding headings, tables, figure captions and back matter |

Highlights and the supplementary table are separate uploads in the Elsevier system and must not be pasted into
`MANUSCRIPT.md`. To re-check the highlight character limit:

    python3 - <<'EOF'
    for l in open("HIGHLIGHTS.md"):
        if l.startswith("- "): print(len(l[2:].rstrip()), l.rstrip())
    EOF

## Figures

All figures are PNG at 150 dpi in `figures/`. For submission they should be regenerated as vector or 300 dpi
raster by editing `savefig.dpi` in `scratch/P9/p10_figs.py` and rerunning it; the script rebuilds every figure
from the committed result tables.
