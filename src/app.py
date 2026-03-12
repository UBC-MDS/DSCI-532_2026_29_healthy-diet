from shiny import App, ui, render, reactive
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd
import duckdb
from scripts.download_data import download_dataset
from scripts.clean_data import clean_dataset
from dotenv import load_dotenv
from querychat import QueryChat
import chatlas

load_dotenv()

AI_AGENT = "claude-haiku-4-5"

# Data
download_dataset()
clean_dataset()

base_dir = os.path.dirname(os.path.abspath(__file__))

PARQUET_PATH = os.path.join(base_dir, "data/processed/cleaned_price_of_healthy_diet.parquet")
con = duckdb.connect()
con.execute(f"CREATE VIEW diet AS SELECT * FROM read_parquet('{PARQUET_PATH}')")

regions   = ["All"] + con.execute("SELECT DISTINCT region FROM diet WHERE region IS NOT NULL ORDER BY region").df()["region"].tolist()
years     = con.execute("SELECT DISTINCT year FROM diet ORDER BY year").df()["year"].astype(int).tolist()
countries = ["All"] + con.execute("SELECT DISTINCT country FROM diet WHERE country IS NOT NULL ORDER BY country").df()["country"].tolist()
cost_cats = ["All"] + con.execute("SELECT DISTINCT cost_category FROM diet WHERE cost_category IS NOT NULL ORDER BY cost_category").df()["cost_category"].tolist()

country_to_region = dict(con.execute("SELECT DISTINCT country, region FROM diet WHERE country IS NOT NULL").fetchall())

df = con.execute("SELECT * FROM diet").df()

DEFAULT_YEAR_MIN = min(years)
DEFAULT_REGION   = "All"
DEFAULT_COUNTRY  = "All"

COST_RANGE = con.execute("""
    SELECT PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY cost_healthy_diet_ppp_usd),
           PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY cost_healthy_diet_ppp_usd)
    FROM diet
""").fetchone()

region_colors = {
    "Africa":        "#C0392B",
    "Asia":          "#D4860A",
    "Americas":      "#2471A3",
    "Europe":        "#1A3A6B",
    "Oceania":       "#E67E22",
    "North America": "#2471A3",
    "South America": "#17A589",
}

REGION_BOUNDS = {
    "Africa":        [-20,  55, -38,  38],
    "Asia":          [ 25, 145, -12,  55],
    "Europe":        [-28,  48,  34,  72],
    "Americas":      [-170, -30, -58,  72],
    "Oceania":       [ 110, 180, -50,   5],
    "North America": [-170, -52,  15,  75],
    "South America": [ -82, -34, -56,  13],
}

LABEL_MAX_COUNTRIES = 12

# Chart height
# 100vh - navbar(48) - kpi(70) - gaps/padding(60) - 2×card-header(72) = ~calc
CHART_H = "calc((100vh - 290px) / 2)"

qc = QueryChat(
    df, "diet_data",
    client=chatlas.ChatAnthropic(model=AI_AGENT),
)


# JS helper: attach Plotly click handler
def _click_js(div_id: str, shiny_input: str, extractor: str) -> str:
    return f"""
<script>
(function() {{
  function tryAttach() {{
    var el = document.getElementById('{div_id}');
    if (el && el.layout !== undefined) {{
      el.on('plotly_click', function(d) {{
        if (!d || !d.points || !d.points.length) return;
        var pt = d.points[0];
        var val = {extractor};
        if (val) Shiny.setInputValue('{shiny_input}', String(val), {{priority: 'event'}});
      }});
    }} else {{
      setTimeout(tryAttach, 150);
    }}
  }}
  tryAttach();
}})();
</script>"""


