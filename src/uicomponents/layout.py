from dash import Dash, html
from . import bar_chart, nation_dropdown


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),

            # Dropdown container
            html.Div(
                className="dropdown-container",
                children=[
                    nation_dropdown.render(app),
                ],
            ),

            # Single call renders all 9 bar charts in a 3x3 grid
            bar_chart.render(app),
        ],
    )
