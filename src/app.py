from shiny import App, ui, render, reactive
import plotly.express as px
from download_data import get_data

df = get_data()

app_ui = ui.page_fluid(

    ui.h2("Healthy Diet Dashboard"),

    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "region",
                "Select Region",
                choices=sorted(df["region"].unique())
            ),
            ui.input_slider(
                "year",
                "Select Year Range",
                df["year"].min(), df["year"].max(),
                [df["year"].min(), df["year"].max()]
            ),

        ),
        ui.card(
            ui.output_ui("plot_map")
        ),
        ui.card(
            ui.layout_columns(
               ui.output_ui("plot_trend"),
               ui.output_ui("plot_bar")
            )
        ),
        ui.card(
            ui.output_ui("plot_box")
        )
    )
)

def server(input, output, session):

    @reactive.calc
    def avg_data():
        years = input.year()
        region_data = df[df["region"] == input.region()]
        year_and_region_data = region_data[(region_data["year"]>= years[0]) & (region_data["year"]<= years[1])]

        plot_data = (
            year_and_region_data.groupby("country")["cost_healthy_diet_ppp_usd"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        return plot_data

    @reactive.calc
    def cumulative_data():
        years = input.year()
        region_data = df[df["region"] == input.region()]
        plot_data = region_data[(region_data["year"]>= years[0]) & (region_data["year"]<= years[1])]

        return plot_data

    @output
    @render.ui
    def plot_map():
        data = avg_data()
        
        if data.empty:
            return ui.markdown("No data for the selected period.")

        fig = px.choropleth(
            data,
            locations="country",
            # color="cost_healthy_diet_ppp_usd", 
            hover_name="country", 
            # color_continuous_scale="Viridis",
            projection="natural earth",
            title="Healthy Diet Cost Index by Country"
        )

        fig.update_layout(margin={"r":0, "t":40, "l":0, "b":0})

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    @output
    @render.ui
    def plot_trend():
        data = cumulative_data()

        fig = px.line(
            data,
            x="year",
            y="cost_healthy_diet_ppp_usd",
            color="country"
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @output
    @render.ui
    def plot_bar():
        data = avg_data()

        fig = px.bar(
            data,
            x="country",
            y="cost_healthy_diet_ppp_usd"
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    @output
    @render.ui
    def plot_box():
        data = cumulative_data()

        fig = px.box(
            data,
            x="year",
            y="cost_healthy_diet_ppp_usd",
            color="region"
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))


app = App(app_ui, server)
