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
        ui.input_slider("year", "Year", min(years), max(years), [min(years), max(years)], sep=""),
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
    
    # Row 2: World Map
    ui.card(
        ui.card_header("World Map"), 
        ui.output_ui("plot_map")
    ),

    # Row 3: 2 boxes (1 Line + 1 Bar)
    ui.layout_columns(
        ui.card(
            ui.card_header("Cost Over Time (Line Chart)"),
            ui.output_ui("plot_trend")
        ),
        ui.card(
            ui.card_header("Average Cost by Region (Bar Chart)"),
            ui.output_ui("bar_chart"),
        )
    ),
    
    # Row 4: Box plot
    ui.card(
        ui.card_header("Top 10 Countries"), 
        ui.output_ui("plot_box")
    )
)

# Server
def server(input, output, session):
    @reactive.calc
    def filtered():
        year_range = input.year()
        data = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
        if input.region() != "All":
            data = data[data["region"] == input.region()]
        if input.country() != "All":
            data = data[data["country"] == input.country()]
        if input.cost_cat() != "All":
            data = data[data["cost_category"] == input.cost_cat()]
        return data
    
    # @reactive.calc
    # def avg_data():
    #     year_range = input.year()
    #     data = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
    #     if input.region() != "All":
    #         data = data[data["region"] == input.region()]
    #     if input.country() != "All":
    #         data = data[data["country"] == input.country()]
    #     if input.cost_cat() != "All":
    #         data = data[data["cost_category"] == input.cost_cat()]

    #     plot_data = (
    #         data.groupby("country")["cost_healthy_diet_ppp_usd"]
    #         .mean()
    #         .sort_values(ascending=False)
    #         .head(10)
    #         .reset_index()
    #     )
    #     return plot_data

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

    @output
    @render.ui
    def plot_map():
        data = filtered()
        agg = data.groupby("region")["cost_healthy_diet_ppp_usd"].mean().reset_index()
        
        if agg.empty:
            return ui.markdown("No data for the selected period.")

        fig = px.choropleth(
            agg,
            locations="region",
            # color="cost_healthy_diet_ppp_usd", 
            hover_name="region", 
            # color_continuous_scale="Viridis",
            projection="natural earth",
            title="Healthy Diet Cost Index by Country"
        )

        fig.update_layout(margin={"r":0, "t":40, "l":0, "b":0})

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @output
    @render.ui
    def plot_trend():
        data = filtered()

        fig = px.line(
            data,
            x="year",
            y="cost_healthy_diet_ppp_usd",
            color="country"
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @output
    @render.ui
    def plot_box():
        data = filtered()

        fig = px.box(
            data,
            x="year",
            y="cost_healthy_diet_ppp_usd",
            color="region"
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @output
    @render.ui
    def bar_chart():
        data = filtered()
        agg = data.groupby("region")["cost_healthy_diet_ppp_usd"].mean().reset_index()
        fig = px.bar(
        agg, x="region", y="cost_healthy_diet_ppp_usd", color="region",
            labels={"cost_healthy_diet_ppp_usd": "Avg Cost (USD)", "region": "Region"}
        )
        # fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

app = App(app_ui, server)
