
import pandas as pd
from pathlib import Path

# Locate the processed CSV
PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "british_gp_2024_laps_processed.csv"
)

# Load processed data
df = pd.read_csv(FILE)

print("=== F1 DATA VALIDATION ===")

# Test 1: Check for duplicate driver-lap combinations
duplicates = df.duplicated(
    subset=["Driver", "LapNumber"]
).sum()

print(f"Duplicate driver-lap records: {duplicates}")

# Test 2: Check for impossible lap times
invalid_laps = (
    df["LapTime_seconds"].isna()
    | (df["LapTime_seconds"] <= 0)
).sum()

print(f"Invalid lap times: {invalid_laps}")

# Test 3: Check for invalid tyre ages
invalid_tyre_ages = (
    df["TyreLife"].isna()
    | (df["TyreLife"] < 0)
).sum()

print(f"Invalid tyre ages: {invalid_tyre_ages}")

# Test 4: Check for pit-in/pit-out overlap
overlapping_pit_flags = (
    df["IsPitInLap"] & df["IsPitOutLap"]
).sum()

print(f"Laps flagged both pit-in and pit-out: {overlapping_pit_flags}")

# Test 5: Count analysis-ready laps
analysis_laps = df["IsAnalysisLap"].sum()

print(f"Analysis-ready laps: {analysis_laps}")

# Test 6: Inspect lap-time range
print(f"Fastest recorded lap: {df['LapTime_seconds'].min():.3f}s")
print(f"Slowest recorded lap: {df['LapTime_seconds'].max():.3f}s")

# Overall result
print("\n=== VALIDATION RESULT ===")

if duplicates == 0 and invalid_laps == 0 and invalid_tyre_ages == 0:
    print("PASS: Basic data integrity checks passed.")
else:
    print("WARNING: Some data integrity checks need investigation.")
