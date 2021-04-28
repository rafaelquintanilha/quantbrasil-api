import os 
from dotenv import load_dotenv

load_dotenv()
path_to_metatrader_files = os.environ.get("PATH_TO_METATRADER_FILES")

os.system('python scripts/create_db.py')
os.system('python scripts/ibov_portfolio.py')
os.system('python scripts/bdr_portfolio.py')
os.system('python scripts/populate_timeframe_table.py')
os.system(f'python scripts/populate_price_table.py {path_to_metatrader_files}')

print("ALL SCRIPTS SUCCESSFULLY EXECUTED!")