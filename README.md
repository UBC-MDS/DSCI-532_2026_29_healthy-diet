# Global Cost of a Healthy Diet Dashboard

|  |  |
|--|--|
| **Stable** | https://connect.posit.cloud/suryashchakravarty/content/019ca6ef-74fa-a36e-c837-851eb85c3f24 |
| **Preview** | https://019ca57d-6583-da29-765f-1a716196111d.share.connect.posit.cloud/ |
| **Python** | [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) |

An interactive dashboard for exploring the global cost of a healthy diet across 175 countries from 2017 to 2024. All costs are PPP-adjusted USD per person per day.

---

## Features

**Dashboard** — Filter by year, region, country, and cost category. Explore a choropleth world map, regional cost comparisons, cost trends over time, and distribution by region.

**AI Chatbot** — Ask plain-English questions to filter and explore the data. Results update a table, bar chart, and trend line in real time. Filtered data can be downloaded as CSV.

---

## Contributors

- [Jade Chen](https://github.com/jadeeechen)
- [Hooman Esteki](https://github.com/hoomanesteki)
- [Luis Alvarez](https://github.com/luisalonso8)
- [Suryash Chakravarty](https://github.com/suryashch)

---

## Local Setup

### 1. Clone

```bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_29_healthy-diet.git
cd DSCI-532_2026_29_healthy-diet
```

### 2. Environment

**Conda (recommended)**
```bash
conda env create -f environment.yml
conda activate 532-healthy-diet
```

**pip**
```bash
pip install -r requirements.txt
```

### 3. API Keys

**Anthropic** — required for the AI Chatbot tab. Create `src/.env`:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
> Get a key at https://console.anthropic.com. The Dashboard tab works without it.

**Kaggle** — required to download the dataset on first run. Add to `~/.kaggle/kaggle.json` or set as environment variables:
```
KAGGLE_USERNAME=your-username
KAGGLE_KEY=your-key
```

### 4. Run

```bash
python -m shiny run --reload src/app.py
```

Open http://127.0.0.1:8000

---

## Deployment

On Posit Connect Cloud, set these environment variables before deploying:

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | AI Chatbot tab |
| `KAGGLE_USERNAME` | Dataset download |
| `KAGGLE_KEY` | Dataset download |

Dependencies install automatically from `requirements.txt`.

---

## Repository Structure

```
├── environment.yml       # Conda environment (local dev)
├── requirements.txt      # Pip dependencies (deployment)
├── src/
│   ├── app.py            # Shiny application
│   ├── .env              # API keys — do not commit
│   ├── scripts/
│   │   ├── download_data.py
│   │   └── clean_data.py
│   └── data/
│       ├── raw/
│       ├── processed/
│       └── lookups/
├── reports/
├── img/
└── CHANGELOG.md
```

---

## Dataset

**Source:** FAO / World Bank via Kaggle — 1,379 records, 175 countries, 2017–2024.

| Column | Description |
|---|---|
| `country` | Country name |
| `region` | Regional grouping |
| `year` | Year (2017–2024) |
| `cost_healthy_diet_ppp_usd` | Daily cost in PPP-adjusted USD — primary metric |
| `cost_category` | "High Cost" or "Low Cost" classification |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, commit, and pull request guidelines.
