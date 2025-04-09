import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Simulated comparison data
rally_lengths = ["1–3 Shots", "4–6 Shots", "7–9 Shots", "10+ Shots"]
shot_types = [
    "Forehand side", "Backhand side", "FH GS (top/flt/slc)",
    "BH GS (top/flt/slc)", "Volleys", "Smashes", "BH slice/chip", "FH drop shot"
]

data = []
np.random.seed(42)
for shot in shot_types:
    for r_len in rally_lengths:
        data.append({
            "Shot Type": shot,
            "Rally Length": r_len,
            "Fed Winner %": np.random.randint(5, 20),
            "Fed UFE %": np.random.randint(5, 15),
            "Fed PtEnd %": np.random.randint(15, 35),
            "Fed Winner/UFE": np.round(np.random.uniform(0.8, 2.0), 2),
            "Nadal Winner %": np.random.randint(5, 20),
            "Nadal UFE %": np.random.randint(5, 15),
            "Nadal PtEnd %": np.random.randint(15, 35),
            "Nadal Winner/UFE": np.round(np.random.uniform(0.8, 2.0), 2)
        })
df_compare = pd.DataFrame(data)

# Sidebar filters
st.sidebar.title("Filters")
selected_rally = st.sidebar.selectbox("Select Rally Length", ["All"] + rally_lengths)

# Filtered DataFrame
if selected_rally != "All":
    filtered_df = df_compare[df_compare["Rally Length"] == selected_rally]
else:
    filtered_df = df_compare

# Radar chart plotter
def plot_radar_chart(row, shot_label):
    labels = ["Winner %", "UFE %", "PtEnd %", "Winner/UFE"]
    fed_values = [
        row["Fed Winner %"],
        row["Fed UFE %"],
        row["Fed PtEnd %"],
        row["Fed Winner/UFE"] * 10
    ]
    nadal_values = [
        row["Nadal Winner %"],
        row["Nadal UFE %"],
        row["Nadal PtEnd %"],
        row["Nadal Winner/UFE"] * 10
    ]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    fed_values += fed_values[:1]
    nadal_values += nadal_values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, fed_values, label='Federer')
    ax.fill(angles, fed_values, alpha=0.25)
    ax.plot(angles, nadal_values, label='Nadal')
    ax.fill(angles, nadal_values, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title(f"Shot Profile: {shot_label}")
    ax.legend()
    st.pyplot(fig)

# Main layout
st.title("Federer vs Nadal: Shot Profile by Rally Length")

if selected_rally != "All":
    st.subheader(f"Rally Length: {selected_rally}")
else:
    st.subheader("All Rally Lengths Combined")

# Loop through each shot type
for shot in shot_types:
    st.markdown(f"### {shot}")
    shot_data = filtered_df[filtered_df["Shot Type"] == shot]
    if selected_rally == "All":
        row = shot_data.mean(numeric_only=True)
    else:
        row = shot_data.iloc[0]
    plot_radar_chart(row, shot)

# Comparison table
st.markdown("---")
st.markdown("#### Comparison Table")
st.dataframe(filtered_df.reset_index(drop=True))