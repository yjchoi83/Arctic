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
      --metadata title="Hazard-timescale observability of Arctic shipping chokepoints" \
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
| other journals | 16 |
| The Cryosphere | 13 |
| Remote Sensing of Environment | 9 |
| J. Geophys. Res. Oceans | 7 |
| IEEE Trans. Geosci. Remote Sens. | 6 |
| IEEE J. Sel. Top. Appl. Earth Obs. | 5 |
| Marine Policy | 4 |
| IGARSS (conference) | 3 |
| MDPI journals | 3 |
| Annals / J. Glaciology | 2 |
| grey literature | 2 |
| Cold Reg. Sci. Technol. | 2 |
| books (Feller, Cox) | 2 |
| Earth Syst. Sci. Data | 1 |
| Geophys. Res. Lett. | 1 |
| **Total** | **76** |

Targets set for this bibliography were: Remote Sensing of Environment >= 8, IEEE TGRS >= 6, IEEE JSTARS >= 4,
The Cryosphere >= 6, at most 5 MDPI items, and at least 45 verified references overall. All are met.

## Figures

All figures are PNG at 150 dpi in `figures/`. For submission they should be regenerated as vector or 300 dpi
raster by editing `savefig.dpi` in `scratch/P9/p10_figs.py` and rerunning it; the script rebuilds every figure
from the committed result tables.
