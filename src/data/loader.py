import pandas as pd

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

def load_trades(path: str) -> pd.DataFrame:
    """Load and clean the trades dataset, replacing NULLs and extracting year/month."""
    df = pd.read_csv(
        path,
        dtype={
            TradeSchema.TRADE_ID: int,
            TradeSchema.SYMBOL: str,
            TradeSchema.SETUP: str,
            TradeSchema.RATING: "Int64",  # nullable integer
        },
        parse_dates=[TradeSchema.DATE],
    )

    # Ensure DATE column is datetime
    df[TradeSchema.DATE] = pd.to_datetime(
        df[TradeSchema.DATE], format="%Y-%m-%d", errors="coerce"
    )

    # Fill NULL ratings with 0
    df[TradeSchema.RATING] = df[TradeSchema.RATING].fillna(0)

    # Extract year and month as strings
    df[TradeSchema.YEAR] = df[TradeSchema.DATE].dt.year.astype(str)
    df[TradeSchema.MONTH] = df[TradeSchema.DATE].dt.month.astype(str)

    return df

def load_market_data(path: str) -> pd.DataFrame:
    """Load and clean the market data dataset."""
    df = pd.read_csv(
        path,
        dtype={
            MarketDataSchema.SYMBOL: str,
            MarketDataSchema.DATE: str,
            MarketDataSchema.TIME: str,
            MarketDataSchema.OPEN: float,
            MarketDataSchema.HIGH: float,
            MarketDataSchema.LOW: float,
            MarketDataSchema.CLOSE: float,
            MarketDataSchema.VOLUME: int,
            MarketDataSchema.VWAP: float,
            MarketDataSchema.EMA9: float,
            MarketDataSchema.TRADE_ID: int,
            MarketDataSchema.RELATR: float,
        },
        parse_dates=[MarketDataSchema.DATE],
    )

    # Ensure DATE is datetime
    df[MarketDataSchema.DATE] = pd.to_datetime(
        df[MarketDataSchema.DATE], format="%Y-%m-%d", errors="coerce"
    )

    return df