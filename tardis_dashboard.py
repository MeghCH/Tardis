import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

# CONFIG
st.set_page_config(page_title="SNCF TARDIS Dashboard", layout="wide")

# Injection de la police Inter
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, span {
        font-family: 'Inter', sans-serif !important;
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #1E293B; 
        letter-spacing: -0.02em; 
    }

    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
            
    .st-emotion-cache-1r6slb0, .custom-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    [data-testid="stMetricValue"] {
        color: #1c9dc8ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# @st.cache_resource
# def load_model():
#     return joblib.load("tardis_model.joblib")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv", sep=",")
    return df

# Composants
st.title("TARDIS: Système d'Analyse des Trains et d'Inspection des Retards")
st.markdown("<span style='color:#9d9e9f'>Analyses automatisées pour le Service d'Étude des Données de la SNCF.</span>", unsafe_allow_html=True)

try:
    df = load_data()
    # model = load_model()
except Exception as e:
    st.error(f"Erreur lors du chargement des ressources : {e}. Veuillez vous assurer que le fichier CSV et le modèle existent.")
    st.stop()

#FILTRES 
st.sidebar.header("Filtres & Commandes")
selected_train_type = st.sidebar.multiselect(
    "Choisir le type de trajet", 
    options=df["Service"].unique(), 
    default=df["Service"].unique()
)

filtered_df = df[df["Service"].isin(selected_train_type)]

#INDICATEURS CLÉS 
col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.metric("Nombre total de trajets", f"{len(filtered_df):,}")
with col2:
    with st.container(border=True):
        col_retard = "Retard moyen de tous les trains à l'arrivée"
        avg_delay = filtered_df[col_retard].mean()
        st.metric("Retard moyen", f"{avg_delay:.1f} min")
with col3:
    with st.container(border=True):
        punctuality = (filtered_df[col_retard] < 5).mean() * 100
        st.metric("Taux de ponctualité", f"{punctuality:.1f}%")
with col4:
    with st.container(border=True):
        max_delay = filtered_df[col_retard].max()
        st.metric("Plus long retard enregistré", f"{max_delay:.0f} min")

st.divider()

#VISUALISATIONS
tab1, tab2 = st.tabs(["Répartition des retards", "Analyse par gare"])

with tab1:
    st.subheader("Fréquence des retards")
    fig_dist = px.histogram(
        filtered_df, 
        x=col_retard, 
        nbins=50, 
        color="Service",
        title="Répartition des retards par catégorie de train",
        labels={col_retard: "Retard (Minutes)"},
        template="plotly_white"
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    st.subheader("Top 10 des liaisons les plus retardées")
    route_stats = filtered_df.groupby(["Gare de départ", "Gare d'arrivée"])[col_retard].mean().reset_index()
    top_routes = route_stats.sort_values(col_retard, ascending=False).head(10)
    
    fig_bar = px.bar(
        top_routes, 
        x=col_retard, 
        y="Gare de départ", 
        orientation='h',
        color=col_retard,
        title="Retard moyen par gare de départ",
        labels={col_retard: "Moyenne retard (min)"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

#PREDICTIONS
st.divider()
st.header("Estimer mon retard")
st.info("Saisissez les détails de votre trajet ci-dessous pour obtenir une estimation du retard.")

p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    dep_st = st.selectbox("Gare de départ", options=df["Gare de départ"].unique())
    arr_st = st.selectbox("Gare d'arrivée", options=df["Gare d'arrivée"].unique())

with p_col2:
    train_t = st.selectbox("Type de train", options=df["Service"].unique())
    mois_sel = st.slider("Mois", min_value=1, max_value=12, value=1)

if st.button("Lancer l'estimation", type="primary"):
    st.warning("Le modèle de prédiction est actuellement désactivé. Veuillez entraîner votre modèle pour activer cette fonctionnalité.")

st.sidebar.markdown("---")
st.sidebar.caption("SNCF TARDIS Project")