# CSS
CUSTOM_CSS = ui.tags.style("""
  *, *::before, *::after { box-sizing: border-box; }

  html, body { height: 100%; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 13px;
    color: #1a2332;
    background: #edf0f4;
    margin: 0;
  }

  .bslib-sidebar-layout { height: calc(100vh - 48px); }

  /* Navbar */
  .navbar {
    background: #ffffff !important;
    border-bottom: 2px solid #e2e8f0 !important;
    padding: 0 20px !important;
    min-height: 48px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .navbar .navbar-brand {
    font-size: 14px !important; font-weight: 700 !important;
    color: #1a2332 !important; padding: 12px 0 !important;
  }
  .navbar .nav-link {
    font-size: 13px !important; font-weight: 500 !important;
    color: #4a5568 !important; padding: 14px 16px !important;
    border-bottom: 3px solid transparent;
    transition: color 0.15s, border-color 0.15s;
  }
  .navbar .nav-link:hover { color: #2563eb !important; }
  .navbar .nav-link.active {
    color: #2563eb !important;
    border-bottom-color: #2563eb !important;
    font-weight: 600 !important;
  }

  /* Sidebar */
  .bslib-sidebar-layout > .sidebar {
    background: #ffffff;
    border-right: 1px solid #dde3ea;
    padding: 8px 12px;
    overflow-y: auto;
    min-height: 100%;
  }
  .bslib-sidebar-layout > .sidebar > .h4,
  .bslib-sidebar-layout > .sidebar > hr { display: none !important; }

  .sidebar .shiny-input-container {
    margin-top: 0 !important; margin-bottom: 0 !important;
    padding-top: 0 !important; padding-bottom: 0 !important;
  }
  .sidebar .control-label,
  .sidebar .shiny-input-container > label {
    font-size: 10px !important; font-weight: 700 !important;
    color: #64748b !important; text-transform: uppercase !important;
    letter-spacing: 0.7px !important; margin-bottom: 3px !important;
    margin-top: 0 !important; display: block !important; line-height: 1.2 !important;
  }
  .sidebar .shiny-input-radiogroup > .control-label {
    font-size: 10px !important; font-weight: 700 !important;
    color: #64748b !important; text-transform: uppercase !important;
    letter-spacing: 0.7px !important; margin-bottom: 3px !important; margin-top: 0 !important;
  }
  .sidebar .radio { margin: 0 !important; padding: 1px 0 !important; line-height: 1.35 !important; }
  .sidebar .radio label {
    font-size: 12px !important; font-weight: 400 !important;
    color: #1a2332 !important; text-transform: none !important;
    letter-spacing: 0 !important; cursor: pointer;
    padding-left: 4px; line-height: 1.35 !important;
  }
  .sidebar .shiny-options-group { margin: 0 !important; padding: 0 !important; }
  .sidebar .form-select {
    font-size: 13px !important; border: 1px solid #cbd5e0;
    border-radius: 6px; padding: 4px 10px;
    color: #1a2332; background-color: #fff; margin-top: 0 !important;
  }
  .sidebar .form-select:focus {
    border-color: #3b82f6; outline: none;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
  }
  .sidebar .js-irs-0, .sidebar .js-irs-1 { margin-bottom: 0 !important; }
  .sidebar .irs { margin-bottom: 0 !important; margin-top: 0 !important; }
  .sidebar .irs--shiny { margin: 0 !important; }
  .sidebar .irs--shiny .irs-grid-text { font-size: 10px; color: #718096; }
  .sidebar .irs--shiny .irs-single,
  .sidebar .irs--shiny .irs-from,
  .sidebar .irs--shiny .irs-to {
    font-size: 10px !important; background: #3b82f6 !important; border-radius: 4px;
  }
  .sidebar .irs--shiny .irs-bar { background: #3b82f6; border-color: #3b82f6; }
  .sidebar .irs--shiny .irs-handle { border-color: #3b82f6; }
  .sidebar-divider { height: 1px; background: #e8ecf0; margin: 4px 0; }

  /* Interaction tip box */
  .interact-tip {
    background: #f0f4ff;
    border: 1px solid #c7d7f9;
    border-radius: 6px;
    padding: 6px 9px;
    margin-top: 4px;
    font-size: 10px;
    color: #3b5bdb;
    line-height: 1.5;
  }
  .interact-tip strong { font-weight: 700; display: block; margin-bottom: 2px; }

  /* KPI cards */
  .kpi-row {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 8px; margin-bottom: 8px;
  }
  .kpi-card {
    background: #1e3a5f; border-radius: 8px; padding: 7px 12px;
    color: #ffffff; min-height: 54px; display: flex;
    flex-direction: column; justify-content: space-between;
  }
  .kpi-card:nth-child(2) { background: #1a5276; }
  .kpi-card:nth-child(3) { background: #1f618d; }
  .kpi-card:nth-child(4) { background: #2471a3; }
  .kpi-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.7px; color: rgba(255,255,255,0.75); margin: 0 0 2px 0;
  }
  .kpi-value { font-size: 24px; font-weight: 700; color: #ffffff; line-height: 1; margin: 0; }

  /* Cards */
  .card {
    border: 1px solid #dde3ea; border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    background: #ffffff; overflow: hidden;
  }
  .card-header {
    font-size: 12px; font-weight: 700; color: #2d3748;
    background: #ffffff; border-bottom: 1px solid #edf2f7;
    padding: 7px 14px; letter-spacing: 0.2px;
  }
  .card-body { padding: 2px; }

  /* Layout */
  .layout-columns { gap: 8px !important; }
  .bslib-sidebar-layout > .main > .layout-columns + .layout-columns {
    margin-top: 8px !important;
  }
  .kpi-row + .layout-columns { margin-top: 8px !important; }
  .bslib-sidebar-layout > .main {
    padding: 8px 10px 8px 10px; overflow-y: auto;
  }

  /* Clickable chart cursor */
  .js-plotly-plot { cursor: pointer; }

  /* Chat tab */
  .chat-page {
    height: calc(100vh - 52px); display: flex; flex-direction: column;
    padding: 12px; overflow: hidden; background: #edf0f4; box-sizing: border-box;
  }
  .chat-cols { display: flex; flex: 1; gap: 10px; overflow: hidden; min-height: 0; }
  .chat-left {
    flex: 0 0 38%; display: flex; flex-direction: column; overflow: hidden; min-height: 0;
  }
  .chat-left > .card { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-height: 0; }
  .chat-left > .card > .card-body {
    flex: 1; overflow: hidden; padding: 0 !important;
    display: flex; flex-direction: column; min-height: 0;
  }
  .chat-left .shiny-html-output,
  .chat-left [class*="querychat"],
  .chat-left [class*="chat"] {
    flex: 1; overflow-y: auto !important;
    display: flex !important; flex-direction: column !important; min-height: 0;
  }
  .chat-right {
    flex: 0 0 calc(62% - 10px); overflow-y: auto;
    display: flex; flex-direction: column; gap: 10px; min-height: 0;
  }

  /* Reset button */
  .btn-reset {
    width: 100%; font-size: 12px; font-weight: 600;
    padding: 6px 12px; border-radius: 6px;
    border: 1.5px solid #e53e3e; color: #e53e3e;
    background: transparent; cursor: pointer; transition: all 0.15s;
  }
  .btn-reset:hover { background: #e53e3e; color: #fff; }
""")


