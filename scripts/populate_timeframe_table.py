import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import connect_to_db

# Create database connection
engine = connect_to_db()

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

print("Script Successfully Executed!")