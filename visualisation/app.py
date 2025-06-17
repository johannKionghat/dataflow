import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import geopandas as gpd
import time

# ---------------------
# Configuration
# ---------------------
st.set_page_config(page_title="Dashboard Emploi", page_icon="📊", layout="wide")
st.title("📊 Dashboard d'Analyse des Offres d'Emploi")

# ---------------------
# Chargement des données
# ---------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('./data/visualisation/jobs.csv')
        required = {'job_title', 'company', 'location', 'description'}
        if not required.issubset(df.columns):
            st.error("❌ Le fichier CSV ne contient pas toutes les colonnes requises.")
            return pd.DataFrame()
        df.dropna(subset=required, inplace=True)
        df['keywords'] = df['description'].str.lower().str.split()
        return df
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# ---------------------
# Filtres
# ---------------------
# ---------------------
# Filtres dynamiques
# ---------------------
st.sidebar.header("🧰 Filtres")

# 1. Entreprises les plus fréquentes
top_companies = (
    df['company']
    .value_counts()
    .head(5)
    .index
    .tolist()
)
companies = sorted(df['company'].dropna().unique())
company_selected = st.sidebar.multiselect(
    "Entreprise(s)",
    options=companies,
    default=top_companies
)

# 2. Localisations les plus fréquentes
top_locations = (
    df['location']
    .value_counts()
    .head(5)
    .index
    .tolist()
)
locations = sorted(df['location'].dropna().unique())
location_selected = st.sidebar.multiselect(
    "Localisation(s)",
    options=locations,
    default=top_locations
)

# ---------------------
# Filtrage des données
# ---------------------
df_filtered = df[
    df['company'].isin(company_selected) &
    df['location'].isin(location_selected)
]

# Empêcher affichage vide
if df_filtered.empty:
    st.warning("Aucune donnée trouvée avec les filtres sélectionnés. Essayez-en d'autres.")
    st.stop()

# ---------------------
# Résumé
# ---------------------
st.subheader("🔍 Résumé")
col1, col2, col3 = st.columns(3)
col1.metric("Nombre d'offres", len(df_filtered))
col2.metric("Entreprises", df_filtered['company'].nunique())
col3.metric("Localisations", df_filtered['location'].nunique())

# ---------------------
# Top Mots-clés
# ---------------------
st.subheader("🗝️ Top 10 mots-clés")
top_keywords = df_filtered['keywords'].explode().value_counts().head(10)
fig_keywords = px.bar(x=top_keywords.index, y=top_keywords.values,
                      labels={"x": "Mot clé", "y": "Occurrences"},
                      title="Top 10 mots-clés", color_discrete_sequence=["#1f77b4"])
st.plotly_chart(fig_keywords, use_container_width=True)

# ---------------------
# Croisement Job Title / Entreprise
# ---------------------
st.subheader("📊 Corrélation : Job Title vs Entreprise")
cross_tab = pd.crosstab(df_filtered['job_title'], df_filtered['company'])
fig_heatmap = px.imshow(cross_tab, text_auto=True, aspect="auto", color_continuous_scale="Blues")
st.plotly_chart(fig_heatmap, use_container_width=True)

# ---------------------
# Carte interactive avec GeoPandas
# ---------------------
st.subheader("🗺️ Carte des offres par localisation")

@st.cache_data
def geocode_locations(locations_list):
    geolocator = Nominatim(user_agent="job_dashboard")
    geo_data = []
    for loc in locations_list:
        try:
            location = geolocator.geocode(loc)
            if location:
                geo_data.append({"location": loc, "latitude": location.latitude, "longitude": location.longitude})
        except:
            continue
        time.sleep(1)  # pause pour éviter surcharge API
    return pd.DataFrame(geo_data)

geo_df = geocode_locations(df_filtered['location'].unique())
merged = pd.merge(df_filtered, geo_df, on='location', how='left').dropna(subset=["latitude", "longitude"])

fig_map = px.scatter_mapbox(
    merged,
    lat="latitude",
    lon="longitude",
    hover_name="job_title",
    hover_data=["company", "location"],
    color_discrete_sequence=["fuchsia"],
    zoom=3,
    height=500
)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# ---------------------
# Détails
# ---------------------
st.subheader("📄 Détail des Offres")
for _, row in df_filtered.iterrows():
    with st.expander(f"{row['job_title']} - {row['company']}"):
        st.markdown(f"**📍 Localisation :** {row['location']}")
        st.markdown(f"**📝 Description :** {row['description'][:500]}...")

# ---------------------
# Données brutes
# ---------------------
st.subheader("📊 Données brutes")
st.dataframe(df_filtered, use_container_width=True)
