from shiny import App, ui, render, reactive
import plotly.express as px
from download_data import get_data

df = get_data()
regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
years = sorted(df["year"].unique().tolist())
countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
cost_cats = ["All"] + [c for c in df["cost_category"].dropna().unique().tolist()]

# UI
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider("year", "Year", min(years), max(years), value=max(years), sep=""),
        ui.input_select("region", "Region", choices=regions),
        ui.input_select("country", "Country", choices=countries),
        ui.input_select("cost_cat", "Cost Category", choices=cost_cats),
        title="Filters"
    ),
    ui.h2("Global Cost of Healthy Diet Dashboard"),
    
    # Row 1: 4 stat boxes
    ui.layout_columns(
        ui.card(ui.card_header("Countries"), ui.output_text("n_countries")),
        ui.card(ui.card_header("Avg Cost (USD/day)"), ui.output_text("avg_cost")),
        ui.card(ui.card_header("Min Cost"), ui.output_text("min_cost")),
        ui.card(ui.card_header("Max Cost"), ui.output_text("max_cost")),
        col_widths=(3, 3, 3, 3)
    ),
    
    # Row 2: 2 boxes (1 working chart + 1 placeholder)
    ui.layout_columns(
        ui.card(
            ui.card_header("Average Cost by Region (Bar Chart)"),
            ui.output_ui("bar_chart"),
            full_screen=True
        ),
        ui.card(ui.card_header("World Map"), "Coming soon..."),
        col_widths=(6, 6)
    ),
    
    # Row 3: 2 placeholder boxes
    ui.layout_columns(
        ui.card(ui.card_header("Cost Over Time (Line Chart)"), "Coming soon..."),
        ui.card(ui.card_header("Top 10 Countries"), "Coming soon..."),
        col_widths=(6, 6)
    )
)

# Server
def server(input, output, session):
    @reactive.calc
    def filtered():
        data = df[df["year"] == input.year()]
        if input.region() != "All":
            data = data[data["region"] == input.region()]
        if input.country() != "All":
            data = data[data["country"] == input.country()]
        if input.cost_cat() != "All":
            data = data[data["cost_category"] == input.cost_cat()]
        return data

    @render.text
    def n_countries():
        return str(filtered()["country"].nunique())

    @render.text
    def avg_cost():
        return f"${filtered()['cost_healthy_diet_ppp_usd'].mean():.2f}"

    @render.text
    def min_cost():
        return f"${filtered()['cost_healthy_diet_ppp_usd'].min():.2f}"

    @render.text
    def max_cost():
        return f"${filtered()['cost_healthy_diet_ppp_usd'].max():.2f}"

    @render.ui
    def bar_chart():
        data = filtered()
        agg = data.groupby("region")["cost_healthy_diet_ppp_usd"].mean().reset_index()
        fig = px.bar(
            agg, x="region", y="cost_healthy_diet_ppp_usd", color="region",
            labels={"cost_healthy_diet_ppp_usd": "Avg Cost (USD)", "region": "Region"}
        )
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        return ui.HTML(fig.to_html(include_plotlyjs="cdn", full_html=False))

app = App(app_ui, server)
