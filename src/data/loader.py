import pandas as pd
from src.data.db_functions import fetch_all_marketdata,fetch_all_trades

# Schema for the trades file
class TradeSchema:
    TRADE_ID = "TradeId"
    SYMBOL = "Symbol"
    DATE = "Date"
    SETUP = "Setup"
    RATING = "Rating"
    YEAR = "Year"
    MONTH = "Month"

# Schema for the market data file
class MarketDataSchema:
    SYMBOL = "Symbol"
    DATE = "Date"
    TIME = "Time"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    VOLUME = "Volume"
    VWAP = "VWAP"
    EMA9 = "EMA9"
    TRADE_ID = "TradeId"
    RELATR = "Relatr"

def load_trades(database_config: dict, table_name: str) -> pd.DataFrame:
    df = fetch_all_trades(database_config, table_name)
    if df.empty:
        return df

    # Ensure DATE column is datetime
    if TradeSchema.DATE in df.columns:
        df[TradeSchema.DATE] = pd.to_datetime(df[TradeSchema.DATE], errors="coerce")
        df = df.dropna(subset=[TradeSchema.DATE])


    # Extract year and month
    df[TradeSchema.YEAR] = df[TradeSchema.DATE].dt.year.astype(str)
    df[TradeSchema.MONTH] = df[TradeSchema.DATE].dt.month.astype(str)

    return df

def load_market_data(database_config: dict, table_name: str) -> pd.DataFrame:
    """Load and clean the market data dataset from the database."""
    df = fetch_all_marketdata(database_config, table_name)

    if df.empty:
        print(f"No data found in table '{table_name}'.")
        return df

    # Ensure DATE is datetime
    if MarketDataSchema.DATE in df.columns:
        df[MarketDataSchema.DATE] = pd.to_datetime(
            df[MarketDataSchema.DATE], format="%Y-%m-%d", errors="coerce"
        )

    # Convert numeric columns
    numeric_cols = [
        MarketDataSchema.OPEN,
        MarketDataSchema.HIGH,
        MarketDataSchema.LOW,
        MarketDataSchema.CLOSE,
        MarketDataSchema.VOLUME,
        MarketDataSchema.VWAP,
        MarketDataSchema.EMA9,
        MarketDataSchema.RELATR,
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df