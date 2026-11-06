
import pandas as pd

# Load our downloaded F1 dataset
file_path = "data/raw/british_gp_2024_laps.csv"

df = pd.read_csv(file_path)

# 1. Dataset overview
print("\n========== DATASET OVERVIEW ==========")

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# 2. Column information
print("\n========== COLUMN NAMES ==========")

print(df.columns.tolist())

# 3. Missing values
print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())

# 4. Driver information
print("\n========== DRIVER ANALYSIS ==========")

print("Number of drivers:", df["Driver"].nunique())

print("\nDrivers:")
print(df["Driver"].unique())

# 5. Tyre compounds
print("\n========== TYRE COMPOUNDS ==========")

print(df["Compound"].value_counts())

# 6. Lap records per driver
print("\n========== LAPS PER DRIVER ==========")

print(
    df.groupby("Driver")["LapNumber"]
    .count()
    .sort_values(ascending=False)
)

# 7. Display sample records
print("\n========== SAMPLE DATA ==========")

print(
    df[
        [
            "Driver",
            "LapNumber",
            "LapTime",
            "Compound",
            "TyreLife"
        ]
    ].head(15).to_string(index=False)
)

print("\nDATA EXPLORATION COMPLETED!")
