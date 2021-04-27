import pandas as pd
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import connect_to_db

# Create database connection
engine = connect_to_db()

# Looping through all the timeframes directories
path = "/Users/andressamonteiro/QuantBrasil/Data/"
timeframe_dirs = os.listdir(path)[1:] #[1:] removes the first file which is '.DS_S' from mac

for timeframe in timeframe_dirs:
    asset_dirs = os.listdir(path + timeframe + "/")[1:] #[1:] removes the first file which is '.DS_S' from mac
    symbol_list = [s[:-4] for s in asset_dirs]
    
    # Looping through all the symbols and adding it to the price table 
    for symbol in symbol_list:
        df = pd.read_csv(f'/Users/andressamonteiro/QuantBrasil/Data/{timeframe}/{symbol}.csv')[["time","open", "high", "low", "close", "real_volume"]]
        df.rename(columns={"time": "datetime", "real_volume": "volume"}, inplace=True)
        
        # Importing asset_id and timeframe_id from tables in PostgreSQL
        asset_id = pd.read_sql(
            f"SELECT id FROM asset WHERE symbol = '{symbol}';",
            engine
        )
        timeframe_id = pd.read_sql(
            f"SELECT id FROM timeframe WHERE name = '{timeframe}';",
            engine
        )

        # Creating the columns
        df["asset_id"] = int(asset_id["id"])
        df["timeframe_id"] = int(timeframe_id["id"])

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
                    row["timeframe_id"]
                    )
                for datetime, row in df.iterrows()
            ]
        )

        insert_end = """
            ON CONFLICT (datetime, asset_id, timeframe_id) DO UPDATE 
            SET
            datetime = EXCLUDED.datetime, 
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low, 
            close = EXCLUDED.close,
            volume = EXCLUDED.volume,
            asset_id = EXCLUDED.asset_id,
            timeframe_id = EXCLUDED.timeframe_id;
        """

        query = insert_init + values + insert_end
        engine.execute(query)

print("Script Successfully Executed!")
