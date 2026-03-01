# Global Cost of a Healthy Diet Dashboard

|  |  |
|--|--|
| **Stable deployment (main)** | _Add main Posit URL here_ |
| **Preview deployment (dev)** | https://019ca57d-6583-da29-765f-1a716196111d.share.connect.posit.cloud/ |
| Package | [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) |

## Contributors

- [Jade Chen](https://github.com/jadeeechen)
- [Hooman Esteki](https://github.com/hoomanesteki)
- [Luis Alvarez](https://github.com/luisalonso8)
- [Suryash Chakravarty](https://github.com/suryashch)

## Summary

This dashboard enables cross-country and regional comparisons of the cost of a healthy diet from 2017 to 2024 using PPP-adjusted USD. Users can explore geographic patterns on a world map, compare trends over time for selected countries, and examine regional distributions to understand disparities in affordability. The app also supports quick identification of high-cost versus low-cost contexts using the dataset's `cost_category` classification. Intended users include policy analysts, public health researchers, and international development organizations.

## Demo

![App demo](img/demo.gif)

## Dataset

The dataset contains **1,379 records** of country-year observations covering **175 countries** across **2017 to 2024**. Costs are reported in **Purchasing Power Parity (PPP) adjusted USD**, which supports cross-country comparisons by accounting for differences in cost of living.

### Key columns used in the app

- `country`: country name
- `region`: region grouping used for comparisons
- `year`: year (2017 to 2024)
- `cost_healthy_diet_ppp_usd`: daily cost of a healthy diet (PPP-adjusted USD). Primary metric, complete with no missing values.
- `cost_vegetables_ppp_usd`, `cost_fruits_ppp_usd`: component costs (PPP-adjusted USD). Sparse — best used for exploratory checks only.
- `cost_category`: classification ("High cost" vs "Low Cost"). ~1% missing values.

## Repository Structure

- `src/app.py` — Shiny app entry point
- `scripts/download_data.py` — downloads dataset from Kaggle
- `scripts/clean_data.py` — cleans and joins with country code lookups
- `data/raw/`, `data/processed/`, `data/lookups/` — raw, cleaned, and reference data
- `reports/` — proposal and M2 spec
- `img/` — figures and demo animation
- `environment.yml` — conda environment for local development
- `requirements.txt` — pinned pip dependencies used by Posit Connect Cloud for deployment

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, commit, and pull request guidelines.

## Local Setup

### Option A — Conda (recommended)

Installs all app dependencies plus Jupyter for notebooks.

```bash
conda env create -f environment.yml
conda activate 532-healthy-diet
```

### Option B — pip

Installs only what's needed to run the app (same packages used by Posit Connect Cloud).

```bash
pip install -r requirements.txt
```

### Run the app

```bash
python -m shiny run --reload src/app.py
```

Open `http://127.0.0.1:8000` in your browser.

> **Kaggle API required:** The app downloads and cleans the dataset on first run. Set up `~/.kaggle/kaggle.json` locally, or export `KAGGLE_USERNAME` and `KAGGLE_KEY` as environment variables.

## How the App Works

- **Filters:** year range slider, region dropdown, country dropdown, cost category radio buttons — plus a Reset button to restore all defaults
- **KPI cards:** number of countries, average, min, and max daily cost (USD/day)
- **Visuals:** choropleth world map · top-10 cost increase line chart · average cost by region bar chart · cost distribution box plot by year
