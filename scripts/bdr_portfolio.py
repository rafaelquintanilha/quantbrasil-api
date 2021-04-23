import pandas as pd
import requests
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import connect_to_db

# Creating the BDR portfolio in the portfolio table
engine = connect_to_db()

insert_portfolio_query = """
INSERT INTO portfolio (name) 
VALUES ('BDR') 
ON CONFLICT (name) 
DO UPDATE SET name = EXCLUDED.name;
"""
# Executing the query
engine.execute(insert_portfolio_query)

# Parsing html BDR table into a dataframe
url = "https://investnews.com.br/financas/veja-a-lista-completa-dos-bdrs-disponiveis-para-pessoas-fisicas-na-b3/"

r = requests.get(url)

df = pd.read_html(r.text, header=0)[0]

# POPULATING ASSET TABLE
asset = df.loc[:, ["EMPRESA", "CÓDIGO"]].copy()
asset.columns = ["name", "symbol"]
asset["yf_symbol"] = asset["symbol"] + ".SA"

# Writing the SQL query to populate asset table
insert_initial = """
    INSERT INTO asset (name, symbol, yf_symbol)
    VALUES
"""

values = ",".join(
    [
        "('{}', '{}', '{}')".format(row["name"], row["symbol"], row["yf_symbol"])
        for symbol, row in asset.iterrows()
    ]
)

insert_end = """
    ON CONFLICT (symbol) DO UPDATE 
    SET
    name = EXCLUDED.name,
    symbol = EXCLUDED.symbol,
    yf_symbol = EXCLUDED.yf_symbol;
"""

query = insert_initial + values + insert_end
engine = connect_to_db()
engine.execute(query)

# POPULATING ASSET_PORTFOLIO TABLE

# Importing asset and portfolio tables from PostgreSQL
symbol_tuple = tuple(asset["symbol"])
asset_portfolio = pd.read_sql(
    f"SELECT id FROM asset WHERE symbol IN {symbol_tuple};", engine
)
asset_portfolio.columns = ["asset_id"]

ibov_portfolio_id = pd.read_sql("SELECT id FROM portfolio WHERE name='BDR';", engine)
asset_portfolio["portfolio_id"] = int(ibov_portfolio_id["id"])

# Writing the SQL query to populate asset_portfolio table
insert_init = """
    INSERT INTO asset_portfolio (asset_id, portfolio_id)
    VALUES
"""

values = ",".join(
    [
        "('{}', '{}')".format(int(row["asset_id"]), int(row["portfolio_id"]))
        for asset_id, row in asset_portfolio.iterrows()
    ]
)

insert_end = """
    ON CONFLICT (asset_id, portfolio_id) DO UPDATE 
    SET
    asset_id = EXCLUDED.asset_id,
    portfolio_id = EXCLUDED.portfolio_id
"""
query = insert_init + values + insert_end
engine.execute(query)

print("Script Successfully Executed!")
