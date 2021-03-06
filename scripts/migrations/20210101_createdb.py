import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from db import connect_to_db

# Create database connection
engine = connect_to_db()

# Creating asset table
asset_query = """CREATE TABLE asset (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR (15) NOT NULL UNIQUE,
    name VARCHAR (100) NULL,
    type VARCHAR (10) NULL,
    yf_symbol VARCHAR (15) NULL
);"""
engine.execute(asset_query)

# Creating portfolio table
portfolio_query = """CREATE TABLE portfolio (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (100) NOT NULL UNIQUE
);"""
engine.execute(portfolio_query)

# Creating asset_portfolio table
asset_portfolio_query = """CREATE TABLE asset_portfolio ( 
    id BIGSERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES asset(id),
    portfolio_id INTEGER NOT NULL REFERENCES portfolio(id),
    weight DOUBLE PRECISION,
    UNIQUE (asset_id, portfolio_id)
    );"""
engine.execute(asset_portfolio_query)

print("Script Successfully Executed!")
