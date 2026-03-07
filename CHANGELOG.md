# CHANGELOG

All notable changes to this project will be documented in this file.

The format follows semantic versioning (MAJOR.MINOR.PATCH).

---

## [0.2.0] - 2026-02-28

### Added
- App specification report (`reports/m2_spec.md`) with job stories, component inventory, reactivity diagram (Mermaid), and calculation details
- 
- App specification (`reports/m2_spec.md`) with job stories, component inventory, reactivity diagram, and calculation details
- Deployed app on Posit Connect Cloud on `main` (stable) and `dev` (preview) branches
- Sidebar with year slider, region dropdown, country dropdown, and cost category radio buttons
- 4 KPI value boxes: number of countries, average, min, and max daily cost (USD)
- Choropleth world map of healthy diet cost by country (`plot_map`)
- Added color scale to world map based on theme- `rdylbu`
- Line chart of top 10 countries with highest cost increase over selected period (`plot_trend`)
- Bar chart of average cost by region (`bar_chart`)
- Box plot of cost distribution by year and region (`plot_box`)
- Dynamic country dropdown that updates based on selected region
- General plotly-white theme added to all charts
- `requirements.txt` and `environment.yml` with pinned versions for deployment and local dev
- Demo GIF (`img/demo.gif`)
- Countries-by-continent lookup data (Kaggle) and support for downloading it
- Added lookup table for country ISO code (required by Choropleth chart)
- Countries-by-continent lookup file stored in `data/lookups/` (snake_case filename)
- **Complexity Enhancement:** Reset button using `@reactive.event(input.reset)` to restore all filters to defaults

### Changed
- Moved data scripts from `data/` to `scripts/`
- `cost_cat` filter changed from dropdown to radio buttons for better usability
- Country dropdown now filters dynamically by selected region
- Added/updated country name normalization to improve join consistency across sources
- Minor edits to line and bar charts - data aggregations

### Fixed
- Removed unused `__init__.py`
- Removed non-existent `shinywidgets==0.3.5` from `requirements.txt` — package not used in app
- Fixed `shiny==1.2.1` to `shiny==1.3.0` after Posit Connect Cloud deployment failure
- Fixed region assignment issues introduced by inconsistent country naming (via normalization + updated lookup)

### Known Issues
- `plot_trend` color map uses region names but colors by country — lines fall back to default Plotly colors
- Data cleaning required for region and country data
- Bar chart title says "Latest Year" but actually aggregates the full filtered year range
- No app footer yet (authors, repo link, last updated)
- Colorblind safety of `region_colors` and `rdylbu_r` palette not verified
- Reactivity diagram in spec uses wrong node shapes (should follow Lecture 3 notation)
- Incorrect edge in diagram: `bar_chart → plot_box` should be `filtered() → plot_box`

---

## Reflection (Milestone 2)

### Implementation Status
- **Fully implemented:** J1 (regional comparison), J2 (trends over time), J4 (high-cost identification), J5 (cost trend visualization)
- **Partially implemented:** J3 and J6 — cost category filter works but no component-level chart (fruits/vegetables) yet
- **Pending M3:** Component cost breakdown chart to fully address J3 and J6

### Layout Comparison
- Final layout matches M2 spec: value boxes (row 1), map (row 2), line + bar side by side (row 3), box plot (row 4)
- Matches M1 sketch overall; only change is `cost_cat` switched from dropdown to radio buttons

### Deviations from Original Plan
- `cost_cat` uses `ui.input_radio_buttons()` instead of `ui.input_select()` — spec table needs correction
- Component cost chart (fruits/vegetables) deferred to M3 due to sparse data

### Known Limitations
- Narrow filter combinations (single country + single year) can produce empty or broken charts
- `plot_map` always shows latest year in range, which may be unintuitive when year range is narrowed
- Empty filter results not handled with user-friendly messages

### Best Practices (DSCI 531)
- All charts have axis labels, titles, and units on value boxes
- Consistent regional color palette across charts; colorblind safety to be verified in M3

### Self-Assessment
- **Strengths:** Clean reactive architecture with single `filtered()` calc; dynamic country filter; reset button adds good UX
- **Limitations:** Component breakdown not built yet; diagram notation errors to fix; footer and demo GIF still needed
- **Planned for M3:** Fix color bug in `plot_trend`, add footer, verify palette, fix diagram, add component cost chart