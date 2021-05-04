import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from db import connect_to_db

# Create database connection
engine = connect_to_db()

# Creating timeframe table
timeframe_query = """CREATE TABLE timeframe (
    id VARCHAR (5) PRIMARY KEY, 
    description VARCHAR (15) NOT NULL
);"""
engine.execute(timeframe_query)

# Inserting the timeframes' name
insert_query = """
INSERT INTO timeframe (id, description) 
VALUES ('M5', '5 minutes'),
('M10', '10 minutes'),
('M15', '15 minutes'), 
('M30', '30 minutes'), 
('H1', '1 hour'),
('H2', '1 hours'), 
('H4', '4 hour'), 
('D1', 'Daily'),
('W1', 'Weekly'), 
('MN', 'Monthly');
"""
engine.execute(insert_query)

# Creating price table
price_query = """CREATE TABLE price (
    id BIGSERIAL,
    asset_id INTEGER NOT NULL REFERENCES asset(id),
    timeframe_id VARCHAR (5) NOT NULL REFERENCES timeframe(id),
    datetime TIMESTAMP NOT NULL,
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
