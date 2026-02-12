from shiny import App, ui, render
import plotly.express as px
from download_data import get_data

df = get_data()

app_ui = ui.page_fluid(

    ui.h2("Healthy Diet Dashboard"),

    ui.input_select(
        "region",
        "Select Region",
        choices=sorted(df["region"].unique())
    ),

    ui.output_ui("plot")
)


def server(input, output, session):

    @output
    @render.ui
    def plot():
        data = df[df["region"] == input.region()]

        avg = (
            data.groupby("country")["cost_healthy_diet_ppp_usd"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            avg,
            x="country",
            y="cost_healthy_diet_ppp_usd"
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))


app = App(app_ui, server)
