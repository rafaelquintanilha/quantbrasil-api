import pandas as pd
import glob
from dotenv import load_dotenv
import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from db import connect_to_db

# USAGE: $ python populate_price_table.py <PATH_TO_FILES>
args = sys.argv[1:]
path = args[0]

# Create database connection
engine = connect_to_db()

# Looping through all the timeframes directories
timeframe_dirs = os.listdir(f"{path}")

for timeframe in timeframe_dirs:
    # Removes '.DS_Store' in case the script is running in a mac computer
    if timeframe == ".DS_Store":
        timeframe_dirs.remove(".DS_Store")

    for timeframe in timeframe_dirs:
        os.chdir(f"{path}/{timeframe}")
        assets_files = glob.glob("*.csv")
        symbol_list = [s[:-4] for s in assets_files]

        # Looping through all the symbols and adding it to the price table
        for symbol in symbol_list:
            df = pd.read_csv(f"{path}/{timeframe}/{symbol}.csv")[
                ["time", "open", "high", "low", "close", "real_volume"]
            ]
            df.rename(
                columns={"time": "datetime", "real_volume": "volume"}, inplace=True
            )

            # Importing asset_id and timeframe_id from tables in PostgreSQL
            asset_id = pd.read_sql(
                f"SELECT id FROM asset WHERE symbol = '{symbol}';", engine
            )

            # Creating the columns
            df["asset_id"] = int(asset_id["id"])
            df["timeframe_id"] = f"{timeframe}"

            # Writing the SQL query to populate price table
            insert_init = """
                INSERT INTO price (datetime, open, high, low, close, volume, asset_id, timeframe_id)
                VALUES
            """

            values = ",".join(
                [
                    "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        row["datetime"],
                        row["open"],
                        row["high"],
                        row["low"],
                        row["close"],
                        row["volume"],
                        row["asset_id"],
                        row["timeframe_id"],
                    )
                    for datetime, row in df.iterrows()
                ]
            )

            insert_end = """
                ON CONFLICT (datetime, asset_id, timeframe_id) DO UPDATE 
                SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low, 
                close = EXCLUDED.close,
                volume = EXCLUDED.volume;
            """

            query = insert_init + values + insert_end
            engine.execute(query)

print("Script Successfully Executed!")
