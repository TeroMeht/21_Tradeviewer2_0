from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.uicomponents.layout import create_layout
from src.data.loader import load_trades,load_market_data
from src.common.ReadConfigsIn import read_database_config


database_config = read_database_config(filename="database.ini", section="postgresql")

def main() -> None:
    trades_data = load_trades(database_config, "trades")
    market_data = load_market_data(database_config, "marketdataintrad")
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Tradeviewer2.0 dashboard"
    app.layout = create_layout(app,trades_data,market_data)
    app.run()


if __name__ == "__main__":
    main()