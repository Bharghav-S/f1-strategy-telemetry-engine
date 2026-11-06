
import sqlite3
from pathlib import Path

# Locate database
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_ROOT / "data" / "database" / "f1_strategy.db"

# Connect to database
connection = sqlite3.connect(DB_FILE)

cursor = connection.cursor()


# QUERY 1: Total number of laps
print("\n--- QUERY 1: TOTAL LAP RECORDS ---")

cursor.execute("""
SELECT COUNT(*)
FROM race_laps;
""")

print(cursor.fetchone()[0])


# QUERY 2: Number of laps per driver
print("\n--- QUERY 2: LAPS PER DRIVER ---")

cursor.execute("""
SELECT
    Driver,
    COUNT(*) AS total_laps
FROM race_laps
GROUP BY Driver
ORDER BY total_laps DESC;
""")

for row in cursor.fetchall():
    print(row)


# QUERY 3: Average lap time per driver
print("\n--- QUERY 3: DRIVER AVERAGE LAP TIME ---")

cursor.execute("""
SELECT
    Driver,
    ROUND(AVG(LapTime_seconds), 3) AS average_lap_time
FROM race_laps
WHERE IsAnalysisLap = 1
GROUP BY Driver
ORDER BY average_lap_time ASC;
""")

for row in cursor.fetchall():
    print(row)


# QUERY 4: Tyre compound usage
print("\n--- QUERY 4: TYRE COMPOUND USAGE ---")

cursor.execute("""
SELECT
    Compound,
    COUNT(*) AS total_laps
FROM race_laps
GROUP BY Compound
ORDER BY total_laps DESC;
""")

for row in cursor.fetchall():
    print(row)


# QUERY 5: Drivers with more than 45 analysis laps

print("\n--- QUERY 5: DRIVERS WITH MORE THAN 45 ANALYSIS LAPS ---")

cursor.execute("""
SELECT
    Driver,
    COUNT(*) AS analysis_laps
FROM race_laps
WHERE IsAnalysisLap = 1
GROUP BY Driver
HAVING COUNT(*) > 45
ORDER BY analysis_laps DESC;
""")

for row in cursor.fetchall():
    print(row)


# QUERY 6: Categorise lap times

print("\n--- QUERY 6: LAP TIME CATEGORIES ---")

cursor.execute("""
SELECT
    Driver,
    CASE
        WHEN LapTime_seconds < 90 THEN 'Under 90 seconds'
        WHEN LapTime_seconds < 100 THEN '90-100 seconds'
        ELSE '100+ seconds'
    END AS lap_category,
    COUNT(*) AS total_laps
FROM race_laps
WHERE IsAnalysisLap = 1
GROUP BY Driver, lap_category
ORDER BY Driver, lap_category;
""")

for row in cursor.fetchall():
    print(row)

# Close connection
connection.close()
