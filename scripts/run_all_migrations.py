import os

##### ToDo: Figure out how to handle each script synchronously
# import glob
# migrations = glob.glob("scripts/migrations/*.py")
# for migration in migrations:
#   os.system(f"python {migration}")

os.system("python scripts/migrations/20210101_createdb.py")
os.system("python scripts/migrations/20210428_timeframe_and_price.py")

print("ALL MIGRATIONS SUCCESSFULLY EXECUTED!")
