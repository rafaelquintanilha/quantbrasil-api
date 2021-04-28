import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import connect_to_db

# Create database connection
engine = connect_to_db()

# Dropping all tables in cascade to be able to create them again
drop_query = """DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
"""
engine.execute(drop_query)

# Creating asset table
asset_query = """CREATE TABLE asset (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR (15) NOT NULL UNIQUE,
    name VARCHAR (100) NOT NULL,
    type VARCHAR (10),
    yf_symbol VARCHAR (15) NOT NULL
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

# Creating timeframe table 
timeframe_query = """CREATE TABLE timeframe (
    id VARCHAR (5) PRIMARY KEY, 
    description VARCHAR (15) NOT NULL
);"""
engine.execute(timeframe_query)

# Creating price table 
price_query = """CREATE TABLE price (
    id BIGSERIAL,
    asset_id INTEGER NOT NULL REFERENCES asset(id),
    timeframe_id VARCHAR (5) NOT NULL REFERENCES timeframe(id),
    datetime TIMESTAMP,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume INTEGER,
    PRIMARY KEY (id, datetime),
    UNIQUE (asset_id, timeframe_id, datetime)
);"""
engine.execute(price_query)

print("Script Successfully Executed!")
