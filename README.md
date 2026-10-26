# Theory-guided AI reveals how climate extremes reshape global tree growth

Code and derived site-level results for:

> Ercanlı, İ. *Theory-guided AI reveals how climate extremes reshape global tree growth.* Manuscript in preparation.

Companion study (model development and projections, separate repository):
> Ercanlı, İ. *Growth theory changes projected tree-growth responses to climate despite similar historical skill.* Manuscript under review.
> Code: <https://github.com/ilkerercanli/growth-theory-ai>

## What this repository contains

| Folder | Content |
|---|---|
| `notebooks/` | Google Colab notebooks (Defter 11–18) that produce every number in the manuscript. They load the models trained in the companion repository; **no model is retrained here**. |
| `figures/` | Python scripts that draw Figs 1–4 and Extended Data Figs 1–2 from the result tables (`blok.py` holds the spatial-block results copied from the tables). |
| `app/` | Interactive explorer: `index.src.html` (template), `data.json` (derived site-level results), `build.py` (inlines the data). |
| `docs/` | Built explorer (`index.html`) for GitHub Pages. |
| `results/result_provenance.csv` | For every result table: the notebook that produced it, the run date (UTC) and the random-seed note. All tables come from a single version of the prepared data set. |

## Notebooks

| Notebook | Purpose |
|---|---|
| Defter 11 | Attribution with observed and ISIMIP3a counterfactual climate |
| Defter 12 | Classical methods (response function, VS-Lite) and detection test |
| Defter 13 | Extreme years: frequency, observed responses, model responses |
| Defter 14 | Growth change through extreme years (equations 4–5) and limiting factor |
| Defter 15 | Independent tests, robustness, confounding, spatial-block intervals |
| Defter 16 | Same-target comparison, paired differences, block size, block-shared permutation |
| Defter 17 | Predicted − observed differences with paired spatial-block intervals |
| Defter 18 | Change in responses between 1902–1960 and 1961–2019 |

Run order: the companion repository's data preparation and training notebooks first, then Defter 11 → 18 in Google Colab (GPU recommended for 11–17; Defter 18 needs no GPU). Outputs are written to `ANALIZ_SON/` in the user's Google Drive.

## Data and permissions

- **Tree rings:** International Tree-Ring Data Bank (NOAA World Data Service for Paleoclimatology). Raw measurements are **not redistributed**; the companion repository provides the study codes and code that retrieves the identical data set. Records with withheld coordinates or third-party permission were excluded.
- **Climate:** CRU TS 4.09 (Open Government Licence v3); ISIMIP3a GSWP3-W5E5 obsclim and counterclim.
- `app/data.json` contains only derived site-level quantities (growth change through extreme years, event effects, frequency changes, limiting-factor shares) and public site metadata (study code, coordinates, genus, region).

## Interactive explorer

Open `docs/index.html` in a browser, or enable GitHub Pages on the `docs/` folder. To rebuild after changing the data: `python app/build.py`.

## Citation and licence

Please cite the article (DOI to be added on publication; archived on Zenodo). Code is released under the MIT licence (`LICENSE`).
