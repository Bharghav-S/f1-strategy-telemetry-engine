
import pandas as pd
import numpy as np

print("======================================")
print(" F1 PERFORMANCE DATA INVESTIGATION")
print(" 2024 BRITISH GRAND PRIX")
print("======================================")

# 1. Load dataset
df = pd.read_csv("data/raw/british_gp_2024_laps.csv")

# 2. Convert lap times into seconds
df["LapTime_seconds"] = pd.to_timedelta(
    df["LapTime"], errors="coerce"
).dt.total_seconds()

df["TyreLife"] = pd.to_numeric(
    df["TyreLife"], errors="coerce"
)

# 3. Remove inaccurate or incomplete observations
df = df.dropna(
    subset=["Driver", "LapTime_seconds", "TyreLife", "Compound"]
).copy()

if "IsAccurate" in df.columns:
    accurate = df["IsAccurate"].astype(str).str.lower()
    df = df[accurate == "true"].copy()

# Keep physically valid lap times
df = df[df["LapTime_seconds"] > 0].copy()

# ======================================
# ANALYSIS 1: DRIVER PERFORMANCE
# ======================================

print("\n1. DRIVER PERFORMANCE")

driver_stats = (
    df.groupby("Driver")
    .agg(
        average_lap=("LapTime_seconds", "mean"),
        median_lap=("LapTime_seconds", "median"),
        fastest_lap=("LapTime_seconds", "min"),
        laps_completed=("LapNumber", "count")
    )
    .round(3)
    .sort_values("average_lap")
)

print(driver_stats)

# ======================================
# ANALYSIS 2: TYRE COMPOUND ANALYSIS
# ======================================

print("\n2. TYRE COMPOUND PERFORMANCE")

compound_stats = (
    df.groupby("Compound")
    .agg(
        average_lap=("LapTime_seconds", "mean"),
        median_lap=("LapTime_seconds", "median"),
        average_tyre_age=("TyreLife", "mean"),
        total_laps=("LapNumber", "count")
    )
    .round(3)
    .sort_values("average_lap")
)

print(compound_stats)

# ======================================
# ANALYSIS 3: TYRE AGE VS LAP TIME
# ======================================

print("\n3. TYRE DEGRADATION INVESTIGATION")

tyre_age_stats = (
    df.groupby(["Compound", "TyreLife"])
    .agg(
        average_lap=("LapTime_seconds", "mean"),
        observations=("LapNumber", "count")
    )
    .reset_index()
)

print(tyre_age_stats.head(25).to_string(index=False))

# ======================================
# ANALYSIS 4: DRIVER STINT ANALYSIS
# ======================================

print("\n4. DRIVER STINT PERFORMANCE")

stint_stats = (
    df.groupby(["Driver", "Stint", "Compound"])
    .agg(
        stint_average=("LapTime_seconds", "mean"),
        stint_fastest=("LapTime_seconds", "min"),
        average_tyre_age=("TyreLife", "mean"),
        laps=("LapNumber", "count")
    )
    .round(3)
    .reset_index()
)

print(stint_stats.to_string(index=False))

# ======================================
# ANALYSIS 5: SLOW LAP INVESTIGATION
# ======================================

print("\n5. SLOW LAP INVESTIGATION")

driver_baseline = df.groupby("Driver")[
    "LapTime_seconds"
].transform("median")

df["LapDelta"] = (
    df["LapTime_seconds"] - driver_baseline
)

slow_laps = (
    df[df["LapDelta"] > 3]
    .sort_values("LapDelta", ascending=False)
)

print(
    slow_laps[
        ["Driver", "LapNumber", "LapTime_seconds",
         "LapDelta", "Compound", "TyreLife"]
    ].head(20).to_string(index=False)
)

# ======================================
# SAVE ANALYSIS OUTPUTS
# ======================================

driver_stats.to_csv("outputs/driver_performance.csv")
compound_stats.to_csv("outputs/compound_performance.csv")
tyre_age_stats.to_csv("outputs/tyre_degradation.csv", index=False)
stint_stats.to_csv("outputs/stint_analysis.csv", index=False)
slow_laps.to_csv("outputs/slow_laps.csv", index=False)

print("\n======================================")
print("DEEP DIVE COMPLETED SUCCESSFULLY")
print("5 analytical datasets exported.")
print("======================================")
