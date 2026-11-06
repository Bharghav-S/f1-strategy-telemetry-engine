
import pandas as pd
from pathlib import Path

# -----------------------------------
# 1. Define file locations
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "british_gp_2024_laps.csv"

PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"

PROCESSED_FILE = PROCESSED_FOLDER / "british_gp_2024_laps_processed.csv"


# -----------------------------------
# 2. Load the raw data
# -----------------------------------

print("Loading raw F1 data...")

df = pd.read_csv(RAW_FILE)

print(f"Original dataset shape: {df.shape}")


# -----------------------------------
# 3. Standardise text columns
# -----------------------------------

df["Driver"] = df["Driver"].astype("string").str.strip().str.upper()

df["Compound"] = df["Compound"].astype("string").str.strip().str.upper()


# -----------------------------------
# 4. Convert columns into useful types
# -----------------------------------

df["LapTime_seconds"] = (
    pd.to_timedelta(df["LapTime"], errors="coerce")
    .dt.total_seconds()
)

df["TyreLife"] = pd.to_numeric(df["TyreLife"], errors="coerce")

df["LapNumber"] = pd.to_numeric(df["LapNumber"], errors="coerce")

df["Position"] = pd.to_numeric(df["Position"], errors="coerce")


# -----------------------------------
# 5. Create useful pit-stop flags
# -----------------------------------

df["IsPitInLap"] = df["PitInTime"].notna()

df["IsPitOutLap"] = df["PitOutTime"].notna()


# -----------------------------------
# 6. Create an analysis-ready lap flag
# -----------------------------------

df["IsAnalysisLap"] = (
    df["LapTime_seconds"].notna()
    & (df["LapTime_seconds"] > 0)
    & (~df["IsPitInLap"])
    & (~df["IsPitOutLap"])
)


# -----------------------------------
# 7. Check data quality
# -----------------------------------

print("\n--- DATA QUALITY REPORT ---")

print(f"Total rows: {len(df)}")

print(f"Unique drivers: {df['Driver'].nunique()}")

print(f"Missing lap times: {df['LapTime_seconds'].isna().sum()}")

print(f"Missing tyre ages: {df['TyreLife'].isna().sum()}")

print(f"Pit-in laps: {df['IsPitInLap'].sum()}")

print(f"Pit-out laps: {df['IsPitOutLap'].sum()}")

print(f"Analysis-ready laps: {df['IsAnalysisLap'].sum()}")


# -----------------------------------
# 8. Save processed data
# -----------------------------------

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

df.to_csv(PROCESSED_FILE, index=False)

print("\nProcessed data saved successfully!")

print(f"Saved to: {PROCESSED_FILE}")

print(f"Final dataset shape: {df.shape}")
