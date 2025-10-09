import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids

MEDAL_DATA = px.data.medals_long()


def render(app: Dash, num_charts=9) -> html.Div:
    """
    Returns a 3x3 grid of bar charts.
    Each chart has a unique ID for callbacks.
    """

    # Generate unique IDs for each chart
    chart_ids = [f"{ids.BAR_CHART}-{i}" for i in range(1, num_charts + 1)]

    # Create the grid of empty Graphs initially
    chart_components = [
        dcc.Graph(id=chart_id, figure=px.bar(MEDAL_DATA, x="medal", y="count", color="nation"))
        for chart_id in chart_ids
    ]

    # Wrap them in a grid container
    container = html.Div(chart_components, className="chart-grid")

    # Optional: single callback updating all charts at once
    @app.callback(
        [Output(chart_id, "figure") for chart_id in chart_ids],
        [Input(ids.NATION_DROPDOWN, "value")],
    )
    def update_charts(nations: list[str]):
        if not nations:
            # Return empty figures if nothing selected
            return [px.bar(title="No data selected") for _ in chart_ids]

        filtered_data = MEDAL_DATA.query("nation in @nations")

        # For demonstration, create the same figure in all charts
        figs = [
            px.bar(filtered_data, x="medal", y="count", color="nation", text="nation")
            for _ in chart_ids
        ]
        return figs

    return container