PLOTLY_CDN_SCRIPT = ui.tags.script(
    src="https://cdn.plot.ly/plotly-latest.min.js",
    charset="utf-8",
)


# UI
app_ui = ui.page_navbar(

    ui.nav_panel("Dashboard",
        CUSTOM_CSS,
        PLOTLY_CDN_SCRIPT,
        ui.page_sidebar(
            ui.sidebar(
                ui.tags.div(
                    ui.input_slider("year", "Year Range",
                        min=min(years), max=max(years),
                        value=[DEFAULT_YEAR_MIN, max(years)], sep="", step=1),
                    style="margin-bottom:0;",
                ),
                ui.tags.div(class_="sidebar-divider"),
                ui.tags.div(
                    ui.input_radio_buttons("cost_cat", "Cost Category",
                        choices=cost_cats, selected="All"),
                    style="margin-bottom:0;",
                ),
                ui.tags.div(class_="sidebar-divider"),
                ui.tags.div(
                    ui.input_select("region", "Region",
                        choices=regions, selected=DEFAULT_REGION),
                    style="margin-bottom:4px;",
                ),
                ui.tags.div(
                    ui.input_select("country", "Country",
                        choices=countries,
                        selected=DEFAULT_COUNTRY),
                    style="margin-bottom:0;",
                ),
                ui.tags.div(class_="sidebar-divider"),
                ui.tags.button("Reset Filters", id="reset", class_="btn-reset",
                    onclick="Shiny.setInputValue('reset', Math.random())"),
                
                ui.tags.div(
                    ui.tags.strong("Tip"),
                    "Click any country on the map, a bar, a trend line, or a box to instantly filter the dashboard.",
                    class_="interact-tip",
                ),
                ui.tags.p(
                    " · PPP-adjusted USD", ui.tags.br(),
                    " · Source: FAO/World Bank", ui.tags.br(),
                    style="font-size:11px; color:#94a3b8; margin-top:4px; line-height:1.4",
                ),
                width=210,
            ),

            
            ui.tags.div(
                ui.tags.div(
                    ui.tags.p("Countries", class_="kpi-label"),
                    ui.tags.div(ui.output_text("n_countries"), class_="kpi-value"),
                    class_="kpi-card",
                ),
                ui.tags.div(
                    ui.tags.p("Avg Cost / day", class_="kpi-label"),
                    ui.tags.div(ui.output_text("avg_cost"), class_="kpi-value"),
                    class_="kpi-card",
                ),
                ui.tags.div(
                    ui.tags.p("Min Cost / day", class_="kpi-label"),
                    ui.tags.div(ui.output_text("min_cost"), class_="kpi-value"),
                    class_="kpi-card",
                ),
                ui.tags.div(
                    ui.tags.p("Max Cost / day", class_="kpi-label"),
                    ui.tags.div(ui.output_text("max_cost"), class_="kpi-value"),
                    class_="kpi-card",
                ),
                class_="kpi-row",
            ),


            ui.layout_columns(
                ui.card(
                    ui.card_header("Diet Cost Map"),
                    ui.output_ui("plot_map"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Average Cost by Region"),
                    ui.output_ui("bar_chart"),
                    full_screen=True,
                ),
                col_widths=(7, 5),
            ),


            ui.layout_columns(
                ui.card(
                    ui.card_header("Top Countries by Cost Increase"),
                    ui.output_ui("plot_trend"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Cost Distribution by Region"),
                    ui.output_ui("plot_box"),
                    full_screen=True,
                ),
                col_widths=(7, 5),
                style="margin-top:8px;",
            ),
        )
    ),

    ui.nav_panel("AI Chatbot",
        ui.div(
            ui.div(
                ui.div(
                    ui.card(
                        ui.card_header("Ask about healthy diet costs around the world"),
                        qc.ui(),
                    ),
                    class_="chat-left",
                ),
                ui.div(
                    ui.card(
                        ui.card_header("Query Results"),
                        ui.output_data_frame("chat_table"),
                        ui.tags.div(
                            ui.download_button("download_chat", "Download filtered data as CSV",
                                class_="btn btn-sm btn-outline-secondary",
                                style="margin: 6px 0 4px 0; font-size:12px;"),
                            style="padding: 0 8px 6px 8px;",
                        ),
                    ),
                    ui.layout_columns(
                        ui.card(ui.card_header("Avg Cost by Region"), ui.output_ui("chat_bar")),
                        ui.card(ui.card_header("Cost Over Time"),     ui.output_ui("chat_trend")),
                        col_widths=(6, 6),
                    ),
                    class_="chat-right",
                ),
                class_="chat-cols",
            ),
            class_="chat-page",
        )
    ),

    title="Global Cost of a Healthy Diet",
    navbar_options=ui.navbar_options(bg="#ffffff", inverse=False),
)


# Server
def server(input, output, session):

    chat_result = qc.server()

    # Chat outputs
    @render.data_frame
    def chat_table():
        return render.DataGrid(chat_result.df(), height="175px")

    @render.download(filename="healthy_diet_filtered.csv")
    def download_chat():
        data = chat_result.df()
        if data is None or data.empty:
            yield ""
        else:
            yield data.to_csv(index=False)

    @output
    @render.ui
    def chat_bar():
        data = chat_result.df()
        if data is None or data.empty:
            return ui.tags.p("Ask a question above — charts will update automatically.",
                style="color:#94a3b8; font-size:12px; padding:18px 14px;")
        agg = (data.groupby("region")["cost_healthy_diet_ppp_usd"]
               .mean().reset_index()
               .sort_values("cost_healthy_diet_ppp_usd", ascending=False))
        fig = px.bar(agg, x="region", y="cost_healthy_diet_ppp_usd",
                     color="region", color_discrete_map=region_colors,
                     labels={"cost_healthy_diet_ppp_usd": "USD/day", "region": "Region"},
                     text_auto=".2f")
        fig.update_traces(textposition="outside", textfont_size=9, marker_line_width=0)
        _apply_chart_style(fig)
        fig.update_layout(xaxis=dict(tickangle=-30, tickfont_size=10, title=None),
                          yaxis=dict(title="USD/day", tickfont_size=10))
        return ui.HTML(fig.to_html(include_plotlyjs=False, default_height="28vh"))

    @output
    @render.ui
    def chat_trend():
        data = chat_result.df()
        if data is None or data.empty:
            return ui.div()
        agg = (data.groupby(["year", "region"])["cost_healthy_diet_ppp_usd"]
               .mean().reset_index())
        fig = px.line(agg, x="year", y="cost_healthy_diet_ppp_usd",
                      color="region", color_discrete_map=region_colors, markers=True,
                      labels={"cost_healthy_diet_ppp_usd": "USD/day",
                              "year": "Year", "region": "Region"})
        _apply_chart_style(fig)
        fig.update_layout(
            legend=dict(font_size=9, x=1.01, y=1, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickformat="d", dtick=1, tickfont_size=10, title="Year"),
            yaxis=dict(title="USD/day", tickfont_size=10),
        )
        return ui.HTML(fig.to_html(include_plotlyjs=False, default_height="28vh"))

    # Reset
    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_slider("year",            value=[DEFAULT_YEAR_MIN, max(years)])
        ui.update_select("region",          selected=DEFAULT_REGION)
        ui.update_select("country",         selected=DEFAULT_COUNTRY)
        ui.update_radio_buttons("cost_cat", selected="All")

    # Cascade countries
    @reactive.effect
    def _():
        sel = input.region()
        if sel == "All":
            fc = con.execute("SELECT DISTINCT country FROM diet WHERE country IS NOT NULL ORDER BY country").df()["country"].tolist()
        else:
            fc = con.execute(f"SELECT DISTINCT country FROM diet WHERE region = '{sel}' AND country IS NOT NULL ORDER BY country").df()["country"].tolist()
        cur = input.country()
        ui.update_select("country", choices=["All"] + fc,
                         selected=cur if cur in fc else "All")

    # Core filter
    @reactive.calc
    def filtered():
        yr = input.year()
        conditions = [f"year >= {int(yr[0])}", f"year <= {int(yr[1])}"]
        if input.region()   != "All": conditions.append(f"region        = '{input.region()}'")
        if input.country()  != "All": conditions.append(f"country       = '{input.country()}'")
        if input.cost_cat() != "All": conditions.append(f"cost_category = '{input.cost_cat()}'")
        return con.execute(f"SELECT * FROM diet WHERE {' AND '.join(conditions)}").df()

    # KPIs
    @render.text
    def n_countries(): return str(filtered()["country"].nunique())

    @render.text
    def avg_cost():
        v = filtered()["cost_healthy_diet_ppp_usd"]
        return f"${v.mean():.2f}" if not v.empty else "—"

    @render.text
    def min_cost():
        v = filtered()["cost_healthy_diet_ppp_usd"]
        return f"${v.min():.2f}" if not v.empty else "—"

    @render.text
    def max_cost():
        v = filtered()["cost_healthy_diet_ppp_usd"]
        return f"${v.max():.2f}" if not v.empty else "—"

    # Map
    @output
    @render.ui
    def plot_map():
        data = filtered()
        if data.empty:
            return _empty_msg("No data for current filters.")
        latest_year = int(data["year"].max())
        map_data    = data[data["year"] == latest_year].copy()
        sr, sc      = input.region(), input.country()
        n_shown     = map_data["country"].nunique()
        show_labels = (sc != "All") or (sr != "All" and n_shown <= LABEL_MAX_COUNTRIES)

        geo_base = dict(
            projection_type="mercator",
            showcoastlines=True,  coastlinecolor="#c8d0da", coastlinewidth=0.5,
            showland=True,        landcolor="#eef0f2",
            showocean=True,       oceancolor="#dce9f5",
            showlakes=False,      showframe=False,
            showcountries=True,   countrycolor="#c8d0da", countrywidth=0.4,
        )

        fig = px.choropleth(
            map_data,
            locations="Alpha-3 code", locationmode="ISO-3",
            color="cost_healthy_diet_ppp_usd",
            hover_name="country",
            custom_data=["region"],
            color_continuous_scale="rdylbu_r",
            range_color=COST_RANGE,
            labels={"cost_healthy_diet_ppp_usd": "USD/day"},
        )
        fig.update_traces(hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Region: %{customdata[0]}<br>"
            "Cost: $%{z:.2f} / day<extra></extra>"
        ))

        if sc != "All":
            fig.update_geos(**geo_base, fitbounds="locations", visible=True)
        elif sr != "All":
            b = REGION_BOUNDS.get(sr)
            if b:
                fig.update_geos(**geo_base,
                                lonaxis_range=[b[0], b[1]],
                                lataxis_range=[b[2], b[3]], visible=True)
            else:
                fig.update_geos(**geo_base, fitbounds="locations", visible=True)
        else:
            fig.update_geos(**geo_base,
                            lonaxis_range=[-168, 178],
                            lataxis_range=[-58, 82], visible=True)

        if show_labels:
            fig.add_trace(go.Scattergeo(
                locations=map_data["Alpha-3 code"],
                locationmode="ISO-3",
                text=map_data["country"],
                mode="text",
                textfont=dict(size=13 if sc != "All" else 9, color="#1e2a3a"),
                hoverinfo="skip", showlegend=False,
            ))

        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#ffffff",
            coloraxis_colorbar=dict(
                title=dict(text="USD/day", font=dict(size=10)),
                thickness=10, len=0.6, tickfont=dict(size=9), x=1.0,
            ),
            font_size=11,
        )

        html = fig.to_html(include_plotlyjs=False, default_height=CHART_H,
                           div_id="map_plot")
        html += _click_js("map_plot", "map_click",
                          "pt.hovertext || (pt.customdata && pt.customdata[0])")
        return ui.HTML(html)

    # Bar chart
    @output
    @render.ui
    def bar_chart():
        data = filtered()
        if data.empty:
            return _empty_msg("No data.")
        agg = (data.groupby("region")["cost_healthy_diet_ppp_usd"]
               .mean().reset_index()
               .sort_values("cost_healthy_diet_ppp_usd", ascending=False))
        fig = px.bar(agg, x="region", y="cost_healthy_diet_ppp_usd",
                     color="region", color_discrete_map=region_colors,
                     labels={"cost_healthy_diet_ppp_usd": "USD/day", "region": "Region"},
                     text_auto=".2f")
        fig.update_traces(textposition="outside", textfont_size=9, marker_line_width=0)
        _apply_chart_style(fig)
        fig.update_layout(
            showlegend=False,
            xaxis=dict(tickangle=-30, tickfont_size=10, title=None),
            yaxis=dict(title="USD/day", tickfont_size=10),
        )
        html = fig.to_html(include_plotlyjs=False, default_height=CHART_H,
                           div_id="bar_plot")
        html += _click_js("bar_plot", "bar_click", "pt.x")
        return ui.HTML(html)

    # Trend line
    @output
    @render.ui
    def plot_trend():
        data = filtered()
        if data.empty:
            return _empty_msg("No data.")
        min_yr, max_yr = int(data["year"].min()), int(data["year"].max())
        if min_yr == max_yr:
            return _empty_msg("Select a wider year range to see trends.")
        stats = (data[data["year"].isin([min_yr, max_yr])]
                 .pivot_table(index="country", columns="year",
                              values="cost_healthy_diet_ppp_usd").dropna())
        if stats.empty:
            return _empty_msg("Not enough data for trend comparison.")
        stats["increase"] = stats[max_yr] - stats[min_yr]
        top10 = stats.sort_values("increase", ascending=False).head(10).index.tolist()
        fig = px.line(
            data[data["country"].isin(top10)],
            x="year", y="cost_healthy_diet_ppp_usd",
            color="country", markers=True,
            labels={"cost_healthy_diet_ppp_usd": "Cost (USD/day)",
                    "year": "Year", "country": "Country"},
        )
        _apply_chart_style(fig)
        fig.update_layout(
            legend=dict(orientation="v", x=1.02, y=1,
                        font_size=9, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickformat="d", dtick=1, tickfont_size=10, title="Year"),
            yaxis=dict(title="USD/day", tickfont_size=10),
        )
        html = fig.to_html(include_plotlyjs=False, default_height=CHART_H,
                           div_id="trend_plot")
        html += _click_js("trend_plot", "trend_click", "pt.data.name")
        return ui.HTML(html)

    # Box plot
    @output
    @render.ui
    def plot_box():
        data = filtered()
        if data.empty:
            return _empty_msg("No data.")
        fig = px.box(
            data, x="year", y="cost_healthy_diet_ppp_usd",
            color="region", color_discrete_map=region_colors,
            points="outliers", hover_data={"country": True},
            labels={"cost_healthy_diet_ppp_usd": "Cost (USD/day)",
                    "year": "Year", "region": "Region"},
        )
        _apply_chart_style(fig)
        fig.update_layout(
            legend=dict(orientation="v", x=1.02, y=1,
                        font_size=9, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(type="category", tickfont_size=10, title="Year"),
            yaxis=dict(title="USD/day", tickfont_size=10),
        )
        html = fig.to_html(include_plotlyjs=False, default_height=CHART_H,
                           div_id="box_plot")
        html += _click_js("box_plot", "box_click", "pt.data.name")
        return ui.HTML(html)

    # Click-to-filter handlers

    @reactive.effect
    @reactive.event(input.map_click)
    def _():
        clicked = input.map_click()
        if not clicked:
            return
        if clicked not in countries[1:]:
            return
        region = country_to_region.get(clicked, "All")
        if region in regions[1:]:
            ui.update_select("region", selected=region)
        ui.update_select("country", selected=clicked)

    @reactive.effect
    @reactive.event(input.bar_click)
    def _():
        clicked = input.bar_click()
        if not clicked:
            return
        if clicked in regions[1:]:
            ui.update_select("region",  selected=clicked)
            ui.update_select("country", selected="All")

    @reactive.effect
    @reactive.event(input.trend_click)
    def _():
        clicked = input.trend_click()
        if not clicked:
            return
        if clicked not in countries[1:]:
            return
        region = country_to_region.get(clicked, "All")
        if region in regions[1:]:
            ui.update_select("region", selected=region)
        ui.update_select("country", selected=clicked)

    @reactive.effect
    @reactive.event(input.box_click)
    def _():
        clicked = input.box_click()
        if not clicked:
            return
        if clicked in regions[1:]:
            ui.update_select("region",  selected=clicked)
            ui.update_select("country", selected="All")


# Shared chart helpers
def _apply_chart_style(fig):
    fig.update_layout(
        template="plotly_white",
        margin={"t": 8, "b": 40, "l": 44, "r": 8},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(size=11, color="#2d3748"),
        xaxis=dict(gridcolor="#f0f4f8", linecolor="#e2e8f0", zerolinecolor="#e2e8f0"),
        yaxis=dict(gridcolor="#f0f4f8", linecolor="#e2e8f0", zerolinecolor="#e2e8f0"),
    )


def _empty_msg(msg):
    return ui.tags.p(
        msg,
        style="color:#94a3b8; font-size:12px; padding:32px 20px; text-align:center;"
    )


app = App(app_ui, server)
