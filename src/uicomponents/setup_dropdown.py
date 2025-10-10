from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from . import ids
from src.data.loader import TradeSchema

def render(app: Dash,data: pd.DataFrame) -> html.Div:
    all_setups: list[str] = data[TradeSchema.SETUP].tolist()
    unique_setups = sorted(set(all_setups),key=str)

    @app.callback(
        Output(ids.SETUP_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_TRADES_BUTTON, "n_clicks"),
        prevent_initial_call=True,  # <-- important!
    )
    def select_all_nations(_: int) -> list[str]:
        return unique_setups

    return html.Div(
        children=[
            html.H6("Setup"),
            dcc.Dropdown(
                id=ids.SETUP_DROPDOWN,
                options=[{"label": setup, "value": setup} for setup in unique_setups],
                value=[],
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_TRADES_BUTTON,
                n_clicks=0,
            ),
        ]
    )