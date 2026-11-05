# Theory-guided AI reveals that a century of climate change has slowed tree growth in dry forests but not in cold ones

Code for:

> Ercanlı, İ. *Theory-guided AI reveals that a century of climate change has slowed tree growth in dry forests but not in cold ones.* Manuscript submitted.

The study attributes changes in annual tree growth in the International Tree-Ring Data Bank (19.4 million rings, 120,332 trees, 6,280 sites) to climate change by driving a theory-guided neural network with the observed CRU TS 4.09 climate and the ISIMIP3a counterfactual climate. It compares the network with a statistical estimate from the rings that uses no network.

Data preparation (ITRDB retrieval, climate extraction, site variables) follows the companion study:
> Ercanlı, İ. *Growth theory changes projected tree-growth responses to climate despite similar historical skill.* Manuscript under review.
> Code: <https://github.com/ilkerercanli/growth-theory-ai>

## Contents

| Folder | Content |
|---|---|
| `notebooks/network/` | Google Colab notebooks for the theory-guided network: year-block cross-validation, training of the 20-member ensemble, attribution, uncertainty and the reviewer analyses |
| `notebooks/ring_based_estimate/` | Notebooks that produce the ring-based estimate of growth change through extreme years (equations 5–6 of the manuscript), its spatial-block intervals, specifications and permutation tests |
| `figures/` | Figure scripts: Defter 22 (Figs 1–6, Extended Data Figs 2–4) and `figures_draft14.py` (revised Figs 2–5 and Extended Data Figs 5–6; Fig. 4a in 100 × log units so that the channel contributions add up, Fig. 4b on sites recorded in every period); `ED1_structure.py` draws Extended Data Fig. 1 |
| `results/result_provenance.csv` | For every result table: the notebook that produced it, the Drive folder, the time of the last change (UTC) and the random seed |
| `archive/` | Notebooks and figure scripts of an earlier version of the study that are not used in the manuscript |

## Notebooks

| Notebook | Purpose | Output folder |
|---|---|---|
| `network/Defter19_year_block_pilot` | Pilot of the year-block cross-validation (five-year blocks, four folds) | `SONUC_19` |
| `network/Defter20_main_run` | Architecture search, main run (4 folds × 5 seeds), comparison without climate, ensemble uncertainty, unseen-site test | `SONUC_20` |
| `network/Defter21_attribution_uncertainty` | Counterfactual climate, attribution by period, decade and channel, limiting factors, growth curves, calibration at unseen sites | `SONUC_21` |
| `network/Defter23A_reviewer_analyses` | Same-site comparison with the ring-based estimate, balanced panels and chain-linked index, spatial-block intervals, age and sampling, bounds, factorial Shapley decomposition, out-of-distribution check | `SONUC_23A` |
| `network/Defter23B_transfer_and_structure` | Network trained on 1902–1960 only; product rule instead of the law of the minimum; comparison of all estimates | `SONUC_23B` |
| `ring_based_estimate/Defter13–16` | Extreme-year frequency and responses, growth change through extreme years, spatial-block intervals, specifications, block size and block-shared permutation | `ANALIZ_SON` |

Run order: the companion repository's data preparation first, then Defter 13–16 and Defter 19 → 20 → 21 → 23A → 23B in Google Colab (L4 or T4 GPU, high RAM), then the figure scripts (`figures_draft14.py` reads the summary tables of SONUC_21, SONUC_23A/23B and the Defter 22 output). Each notebook ends with the line `==== DEFTER NN TAMAM ====`. Comments and printed messages in the notebooks are partly in Turkish.

## Data and permissions

- **Tree rings:** International Tree-Ring Data Bank (NOAA World Data Service for Paleoclimatology). Raw measurements are not redistributed; the companion repository provides the study codes and code that retrieves the identical data set. Records with withheld coordinates or third-party permission were excluded.
- **Climate:** CRU TS 4.09 (Open Government Licence v3); ISIMIP3a GSWP3-W5E5 obsclim and counterclim.
- **Site variables:** SoilGrids 2.0, Copernicus DEM GLO-90, RESOLVE Ecoregions 2017 and Köppen–Geiger 1-km maps (open licences; see Methods).

## Citation and licence

Please cite the article (DOI to be added on publication; the repository will be archived on Zenodo). Code is released under the MIT licence (`LICENSE`).
