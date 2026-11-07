
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "processed" / "british_gp_2024_laps_processed.csv"
MODEL_FILE = ROOT / "outputs" / "tyre_degradation_model.csv"

st.set_page_config(
    page_title="F1 Strategy & Telemetry Engine",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ F1 Strategy & Telemetry Engine")
st.subheader("2024 British Grand Prix — Silverstone")
st.caption("Race analysis | Driver performance | Tyre degradation | Strategy simulation")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    race = pd.read_csv(DATA_FILE)
    degradation = pd.read_csv(MODEL_FILE)
    return race, degradation

try:
    race, degradation = load_data()
except FileNotFoundError as error:
    st.error(f"Could not find a required data file: {error}")
    st.stop()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

drivers = sorted(race["Driver"].dropna().unique())

selected_drivers = st.sidebar.multiselect(
    "Select drivers",
    drivers,
    default=drivers
)

filtered = race[race["Driver"].isin(selected_drivers)].copy()
analysis = filtered[filtered["IsAnalysisLap"] == True].copy()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_laps = len(race)
total_drivers = race["Driver"].nunique()
analysis_laps = len(analysis)

if not analysis.empty:
    fastest_lap = analysis["LapTime_seconds"].min()
else:
    fastest_lap = 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total recorded laps", f"{total_laps:,}")
c2.metric("Drivers", total_drivers)
c3.metric("Analysis-ready laps", f"{analysis_laps:,}")
c4.metric(
    "Fastest analysis lap",
    f"{fastest_lap:.3f} s" if fastest_lap else "N/A"
)

st.divider()

# --------------------------------------------------
# DRIVER PERFORMANCE
# --------------------------------------------------

st.header("1. Driver Performance")

if not analysis.empty:
    driver_pace = (
        analysis.groupby("Driver")["LapTime_seconds"]
        .mean()
        .reset_index()
        .sort_values("LapTime_seconds")
    )

    fig = px.bar(
        driver_pace,
        x="Driver",
        y="LapTime_seconds",
        color="LapTime_seconds",
        color_continuous_scale="Turbo",
        title="Average Analysis Lap Time by Driver",
        labels={"LapTime_seconds": "Average lap time (seconds)"}
    )

    st.plotly_chart(fig, width="stretch")
else:
    st.info("No analysis laps available for the selected drivers.")

# --------------------------------------------------
# TYRE COMPOUND USAGE
# --------------------------------------------------

st.header("2. Tyre Strategy")

compound_counts = (
    filtered["Compound"]
    .value_counts()
    .rename_axis("Compound")
    .reset_index(name="Lap count")
)

fig = px.pie(
    compound_counts,
    names="Compound",
    values="Lap count",
    title="Tyre Compound Usage",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# TYRE DEGRADATION
# --------------------------------------------------

st.header("3. Tyre Degradation Model")

filtered_model = degradation[
    degradation["Driver"].isin(selected_drivers)
].copy()

if not filtered_model.empty:
    fig = px.scatter(
        filtered_model,
        x="Stint",
        y="Degradation_sec_per_lap",
        color="Compound",
        hover_data=["Driver", "R_squared"],
        title="Estimated Degradation by Driver and Stint",
        labels={
            "Stint": "Stint number",
            "Degradation_sec_per_lap": "Estimated seconds per lap"
        }
    )

    fig.add_hline(y=0, line_dash="dash")
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Positive slopes indicate lap times increased with tyre age in the fitted "
        "stint. Negative slopes do not prove tyres improved. Weather, traffic, "
        "fuel load and track evolution can affect these estimates."
    )
else:
    st.info("No degradation model results for the selected drivers.")

# --------------------------------------------------
# STRATEGY SIMULATION
# --------------------------------------------------

st.header("4. Race Strategy Simulator")

st.warning(
    "Prototype: baseline lap times and pit-stop loss are illustrative assumptions. "
    "Results are not validated race predictions."
)

pit_loss = st.slider(
    "Assumed time lost per pit stop (seconds)",
    min_value=10,
    max_value=35,
    value=22
)

base_times = {
    "SOFT": 90.5,
    "MEDIUM": 91.0,
    "HARD": 91.5
}

strategies = {
    "One-stop": [
        ("MEDIUM", 25),
        ("SOFT", 27)
    ],
    "Two-stop": [
        ("MEDIUM", 18),
        ("MEDIUM", 17),
        ("SOFT", 17)
    ]
}

results = []

for strategy_name, stints in strategies.items():
    total_time = 0

    for compound, laps in stints:
        compound_data = degradation[
            degradation["Compound"] == compound
        ]

        if compound_data.empty:
            total_time = None
            break

        slope = compound_data["Degradation_sec_per_lap"].median()

        stint_time = sum(
            base_times[compound] + slope * (age - 1)
            for age in range(1, laps + 1)
        )

        total_time += stint_time

    if total_time is not None:
        total_time += (len(stints) - 1) * pit_loss

        results.append({
            "Strategy": strategy_name,
            "Total laps": sum(laps for _, laps in stints),
            "Projected time (seconds)": total_time
        })

if results:
    strategy_df = pd.DataFrame(results)

    fig = px.bar(
        strategy_df,
        x="Strategy",
        y="Projected time (seconds)",
        color="Strategy",
        title="Illustrative Strategy Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(strategy_df, hide_index=True, use_container_width=True)

    fastest = strategy_df.loc[
        strategy_df["Projected time (seconds)"].idxmin()
    ]

    st.success(
        f"Fastest under these assumptions: {fastest['Strategy']} "
        f"({fastest['Projected time (seconds)']:.2f} seconds)"
    )
else:
    st.error("Could not calculate strategies. Check the degradation data.")

# --------------------------------------------------
# RAW DATA EXPLORER
# --------------------------------------------------

st.header("5. Lap Data Explorer")

columns = [
    "Driver",
    "LapNumber",
    "LapTime_seconds",
    "Compound",
    "TyreLife",
    "Stint",
    "IsAnalysisLap"
]

available_columns = [col for col in columns if col in filtered.columns]

st.dataframe(
    filtered[available_columns],
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download filtered lap data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="british_gp_filtered_laps.csv",
    mime="text/csv"
)

st.divider()
st.caption("Built with Python, FastF1, Pandas, SQLite, Plotly and Streamlit.")


# --------------------------------------------------
# ADDITIONAL RACE ANALYSIS GALLERY
# --------------------------------------------------

st.divider()

st.header("6. Additional Race Analysis")
st.write(
    "Explore the additional visualisations generated "
    "during the analysis of the 2024 British Grand Prix."
)

gallery = [
    {
        "title": "Driver Lap Progression",
        "file": "driver_lap_progression.png",
        "description": "Lap-time progression across the race."
    },
    {
        "title": "Tyre Degradation",
        "file": "tyre_degradation.png",
        "description": "Lap times against tyre age."
    },
    {
        "title": "Compound Comparison",
        "file": "compound_comparison.png",
        "description": "Lap-time distributions by tyre compound."
    },
    {
        "title": "Stint Comparison",
        "file": "stint_comparison.png",
        "description": "Performance comparison across race stints."
    },
    {
        "title": "Tyre Degradation Regression Model",
        "file": "tyre_degradation_model.png",
        "description": "Estimated lap-time degradation slopes."
    }
]

for item in gallery:
    image_path = ROOT / "outputs" / item["file"]

    if image_path.exists():
        st.subheader(item["title"])
        st.caption(item["description"])
        st.image(str(image_path), width="stretch")
    else:
        st.warning(f"Missing visualisation: {item['file']}")
