# F1 Strategy & Telemetry Engine

An end-to-end Formula 1 data analytics project analysing the **2024 British Grand Prix at Silverstone** using Python, FastF1, Pandas, SQLite, Plotly and Streamlit.

## Project Overview

This project transforms Formula 1 race telemetry into driver performance analysis, tyre degradation estimates and illustrative race strategy comparisons.

The project covers the complete data workflow: collection, cleaning, validation, storage, analysis, modelling and interactive visualisation.

## Features

- **Race data collection:** Downloaded lap and weather data using FastF1.
- **Data processing:** Cleaned and transformed 960 recorded lap entries.
- **Data validation:** Checked duplicate records, invalid lap times and tyre age values.
- **SQL analytics:** Stored race data in SQLite and performed analytical queries.
- **Driver performance:** Compared average analysis lap times across 19 drivers.
- **Tyre analysis:** Examined compound usage and stint performance.
- **Degradation modelling:** Applied linear regression to estimate lap-time changes with tyre age across 37 stints.
- **Strategy simulation:** Compared illustrative one-stop and two-stop strategies.
- **Interactive dashboard:** Built a Streamlit application with Plotly visualisations and driver filters.

## Technology Stack

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python     | Main programming language             |
| FastF1     | Formula 1 timing and telemetry data   |
| Pandas     | Data processing and analysis          |
| NumPy      | Numerical calculations and regression |
| SQLite     | Relational data storage               |
| SQL        | Data querying                         |
| Matplotlib | Static visualisations                 |
| Plotly     | Interactive charts                    |
| Streamlit  | Interactive dashboard                 |

## Project Structure

```text
f1-strategy-engine/
├── data/
│   ├── raw/
│   ├── cache/
│   ├── processed/
│   └── database/
├── notebooks/
├── outputs/
├── src/
│   ├── test_fastf1.py
│   ├── explore_data.py
│   ├── deep_dive.py
│   ├── visualize_data.py
│   ├── process_data.py
│   ├── validate_data.py
│   ├── load_database.py
│   ├── run_sql_queries.py
│   ├── tyre_degradation_model.py
│   ├── strategy_simulator.py
│   └── dashboard.py
├── requirements.txt
└── README.md
```

## Running the Project

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd f1-strategy-engine
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
streamlit run src/dashboard.py
```

The dashboard will be available at:

`http://localhost:8501`

## Key Findings

- 960 recorded lap entries across 19 drivers.
- 868 analysis-ready laps after excluding pit-in and pit-out laps.
- 37 tyre stints included in the degradation model.
- The strategy simulator produced a faster one-stop result under its current illustrative assumptions.

## Important Modelling Limitations

The tyre degradation estimates are based on linear regression of lap time against tyre age. Lap times are also influenced by weather, fuel load, traffic, safety cars and track evolution.

The strategy simulator currently uses illustrative baseline lap times and an assumed pit-stop time loss. Its results should not be interpreted as validated race predictions.

These limitations are important when interpreting the results.

## Project Objective

The objective was to build a complete Formula 1 analytics workflow while developing practical skills in Python, SQL, data engineering, statistical modelling and interactive visualisation.
