
import pandas as pd
from pathlib import Path

# =====================================
# 1. PROJECT FILES
# =====================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_FILE = PROJECT_ROOT / "outputs" / "tyre_degradation_model.csv"


# =====================================
# 2. LOAD DEGRADATION RESULTS
# =====================================

df = pd.read_csv(MODEL_FILE)

print("LOADING TYRE DEGRADATION DATA")
print(f"Modelled stints: {len(df)}")


# =====================================
# 3. BUILD A SIMPLE STRATEGY SIMULATOR
# =====================================

def simulate_strategy(strategy, pit_loss=22):

    total_time = 0
    total_laps = 0

    for stint in strategy:

        compound = stint["compound"]
        laps = stint["laps"]

        # Use the median observed slope for the compound
        compound_data = df[
            df["Compound"] == compound
        ]

        if compound_data.empty:
            raise ValueError(
                f"No model data for {compound}"
            )

        degradation = compound_data[
            "Degradation_sec_per_lap"
        ].median()

        # Simple illustrative baseline lap times.
        # These are placeholders, not calibrated race pace.
        base_lap_times = {
            "SOFT": 90.5,
            "MEDIUM": 91.0,
            "HARD": 91.5
        }

        base_time = base_lap_times[compound]

        # Tyre age starts at 1 for each new stint
        stint_time = sum(
            base_time + degradation * (age - 1)
            for age in range(1, laps + 1)
        )

        total_time += stint_time
        total_laps += laps

    # Add pit-stop time loss
    total_time += (len(strategy) - 1) * pit_loss

    return total_time, total_laps


# =====================================
# 4. DEFINE STRATEGIES
# =====================================

strategies = {

    "One-stop": [
        {"compound": "MEDIUM", "laps": 25},
        {"compound": "SOFT", "laps": 27}
    ],

    "Two-stop": [
        {"compound": "MEDIUM", "laps": 18},
        {"compound": "MEDIUM", "laps": 17},
        {"compound": "SOFT", "laps": 17}
    ]
}


# =====================================
# 5. COMPARE STRATEGIES
# =====================================

print("\nRACE STRATEGY COMPARISON")
print("=" * 45)

results = []

for name, strategy in strategies.items():

    total_time, total_laps = simulate_strategy(strategy)

    results.append({
        "Strategy": name,
        "Total_laps": total_laps,
        "Projected_time_seconds": total_time
    })

results_df = pd.DataFrame(results)

print(results_df.to_string(index=False))

best_strategy = results_df.loc[
    results_df["Projected_time_seconds"].idxmin()
]

print("\nFASTEST MODELLED STRATEGY:")
print(best_strategy["Strategy"])

print(
    f"Projected time: "
    f"{best_strategy['Projected_time_seconds']:.2f} seconds"
)

print("\nSTRATEGY SIMULATION COMPLETED!")
