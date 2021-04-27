import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import connect_to_db

# Create database connection
engine = connect_to_db()

# Inserting the timeframes' name 
insert_query = """
INSERT INTO timeframe (name) 
VALUES ('M5'),
('M15'), 
('M30'), 
('H1'),
('H2'), 
('H4'), 
('D1'),
('W1'), 
('MN')
ON CONFLICT (name) 
DO UPDATE SET name = EXCLUDED.name;
"""
engine.execute(insert_query)

print("Script Successfully Executed!")