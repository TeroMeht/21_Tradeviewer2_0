import psycopg2
import pandas as pd



def get_connection_and_cursor(database_config):
    """Create and return a database connection and cursor."""
    conn = psycopg2.connect(**database_config)
    if not conn:
        raise Exception("Failed to connect to database.")
    cur = conn.cursor()
    return conn, cur




def fetch_all_marketdata(database_config: dict, table_name: str) -> pd.DataFrame:
    """Fetch all rows from the given market-data table using get_connection_and_cursor."""

    try:
        conn, cur = get_connection_and_cursor(database_config)

        query = f'SELECT * FROM "{table_name}";'
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=colnames)

        if df.empty:
            print(f"No data found in table '{table_name}'.")
            return df

        return df

    except Exception as e:
        print(f"Error fetching all data from {table_name}: {e}")
        return pd.DataFrame()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def fetch_all_trades(database_config: dict, table_name: str = "Trades") -> pd.DataFrame:
    """Fetch all rows from the trades table using get_connection_and_cursor."""
    try:
        conn, cur = get_connection_and_cursor(database_config)

        query = f'SELECT * FROM "{table_name}" ORDER BY "Date";'
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=colnames)

        if df.empty:
            print(f"No data found in table '{table_name}'.")
            return df

        return df

    except Exception as e:
        print(f"Error fetching trades data from {table_name}: {e}")
        return pd.DataFrame()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()