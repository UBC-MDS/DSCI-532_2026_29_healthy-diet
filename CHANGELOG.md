# CHANGELOG

All notable changes to this project will be documented in this file.

The format follows semantic versioning (MAJOR.MINOR.PATCH).

---

## [0.4.0] - 2026-03-15

### Added
- **Parquet + DuckDB** (#94): processed dataset now exported as `data/processed/cleaned_price_of_healthy_diet.parquet` alongside existing CSV (`src/scripts/clean_data.py`)
- **Parquet + DuckDB** (#94): `duckdb==1.1.3` and `pyarrow==14.0.2` added to `requirements.txt`, `src/requirements.txt`, and `environment.yml`
- **Docs** (#95): `README.md` updated with Data Pipeline section showing the full data flow from Kaggle through DuckDB; repository structure updated to reflect parquet file and inline descriptions


### Changed
- **Parquet + DuckDB** (#94): data loading switched from `pd.read_csv` to DuckDB `CREATE VIEW` over parquet; metadata queries now run as SQL (`src/app.py` lines 23-44)
- **Parquet + DuckDB** (#94): `filtered()` builds a SQL `WHERE` clause before `.df()` — filtering happens at DB level, not in memory (`src/app.py` lines 525-532)
- **Parquet + DuckDB** (#94): cascade dropdown and click handlers use DuckDB queries and pre-built lists instead of the global pandas DataFrame (`src/app.py` lines 513-522, 722-766)
- **Dependency setup** (#97): removed duplicate repo-root `requirements.txt` so `src/requirements.txt` is the single maintained dependency file for the deployed app
- **Docs** (#97): `README.md` pip installation instructions updated from `pip install -r requirements.txt` to `pip install -r src/requirements.txt`
- **app.py** (#101): Bar chart values were being cut off at the top- changed location of values to be inside of bar visual.
- **Map layout** (#100): Diet Cost Map now fills the dashboard tile with reduced whitespace
  - `.card-body` padding set to `0` so Plotly charts use the full card area (`src/app.py` line 239)
  - Default world map bounds widened horizontally and trimmed vertically (`lonaxis_range=[-180,180]`, `lataxis_range=[-5,75]`) to better match Mercator projection proportions (`src/app.py` lines 600-603)
  - Plotly layout adjusted so the geo domain uses almost the full figure width and the colorbar sits closer to the map (`src/app.py` lines 615-628)

### Fixed
- **Blank charts on load** (#93): all 4 chart panels rendered blank on initial page load while KPI cards were unaffected
  - Root cause: `include_plotlyjs="cdn"` embedded a CDN `<script>` inside each dynamically injected `@render.ui` block — Plotly loaded async but `Plotly.newPlot()` fired sync
  - Fix: `PLOTLY_CDN_SCRIPT` added as a static page-level tag; all 6 `fig.to_html()` calls changed to `include_plotlyjs=False` (`src/app.py` lines 469, 489, 612, 639, 675, 701)
- **Map year label** (#102): map card header now displays "Showing data for {year}" dynamically, clarifying that the map always shows the latest year in the selected range (`src/app.py`)

---
---

## [0.3.0] - 2026-03-08

### Added
- **AI Chatbot tab** powered by Claude (Anthropic) via `querychat`:
  - Plain-English chat interface to query and filter the dataset (also available in Spanish)
  - Filtered dataframe displayed as an interactive table
  - Two reactive visualizations (bar chart + trend line) that update from chatbot output
  - Download button to export chatbot-filtered data as CSV
- `ANTHROPIC_API_KEY` support via `src/.env` file (local) and deployment environment variable
- `querychat`, `chatlas`, `anthropic`, and `python-dotenv` added to both `environment.yml` and `requirements.txt`

### Changed
- **Map:** switched to Mercator projection; region-level zoom uses fixed bounding boxes instead of globe rotation; country name labels shown only when ≤12 countries are in view to avoid clutter
- **Sidebar filter order:** Year Range → Cost Category → Region → Country → Reset; thin dividers between groups; no excess whitespace
- **Dashboard layout:** KPI row → Map + Bar (7/5 split) → Trend + Box (7/5 split); explicit 14px gap between rows
- **KPI cards:** replaced default `value_box` with custom HTML cards — deep navy background, white text, always readable regardless of theme
- **Navbar:** white background with dark text and blue active-tab underline (was dark/inverse, text was invisible)
- All emojis removed from UI labels and card headers
- Default filters reset to: all years (from earliest), All cost categories, All regions, All countries
- Chart margins, heights, and font sizes unified across all plots
- Hover tooltips on map show country name, region, and formatted cost

### Fixed
- `showborders` invalid Plotly geo property removed (caused map to crash on load)
- Deprecated `bg`/`inverse` args in `page_navbar` replaced with `navbar_options=ui.navbar_options(...)`
- `CUSTOM_CSS` moved inside `nav_panel` (was incorrectly placed as direct child of `page_navbar`, causing `AttributeError`)
- Year axis showing float values (e.g. `2,020.5`) fixed with `tickformat="d"` and `type="category"`
- Chatbot tab scroll issue — redesigned with flexbox so only the message area scrolls, not the whole page
- `querychat.init()` deprecated API replaced with `QueryChat()` class

### Known Issues
- `querychat` welcome message styling inherits from the library and cannot be fully overridden via CSS
- Map `fitbounds` for single-country zoom may include surrounding ocean for island nations
- Colorblind safety of `region_colors` and `rdylbu_r` palette not yet verified

### Reflection
- Integrating `querychat` required migrating from the deprecated `querychat.init()` API to the new `QueryChat()` class
- CSS specificity conflicts with bslib's sidebar component required `!important` overrides on multiple spacing properties
- Keeping the chatbot panel fixed-height without page scroll required a full flexbox layout rebuild

---

## [0.2.0] - 2026-02-28

### Added
- App specification report (`reports/m2_spec.md`) with job stories, component inventory, reactivity diagram (Mermaid), and calculation details
- Deployed app on Posit Connect Cloud on `main` (stable) and `dev` (preview) branches
- Sidebar with year slider, region dropdown, country dropdown, and cost category radio buttons
- 4 KPI value boxes: number of countries, average, min, and max daily cost (USD)
- Choropleth world map of healthy diet cost by country (`plot_map`)
- Color scale on world map using `rdylbu` theme
- Line chart of top 10 countries with highest cost increase over selected period (`plot_trend`)
- Bar chart of average cost by region (`bar_chart`)
- Box plot of cost distribution by year and region (`plot_box`)
- Dynamic country dropdown that updates based on selected region
- General `plotly_white` theme applied to all charts
- `requirements.txt` and `environment.yml` with pinned versions for deployment and local dev
- Demo GIF (`img/demo.gif`)
- Countries-by-continent lookup data (Kaggle) and support for downloading it
- Lookup table for country ISO codes (required by choropleth chart)
- Countries-by-continent lookup file stored in `data/lookups/`
- **Complexity Enhancement:** Reset button using `@reactive.event(input.reset)` to restore all filters to defaults

### Changed
- Moved data scripts from `data/` to `scripts/`
- `cost_cat` filter changed from dropdown to radio buttons for better usability
- Country dropdown now filters dynamically by selected region
- Added/updated country name normalization to improve join consistency across sources
- Minor edits to line and bar chart data aggregations

### Fixed
- Removed unused `__init__.py`
- Removed non-existent `shinywidgets==0.3.5` from `requirements.txt`
- Fixed `shiny==1.2.1` to `shiny==1.3.0` after Posit Connect Cloud deployment failure
- Fixed region assignment issues caused by inconsistent country naming

### Known Issues
- `plot_trend` color map uses region names but colors by country — lines fall back to default Plotly colors
- Bar chart title says "Latest Year" but actually aggregates the full filtered year range
- No app footer yet (authors, repo link, last updated)
- Colorblind safety of `region_colors` and `rdylbu_r` palette not verified
- Reactivity diagram in spec uses wrong node shapes and has an incorrect edge (`bar_chart → plot_box` should be `filtered() → plot_box`)

### Reflection (Milestone 2)
- **Fully implemented:** J1 (regional comparison), J2 (trends over time), J4 (high-cost identification), J5 (cost trend visualization)
- **Partially implemented:** J3 and J6 — cost category filter works but no component-level chart yet
- Final layout matches M2 spec; only change is `cost_cat` switched from dropdown to radio buttons
- **Planned for M3:** Fix color bug in `plot_trend`, verify palette, add component cost chart, add footer

---

## [0.1.0] - 2026-02-11

### Added
- Initial project structure
- Data download and cleaning pipeline (Kaggle → processed CSV)
- Basic Shiny app skeleton with sidebar layout
