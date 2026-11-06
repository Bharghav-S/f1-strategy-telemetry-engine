
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# 1. FILE LOCATIONS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "british_gp_2024_laps_processed.csv"
)

OUTPUT_FOLDER = PROJECT_ROOT / "outputs"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. LOAD DATA
# ==========================================

print("Loading processed F1 data...")

df = pd.read_csv(DATA_FILE)

print(f"Loaded {len(df)} lap records.")


# ==========================================
# 3. FILTER FOR SLICK TYRE LAPS
# ==========================================

slick_compounds = ["SOFT", "MEDIUM", "HARD"]

df = df[
    (df["IsAnalysisLap"] == True)
    & (df["Compound"].isin(slick_compounds))
].copy()

print(f"Slick analysis laps: {len(df)}")


# ==========================================
# 4. GROUP DATA INTO TYRE STINTS
# ==========================================

# Each driver, stint and compound combination
# is treated as a separate tyre run.

stint_results = []

for (driver, stint, compound), group in df.groupby(
    ["Driver", "Stint", "Compound"]
):

    group = group.dropna(
        subset=["TyreLife", "LapTime_seconds"]
    ).copy()

    # Require enough observations to fit a trend
    if len(group) < 6:
        continue

    if group["TyreLife"].nunique() < 4:
        continue

    x = group["TyreLife"].to_numpy()
    y = group["LapTime_seconds"].to_numpy()

    # Fit a straight line:
    # lap time = slope * tyre age + intercept

    slope, intercept = np.polyfit(x, y, 1)

    predicted = slope * x + intercept

    # Calculate R-squared to measure how well
    # the straight line fits the observed laps.

    ss_res = np.sum((y - predicted) ** 2)
    ss_total = np.sum((y - np.mean(y)) ** 2)

    r_squared = (
        1 - ss_res / ss_total
        if ss_total > 0
        else np.nan
    )

    stint_results.append({
        "Driver": driver,
        "Stint": stint,
        "Compound": compound,
        "Laps_analysed": len(group),
        "Tyre_age_start": x.min(),
        "Tyre_age_end": x.max(),
        "Degradation_sec_per_lap": slope,
        "Intercept": intercept,
        "R_squared": r_squared
    })


# ==========================================
# 5. CREATE RESULTS TABLE
# ==========================================

results = pd.DataFrame(stint_results)

if results.empty:
    raise ValueError(
        "No stints had enough usable laps for modelling."
    )

results = results.sort_values(
    "Degradation_sec_per_lap",
    ascending=False
)

print("\n==========================================")
print("TYRE DEGRADATION MODEL RESULTS")
print("==========================================")

print(
    results[
        [
            "Driver",
            "Stint",
            "Compound",
            "Laps_analysed",
            "Degradation_sec_per_lap",
            "R_squared"
        ]
    ].round(3).to_string(index=False)
)


# ==========================================
# 6. COMPOUND-LEVEL SUMMARY
# ==========================================

compound_summary = (
    results.groupby("Compound")
    ["Degradation_sec_per_lap"]
    .agg(["mean", "median", "count"])
    .reset_index()
)

print("\n==========================================")
print("COMPOUND DEGRADATION SUMMARY")
print("==========================================")

print(compound_summary.round(3).to_string(index=False))


# ==========================================
# 7. EXPORT RESULTS
# ==========================================

results_file = OUTPUT_FOLDER / "tyre_degradation_model.csv"

summary_file = OUTPUT_FOLDER / "tyre_degradation_summary.csv"

results.to_csv(results_file, index=False)

compound_summary.to_csv(summary_file, index=False)

print("\nSaved model results:")
print(results_file)

print(summary_file)


# ==========================================
# 8. VISUALISE DEGRADATION
# ==========================================

plt.figure(figsize=(11, 6))

for compound in slick_compounds:

    compound_data = results[
        results["Compound"] == compound
    ]

    if compound_data.empty:
        continue

    plt.scatter(
        compound_data["Tyre_age_start"],
        compound_data["Degradation_sec_per_lap"],
        label=compound,
        alpha=0.75
    )

plt.axhline(0, linestyle="--", linewidth=1)

plt.title("Estimated Tyre Degradation by Compound")
plt.xlabel("Starting tyre age (laps)")
plt.ylabel("Estimated lap-time change (seconds per tyre lap)")
plt.legend(title="Compound")
plt.grid(alpha=0.3)

plt.tight_layout()

plot_file = OUTPUT_FOLDER / "tyre_degradation_model.png"

plt.savefig(plot_file, dpi=300)

plt.close()

print(f"\nGraph saved to: {plot_file}")

print("\nTYRE DEGRADATION MODELLING COMPLETED!")
