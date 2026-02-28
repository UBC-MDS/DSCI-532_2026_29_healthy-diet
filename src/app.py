from shiny import App, ui, render, reactive, req
import plotly.express as px
import pandas as pd
from scripts.download_data import download_dataset
from scripts.clean_data import clean_dataset

download_dataset()
clean_dataset()

df = pd.read_csv("data/processed/cleaned_price_of_healthy_diet.csv")
regions = ["All"] + sorted(df["region"].dropna().unique().tolist()) #
years = sorted(df["year"].unique().tolist())
countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
cost_cats = ["All"] + [c for c in df["cost_category"].dropna().unique().tolist()]

region_colors = {
    "Africa": "#B71226",
    "Asia": "#FEE090",
    "Americas": "#B0DBEA",
    "Europe": "#34419A",
    "Oceania": "#FB9D59"
}

# UI
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider("year", "Year", min(years), max(years), [min(years), max(years)], sep=""),
        ui.input_select("region", "Region", choices=regions),
        ui.input_select("country", "Country", choices=countries),
        ui.input_radio_buttons("cost_cat", "Cost Category", choices=cost_cats),
        ui.hr(),
        ui.input_action_button("reset", "Clear Filters", class_="btn-outline-danger w-100"),
        title="Filters"
    ),
    ui.h1("Global Cost of a Healthy Diet"),
    ui.h5("Measured in Purchase Power Parity, normalized to $USD"),
    
    # Row 1: 4 stat boxes
    ui.layout_columns(
        ui.value_box( 
            "Countries", 
            ui.output_text("n_countries"), 
            theme = "bg-gradient-indigo-purple" 
        ),
        ui.value_box( 
            "Avg Cost (USD/day)", 
            ui.output_text("avg_cost"), 
            theme = "bg-gradient-indigo-purple" 
        ),
        ui.value_box( 
            "Min Cost", 
            ui.output_text("min_cost"), 
            theme = "bg-gradient-indigo-purple" 
        ),
        ui.value_box( 
            "Max Cost", 
            ui.output_text("max_cost"), 
            theme = "bg-gradient-indigo-purple" 
        ),
        col_widths=(3, 3, 3, 3)
    ),
    
    # Row 2: World Map
    ui.card(
        # ui.card_header("World Map"), 
        ui.output_ui("plot_map")
    ),

    # Row 3: 2 boxes (1 Line + 1 Bar)
    ui.layout_columns(
        ui.card(
            # ui.card_header("Top 10 Highest Increases Over Time"),
            ui.output_ui("plot_trend")
        ),
        ui.card(
            # ui.card_header("Average Cost by Region (Bar Chart)"),
            ui.output_ui("bar_chart"),
        )
    ),
    
    # Row 4: Box plot
    ui.card(
        # ui.card_header("Top 10 Countries"), 
        ui.output_ui("plot_box")
    )
)

# Server
def server(input, output, session):
    @reactive.effect
    @reactive.event(input.reset)
    def _():
        # Reset Slider
        ui.update_slider("year", value=[min(years), max(years)])
        
        # Reset Selects
        ui.update_select("region", selected="All")
        ui.update_select("country", selected="All")
        
        # Reset Radio Buttons
        ui.update_radio_buttons("cost_cat", selected="All")
    
    @reactive.effect
    def _():
        selected_region = input.region()
        
        # Filter original dataframe for countries in the selected region
        if selected_region == "All":
            filtered_countries = sorted(df["country"].dropna().unique().tolist())
        else:
            filtered_countries = sorted(
                df[df["region"] == selected_region]["country"].dropna().unique().tolist()
            )
        
        # Update the input_select choices
        ui.update_select(
            "country",
            choices=["All"] + filtered_countries,
            selected=input.country() if input.country() in filtered_countries else "All"
        )
    
    @reactive.calc
    def filtered():
        # req(input.year(), input.region(), input.country(), input.cost_cat())
        
        year_range = input.year()
        data = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
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

    @output
    @render.ui
    def plot_map():
        data = filtered()
        latest_year = max(data["year"])
        data = data[ data["year"] == latest_year ]

        fig = px.choropleth(
            data,
            locations=data["Alpha-3 code"],
            color="cost_healthy_diet_ppp_usd", 
            hover_name="country", 
            color_continuous_scale="rdylbu_r",
            projection="natural earth",
            title="Healthy Diet Cost Index by Country"
        )

        fig.update_layout(margin={"r":0, "t":40, "l":0, "b":0})
        fig.update_layout(template="plotly_white")
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @output
    @render.ui
    def plot_trend():
        data = filtered()

        # 1. Calculate the cost increase per country
        min_year = data["year"].min()
        max_year = data["year"].max()
        
        # Pivot to get start and end values side-by-side
        stats = data[data["year"].isin([min_year, max_year])].pivot_table(
            index="country", 
            columns="year", 
            values="cost_healthy_diet_ppp_usd"
        ).dropna()

        if stats.empty:
            return ui.markdown("No countries have data for both the start and end years.")

        # 2. Calculate the difference (Max Year - Min Year)
        stats["increase"] = stats[max_year] - stats[min_year]
        
        # 3. Identify the top 5 countries
        top_10_countries = stats.sort_values("increase", ascending=False).head(10).index.tolist()
        
        # 4. Filter original data for just these 5 countries
        plot_df = data[data["country"].isin(top_10_countries)]

        fig = px.line(
            plot_df,
            x="year",
            y="cost_healthy_diet_ppp_usd",
            color="country",
            color_discrete_map=region_colors,
            labels={"cost_healthy_diet_ppp_usd": "Avg Cost (USD)", "year": "Year", "country": "Country"},
            title="Top 10 Highest Increases Over Time"
        )
        fig.update_layout(template="plotly_white")
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @output
    @render.ui
    def plot_box():
        data = filtered()

        fig = px.box(
            data,
            x="year",
            y="cost_healthy_diet_ppp_usd",
            color="region",
            color_discrete_map=region_colors,
            points="all",
            hover_data={
                "country": True,
            },
            labels={"cost_healthy_diet_ppp_usd": "Avg Cost (USD)", "year": "Year", "region": "Region"},
            title="Change in Cost by Region Over Time"
        )
        fig.update_layout(template="plotly_white")
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @output
    @render.ui
    def bar_chart():
        data = filtered()

        agg = data.groupby("region")["cost_healthy_diet_ppp_usd"].mean().reset_index()
        fig = px.bar(
            agg, 
            x="region", 
            y="cost_healthy_diet_ppp_usd", 
            color="region",
            color_discrete_map=region_colors,
            labels={"cost_healthy_diet_ppp_usd": "Avg Cost (USD)", "region": "Region"},
            title="Highest Average Cost by Region (Latest Year)"
        )
        fig.update_layout(showlegend=False)
        fig.update_layout(template="plotly_white")
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

app = App(app_ui, server)
