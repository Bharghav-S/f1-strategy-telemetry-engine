
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("STARTING F1 VISUALISATION ENGINE")

# Create output directory if it doesn't exist
Path("outputs").mkdir(exist_ok=True)

# Load raw race data
df = pd.read_csv("data/raw/british_gp_2024_laps.csv")

# Convert lap time to seconds
df["LapTime_seconds"] = pd.to_timedelta(
    df["LapTime"], errors="coerce"
).dt.total_seconds()

# Convert tyre age to numeric
df["TyreLife"] = pd.to_numeric(
    df["TyreLife"], errors="coerce"
)

# Remove incomplete records
df = df.dropna(
    subset=["Driver", "LapNumber", "LapTime_seconds"]
).copy()

# Remove pit-in and pit-out laps
df = df[
    df["PitInTime"].isna() &
    df["PitOutTime"].isna()
].copy()

# Remove invalid lap times
df = df[df["LapTime_seconds"] > 0].copy()

# ==========================================
# GRAPH 1: DRIVER LAP-TIME PROGRESSION
# ==========================================

print("\nGenerating driver lap-time graph...")

drivers = ["HAM", "VER", "NOR", "PIA"]

plt.figure(figsize=(13, 6))

for driver in drivers:
    driver_data = df[df["Driver"] == driver].sort_values("LapNumber")

    plt.plot(
        driver_data["LapNumber"],
        driver_data["LapTime_seconds"],
        marker=".",
        markersize=4,
        linewidth=1.2,
        label=driver
    )

plt.title("2024 British GP - Driver Lap Time Progression")
plt.xlabel("Lap Number")
plt.ylabel("Lap Time (seconds)")
plt.legend(title="Driver")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/driver_lap_progression.png", dpi=200)
plt.close()

# ==========================================
# GRAPH 2: TYRE AGE VS LAP TIME
# ==========================================

print("Generating tyre degradation graph...")

dry_tyres = df[
    df["Compound"].isin(["SOFT", "MEDIUM", "HARD"])
].dropna(subset=["TyreLife"]).copy()

plt.figure(figsize=(11, 6))

for compound in ["SOFT", "MEDIUM", "HARD"]:
    tyre_data = dry_tyres[
        dry_tyres["Compound"] == compound
    ]

    # Plot individual lap observations
    plt.scatter(
        tyre_data["TyreLife"],
        tyre_data["LapTime_seconds"],
        alpha=0.25,
        s=18,
        label=f"{compound} observations"
    )

    # Calculate average lap time at each tyre age
    age_average = (
        tyre_data.groupby("TyreLife")["LapTime_seconds"]
        .mean()
        .sort_index()
    )

    plt.plot(
        age_average.index,
        age_average.values,
        marker="o",
        linewidth=2,
        label=f"{compound} average"
    )

plt.title("Tyre Age vs Lap Time - British GP 2024")
plt.xlabel("Tyre Age (laps)")
plt.ylabel("Lap Time (seconds)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/tyre_degradation.png", dpi=200)
plt.close()

# ==========================================
# GRAPH 3: TYRE COMPOUND COMPARISON
# ==========================================

print("Generating compound comparison graph...")

compound_data = dry_tyres[
    dry_tyres["LapTime_seconds"].notna()
]

plt.figure(figsize=(10, 6))

compounds = ["SOFT", "MEDIUM", "HARD"]

box_data = [
    compound_data[
        compound_data["Compound"] == compound
    ]["LapTime_seconds"].values
    for compound in compounds
]

plt.boxplot(box_data, tick_labels=compounds)

plt.title("Lap Time Distribution by Tyre Compound")
plt.xlabel("Tyre Compound")
plt.ylabel("Lap Time (seconds)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/compound_comparison.png", dpi=200)
plt.close()

# ==========================================
# GRAPH 4: DRIVER STINT PERFORMANCE
# ==========================================

print("Generating stint comparison graph...")

stint_data = (
    df.groupby(["Driver", "Stint", "Compound"])
    ["LapTime_seconds"]
    .mean()
    .reset_index()
)

selected_drivers = ["HAM", "VER", "NOR", "PIA"]

stint_data = stint_data[
    stint_data["Driver"].isin(selected_drivers)
].copy()

stint_data["StintLabel"] = (
    stint_data["Driver"] + " - S" +
    stint_data["Stint"].astype(int).astype(str) +
    " (" + stint_data["Compound"] + ")"
)

plt.figure(figsize=(13, 6))

plt.bar(
    stint_data["StintLabel"],
    stint_data["LapTime_seconds"]
)

plt.title("Average Lap Time by Driver and Stint")
plt.xlabel("Driver and Stint")
plt.ylabel("Average Lap Time (seconds)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/stint_comparison.png", dpi=200)
plt.close()

# ==========================================
# COMPLETION
# ==========================================

print("\n====================================")
print("VISUALISATION ENGINE COMPLETED!")
print("====================================")

print("4 graphs saved in outputs/")

print("1. driver_lap_progression.png")
print("2. tyre_degradation.png")
print("3. compound_comparison.png")
print("4. stint_comparison.png")
