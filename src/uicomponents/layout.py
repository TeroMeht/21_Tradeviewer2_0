from dash import Dash, html
from . import marketdata_chart, setup_dropdown, table_grid,rating_dropdown,year_dropdown,month_dropdown
import pandas as pd


def create_layout(app: Dash, trades: pd.DataFrame, marketdata: pd.DataFrame) -> html.Div:
    table_container = html.Div(id="dynamic-table-grid", className="chart-grid")
    chart_container = html.Div(id="dynamic-chart-grid", className="chart-grid")

    table_grid.register_callbacks(app, trades)
    marketdata_chart.register_callbacks(app, trades, marketdata)

    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[year_dropdown.render(app,trades),
                          month_dropdown.render(app,trades),
                          setup_dropdown.render(app, trades),
                          rating_dropdown.render(app, trades)],
            ),
            html.Div(
                className="paired-grid",
                children=[
                   # table_container,
                    chart_container,
                ],
            ),
        ],
    )