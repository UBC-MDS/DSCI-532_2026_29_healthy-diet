# Global Cost of a Healthy Diet Dashboard

|        |        |
|--------|--------|
| Documentation | _Coming soon_ |
| Package | [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) |
| CI | _Coming soon_ |

## Contributors

- [Jade Chen](https://github.com/jadeeechen)
- [Hooman Esteki](https://github.com/hoomanesteki)
- [Luis Alvarez](https://github.com/luisalonso8)
- [Suryash Chakravarty](https://github.com/suryashch)

## Summary

This dashboard enables cross-country and regional comparisons of the cost of a healthy diet from 2017 to 2024 using PPP-adjusted USD. Users can explore geographic patterns on a world map, compare trends over time for selected countries, and examine regional distributions to understand disparities in affordability. The app also supports quick identification of high-cost versus low-cost contexts using the dataset's `cost_category` classification. Intended users include policy analysts, public health researchers, and international development organizations.

## Dataset

The dataset contains **1,379 records** of country-year observations covering **175 countries** across **2017 to 2024**. Costs are reported in **Purchasing Power Parity (PPP) adjusted USD**, which supports cross-country comparisons by accounting for differences in cost of living.

### Key columns used in the app

- `country`: country name
- `region`: region grouping used for comparisons
- `year`: year (2017 to 2024)
- `cost_healthy_diet_ppp_usd`: daily cost of a healthy diet (PPP-adjusted USD). This is the primary metric used throughout the dashboard and is expected to be complete.
- `cost_vegetables_ppp_usd`, `cost_fruits_ppp_usd`: component costs (PPP-adjusted USD). These may be sparse and are best used for exploratory checks rather than core comparisons.
- `cost_category`: ordinal/categorical classification (for example, "High cost" vs "Low Cost"). A small fraction of values may be missing.

## Repository structure

- `src/app.py`: Shiny for Python application entry point
- `src/download_data.py`: helper used by the app to load and return the dataset (via `get_data()`)
- `reports/`: project report materials (proposal, figures)
- `img/`: figures used in the proposal and documentation

## Setup

### 1) Create the conda environment

From the repository root:

```bash
conda env create -f environment.yml
````

### 2) Activate the environment

```bash
conda activate 532-healthy-diet
```

## Running the dashboard

From the repository root:

```bash
python -m shiny run --reload src/app.py
```

Open the app in your browser at the URL printed in the terminal (for example, `http://127.0.0.1:8000`):

```bash
Uvicorn running on http://127.0.0.1:8000
```

* If your app relies on local data files, ensure `download_data.get_data()` can find them when run from the repository root.

## How the app works (high level)

* Filters: year range (slider), region, country, and cost category.
* Outputs:

  * Summary cards: number of countries, average/min/max daily cost
  * Visuals: map, time trend line chart, average cost by region bar chart, and a boxplot over time