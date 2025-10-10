from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
from . import ids
from plotly.subplots import make_subplots


def create_plot_component(df_chunk: pd.DataFrame, plot_id: str) -> dcc.Graph:
    """Candlestick chart with VWAP, EMA9, Volume, and Relatr in light mode."""
    if df_chunk.empty:
        fig = go.Figure()
        fig.update_layout(title="No data for this trade", xaxis_visible=False, yaxis_visible=False)
        return fig

    # Clean column names
    df_chunk.columns = df_chunk.columns.str.strip()
    x = df_chunk["Time"]

    # Use 3-row subplot: Candlestick, Volume, Relatr
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.6, 0.2, 0.2]
    )

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=x,
        open=df_chunk["Open"],
        high=df_chunk["High"],
        low=df_chunk["Low"],
        close=df_chunk["Close"],
        name="OHLC"
    ), row=1, col=1)

    # VWAP
    if "VWAP" in df_chunk.columns:
        fig.add_trace(go.Scatter(
            x=x,
            y=df_chunk["VWAP"],
            line=dict(color="red", width=1),
            name="VWAP"
        ), row=1, col=1)

    # EMA9
    if "EMA9" in df_chunk.columns:
        fig.add_trace(go.Scatter(
            x=x,
            y=df_chunk["EMA9"],
            line=dict(color="blue", width=1),
            name="EMA9"
        ), row=1, col=1)

    # Volume
    if "Volume" in df_chunk.columns:
        fig.add_trace(go.Bar(
            x=x,
            y=df_chunk["Volume"],
            name="Volume",
            marker_color="blue",
        ), row=2, col=1)

    # Relatr
    if "Relatr" in df_chunk.columns:
        fig.add_trace(go.Scatter(
            x=x,
            y=df_chunk["Relatr"],
            mode="lines",
            line=dict(color="green", width=2),
            name="Relatr"
        ), row=3, col=1)

        # Optional horizontal reference lines
        for y_val in [0, 0.4, -0.4]:
            fig.add_shape(
                type="line",
                x0=x.min(),
                x1=x.max(),
                y0=y_val,
                y1=y_val,
                line=dict(color="black", width=1, dash="dash"),
                xref="x3",
                yref="y3"
            )

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False  # <-- remove legend completely
    )

    return fig

def register_callbacks(app: Dash, trades: pd.DataFrame, marketdata: pd.DataFrame):
    """
    Dynamically generate finance charts based on filtered trades.
    Each chart has a header with Symbol, Date, Rating.
    """

    @app.callback(
        Output("dynamic-chart-grid", "children"),
        Input(ids.YEAR_DROPDOWN, "value"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input(ids.SETUP_DROPDOWN, "value"),
        Input(ids.RATING_DROPDOWN, "value"),
        
    )
    def update_charts(selected_years, selected_months, selected_setups, selected_ratings):
        filtered_trades = trades.copy()

        # Filter by selected years
        if selected_years:
            filtered_trades = filtered_trades[filtered_trades["Year"].isin(selected_years)]

        # Filter by selected months
        if selected_months:
            filtered_trades = filtered_trades[filtered_trades["Month"].isin(selected_months)]

        # Filter by selected setups
        if selected_setups:
            filtered_trades = filtered_trades[filtered_trades["Setup"].isin(selected_setups)]

        # Filter by selected ratings, including NaN
        if selected_ratings:
            filtered_trades = filtered_trades[
                filtered_trades["Rating"].isin(selected_ratings) | filtered_trades["Rating"].isna()
            ]

        # If nothing matches, return empty list
        if filtered_trades.empty:
            return []
        chart_components = []

        for _, trade_row in filtered_trades.iterrows():
            trade_id = trade_row["TradeId"]

            # Get only the marketdata rows for this TradeId
            df_trade_data = marketdata[marketdata["TradeId"] == trade_id].copy()
            df_trade_data.columns = df_trade_data.columns.str.strip()  # clean column names

            plot_id = f"{ids.DATA_TABLE}-{trade_id}-chart"

            chart_components.append(
                html.Div(
                    children=[
                        html.H6(f"{trade_row['Symbol']} | {trade_row['Date']} | Rating: {trade_row['Rating']} | Setup: {trade_row['Setup']}"),
                        dcc.Graph(
                            id=plot_id,
                            figure=create_plot_component(df_trade_data, plot_id),  # <- Figure only
                            style={"height": "400px", "width": "100%"}
                        )
                    ],
                    style={"border": "1px solid #eee", "padding": "0.5rem", "borderRadius": "6px"}
                )
            )

        return chart_components




