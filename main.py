from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.uicomponents.layout import create_layout
from src.data.loader import load_trades,load_market_data

TRADE_DATA_PATH = "./data/trades.csv"
MARKET_DATA_PATH = "./data/marketdata2min.csv"

def main() -> None:
    trades_data = load_trades(TRADE_DATA_PATH )
    market_data = load_market_data(MARKET_DATA_PATH)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Tradeviewer2.0 dashboard"
    app.layout = create_layout(app,trades_data,market_data)
    app.run()


if __name__ == "__main__":
    main()