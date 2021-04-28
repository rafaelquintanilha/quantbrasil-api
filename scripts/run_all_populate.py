import os
from dotenv import load_dotenv

load_dotenv()
path_to_metatrader_files = os.environ.get("PATH_TO_METATRADER_FILES")

os.system("python scripts/populate/ibov.py")
os.system("python scripts/populate/bdr.py")
os.system(f"python scripts/populate/prices.py {path_to_metatrader_files}")

print("ALL POPULATE SCRIPTS SUCCESSFULLY EXECUTED!")
