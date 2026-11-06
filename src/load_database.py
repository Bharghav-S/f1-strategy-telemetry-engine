
import pandas as pd
import sqlite3
from pathlib import Path

# Locate project files
PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "british_gp_2024_laps_processed.csv"
)

DB_FOLDER = PROJECT_ROOT / "data" / "database"
DB_FILE = DB_FOLDER / "f1_strategy.db"

# Create database folder if necessary
DB_FOLDER.mkdir(parents=True, exist_ok=True)

# Load processed data
print("Loading processed F1 data...")
df = pd.read_csv(CSV_FILE)

# Connect to SQLite database
connection = sqlite3.connect(DB_FILE)

# Write dataframe into a SQL table
df.to_sql(
    "race_laps",
    connection,
    if_exists="replace",
    index=False
)

print("Data successfully loaded into SQLite!")

# Check how many records were inserted
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM race_laps")

row_count = cursor.fetchone()[0]

print(f"Records in database: {row_count}")

connection.close()

print(f"Database saved at: {DB_FILE}")
