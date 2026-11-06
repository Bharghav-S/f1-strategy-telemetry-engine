import fastf1
import pandas as pd
# ==========================================
# F1 STRATEGY AND TELEMETRY ENGINE
# 2024 BRITISH GRAND PRIX
# ==========================================
print("Starting F1 Data Engine...")
# 1. Enable local data caching
fastf1.Cache.enable_cache("data/cache")
# 2. Load the British Grand Prix race session
print("Loading 2024 British Grand Prix...")
session = fastf1.get_session(2024, "British", "R")
# 3. Download lap and weather data
session.load(
    laps=True,
    telemetry=False,
    weather=True
)
print("Race data downloaded successfully!")
# 4. Extract lap information
laps = session.laps
# 5. Display race information
print("\n========== RACE SUMMARY ==========")
print("Grand Prix:", session.event["EventName"])
print("Session:", session.name)
print("Total lap records:", len(laps))
# 6. Display selected data
print("\n========== FIRST 10 LAP RECORDS ==========")
print(
    laps[
        [
            "Driver",
            "LapNumber",
            "LapTime",
            "Compound",
            "TyreLife"
        ]
    ].head(10)
)
# 7. Save the raw dataset
output_path = "data/raw/british_gp_2024_laps.csv"
laps.to_csv(output_path, index=False)
print("\nDataset saved to:", output_path)
print("\nF1 DATA ENGINE COMPLETED SUCCESSFULLY!")
