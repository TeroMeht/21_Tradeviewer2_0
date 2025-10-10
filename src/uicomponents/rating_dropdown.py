from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from . import ids
from src.data.loader import TradeSchema

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    """Render a Rating dropdown with Select All button."""
    all_ratings = data[TradeSchema.RATING].dropna().astype(int).tolist()  # convert to string for dropdown
    unique_ratings = sorted(set(all_ratings), key=int)

    @app.callback(
        Output(ids.RATING_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_RATINGS_BUTTON, "n_clicks"),
        prevent_initial_call=True,  # avoid triggering on page load
    )
    def select_all_ratings(_: int) -> list[str]:
        return unique_ratings

    return html.Div(
        children=[
            html.H6("Rating"),
            dcc.Dropdown(
                id=ids.RATING_DROPDOWN,
                options=[{"label": r, "value": r} for r in unique_ratings],
                value=[4,5],  # initially nothing selected
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_RATINGS_BUTTON,
                n_clicks=0,
            ),
        ]
    )