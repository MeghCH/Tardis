import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

#CONFIG
st.set_page_config(page_title="SNCF TARDIS Dashboard", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("tardis_model.joblib")

@st.cache_data
def load_data():
    # chemin dataset
    df = pd.read_csv("cleaned_dataset.csv")
    return df

# Composants
st.title("TARDIS: Train Analysis & Delay Inspection System")
st.markdown("Automated insights for the SNCF Data Analysis Service.")

try:
    df = load_data()
    model = load_model()
except Exception as e:
    st.error(f"Error loading assets: {e}. Please ensure the CSV and model file exist.")
    st.stop()

# Filtres
st.sidebar.header("Filters & Controls")
selected_train_type = st.sidebar.multiselect(
    "Select Train Type", 
    options=df["train_type"].unique(), 
    default=df["train_type"].unique()
)

filtered_df = df[df["train_type"].isin(selected_train_type)]

#1 indicateurs cles
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Trips", f"{len(filtered_df):,}")
with col2:
    avg_delay = filtered_df["delay_minutes"].mean()
    st.metric("Avg Delay", f"{avg_delay:.1f} min")
with col3:
    punctuality = (filtered_df["delay_minutes"] < 5).mean() * 100
    st.metric("Punctuality Rate", f"{punctuality:.1%}")
with col4:
    max_delay = filtered_df["delay_minutes"].max()
    st.metric("Worst Delay", f"{max_delay} min")

st.divider()

#2 visualisations
tab1, tab2 = st.tabs(["Delay Distribution", "Station Analysis"])

with tab1:
    st.subheader("How often do delays occur?")
    fig_dist = px.histogram(
        filtered_df, 
        x="delay_minutes", 
        nbins=50, 
        color="train_type",
        title="Distribution of Delays by Train Category",
        labels={"delay_minutes": "Delay (Minutes)"},
        template="plotly_white"
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    st.subheader("Top 10 Most Delayed Routes")
    route_stats = filtered_df.groupby(["departure_station", "arrival_station"])["delay_minutes"].mean().reset_index()
    top_routes = route_stats.sort_values("delay_minutes", ascending=False).head(10)
    
    fig_bar = px.bar(
        top_routes, 
        x="delay_minutes", 
        y="departure_station", 
        orientation='h',
        color="delay_minutes",
        title="Average Delay by Departure Station"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

#3 predictions
st.divider()
st.header("Predict Your Delay")
st.info("Enter your journey details below to see the estimated delay.")

p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    dep_st = st.selectbox("Departure Station", options=df["departure_station"].unique())
    arr_st = st.selectbox("Arrival Station", options=df["arrival_station"].unique())

with p_col2:
    train_t = st.selectbox("Train Type", options=df["train_type"].unique())
    day_w = st.select_slider("Day of Week", options=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

with p_col3:
    dep_hour = st.number_input("Departure Hour (0-23)", min_value=0, max_value=23, value=12)

if st.button("Calculate Estimated Delay", type="primary"):
    input_data = pd.DataFrame({
        'departure_station': [dep_st],
        'arrival_station': [arr_st],
        'train_type': [train_t],
        'day_of_week': [day_w],
        'departure_hour': [dep_hour]
    })
    
    prediction = model.predict(input_data)[0]
    
    #Resultat
    st.success(f"Predicted Delay: {max(0, round(prediction, 1))} minutes")
    
    if prediction > 15:
        st.warning("This route is prone to significant delays. Plan accordingly!")
    else:
        st.info("This route appears relatively stable.")

st.sidebar.markdown("---")
st.sidebar.caption("SNCF TARDIS Project | v1.0")