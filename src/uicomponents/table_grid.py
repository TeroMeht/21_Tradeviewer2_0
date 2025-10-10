from dash import dcc, html, dash_table, Output, Input, Dash
from dash.dependencies import Input, Output
import pandas as pd
from . import ids

def create_table_component(trade_row: dict, table_id: str):
    """Create a single table component for one trade row."""
    columns = [{"name": k, "id": k} for k in trade_row.keys()]
    data = [trade_row]
    return dash_table.DataTable(
        id=table_id,
        columns=columns,
        data=data,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center"},
        style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
    )

def register_callbacks(app: Dash, data: pd.DataFrame):
    """Populate dynamic number of tables based on filtered trades."""

    @app.callback(
        Output("dynamic-table-grid", "children"),
        Input(ids.SETUP_DROPDOWN, "value"),
    )
    def update_tables(selected_setups):
        if not selected_setups:
            return []

        # Filter trades by setup
        filtered = data.query("Setup in @selected_setups")


        table_components = []
        for i, row in filtered.iterrows():
            table_id = f"{ids.DATA_TABLE}-{i}"
            table_components.append(create_table_component(row.to_dict(), table_id))

        return table_components