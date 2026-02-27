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

@st.cache_resource
def load_model():
    model = joblib.load("model.joblib")
    return model

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv", sep=",")
    return df

# Composants
st.title("TARDIS: S.A.T.I.R")
st.markdown("<span style='color:#9d9e9f'>Système d'Analyse des Trains et d'Inspection des Retards</span>", unsafe_allow_html=True)

# Add anchors for navigation
st.markdown('<a id="overview"></a>', unsafe_allow_html=True)

try:
    df = load_data()
    model = load_model()
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
st.markdown('<a id="analysis"></a>', unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Répartition des retards", 
    "Analyse par gare", 
    "Train en retard vs à l'heure", 
    "Nombre de train en retard par type de service", 
    "Top 10 des gares avec le plus de retard au depart", 
    "Top 10 des gares avec le plus de retard à l'arrivée", 
    "Distribution des retards au depart", 
    "Distribution des retards à l'arrivée"
])

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

with tab3:
    st.subheader("Analyse comparative : Trains en retard vs à l'heure")
    st.image("assets/train_retard.png", width=500)

with tab4:
    st.subheader("Analyse comparative : Train en retard par type de service")
    st.image("assets/train_natio_internatio.png", width=800)

with tab5:
    st.subheader("Analyse comparative : Top 10 des gares avec le plus de retard au depart")
    st.image("assets/top_gare_retard_depart.png", width=800)

with tab6:
    st.subheader("Analyse comparative : Top 10 des gares avec le plus de retard à l'arrivée")
    st.image("assets/top_gare_retard_arrivee.png", width=800)

with tab7:
    st.subheader("Analyse comparative : Distribution des retards au depart")
    st.image("assets/retard_au_depart.png", width=900)

with tab8:
    st.subheader("Analyse comparative : Distribution des retards à l'arrivée")
    st.image("assets/retard_arrivee.png", width=900)

# PREDICTIONS
st.markdown('<a id="prediction"></a>', unsafe_allow_html=True)
st.divider()
st.header("🔮 Estimer mon retard")
st.info("Saisissez les détails de votre trajet ci-dessous pour obtenir une estimation du retard.")

# Formulaire de prédiction simplifié
with st.form("prediction_form"):
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        departure_station = st.selectbox(
            "Gare de départ",
            options=sorted(df["Gare de départ"].unique()),
            index=0
        )
        
        arrival_station = st.selectbox(
            "Gare d'arrivée",
            options=sorted(df["Gare d'arrivée"].unique()),
            index=0
        )
    
    with p_col2:
        month = st.number_input("Mois", min_value=1, max_value=12, value=6)
        day_of_week = st.number_input("Jour de la semaine (0=Lundi, 6=Dimanche)", min_value=0, max_value=6, value=3)
    
    submit_button = st.form_submit_button("Estimer le retard")

# Affichage des résultats
if submit_button:
    try:
        # Préparation des données pour la prédiction avec valeurs par défaut
        import pandas as pd
        
        # Récupération des valeurs moyennes pour les champs manquants
        default_service = df["Service"].mode()[0]
        default_year = df["Année"].mode()[0]
        default_duration = df[df["Gare de départ"] == departure_station]["Durée moyenne du trajet"].mean()
        default_circulations = df[df["Gare de départ"] == departure_station]["Nombre de circulations prévues"].mean()
        
        # Si les valeurs par défaut sont NaN, utiliser des valeurs globales
        if pd.isna(default_duration):
            default_duration = df["Durée moyenne du trajet"].mean()
        if pd.isna(default_circulations):
            default_circulations = df["Nombre de circulations prévues"].mean()
        
        input_data = pd.DataFrame({
            'Gare de départ': [departure_station],
            "Gare d'arrivée": [arrival_station],
            'Service': [default_service],
            'Année': [default_year],
            'Mois': [month],
            'day_of_week': [day_of_week],
            'Durée moyenne du trajet': [default_duration],
            'Nombre de circulations prévues': [default_circulations]
        })
        
        # Prédiction
        predicted_delay = model.predict(input_data)[0]
        
        # Affichage du résultat
        st.success(f"🎯 **Retard estimé : {predicted_delay:.1f} minutes**")
        
        # Interprétation
        if predicted_delay < 5:
            st.info("✅ Votre train devrait être à l'heure !")
        elif predicted_delay < 15:
            st.warning("⚠️ Petit retard prévu. Prévoyez un peu de marge.")
        elif predicted_delay < 30:
            st.warning("⚠️ Retard significatif. Vous pourriez manquer une correspondance.")
        else:
            st.error("❌ Retard important. Envisagez des alternatives de transport.")
        
        # Visualisation comparative
        st.subheader("Comparaison avec les retards moyens")
        avg_delay = df[df["Gare de départ"] == departure_station]["Retard moyen de tous les trains à l'arrivée"].mean()
        
        comparison_data = pd.DataFrame({
            'Type': ['Votre estimation', 'Moyenne historique'],
            'Retard (minutes)': [predicted_delay, avg_delay]
        })
        
        fig_comparison = px.bar(
            comparison_data,
            x='Type',
            y='Retard (minutes)',
            title="Comparaison de votre retard estimé avec la moyenne historique",
            color='Type',
            template="plotly_white"
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation rapide")
st.sidebar.markdown("[Vue d'ensemble](#overview)")
st.sidebar.markdown("[Analyse](#analysis)")
st.sidebar.markdown("[Prédiction](#prediction)")
st.sidebar.markdown("---")
st.sidebar.caption("The Satir : Tardis Project by Meghan, Evanne and Wyliam")