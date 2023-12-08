import json
import pandas as pd
import pydeck as pdk
import streamlit as st
import plotly.express as px

# Configurer la page pour utiliser une mise en page en pleine largeur
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .reportview-container .markdown-text-container {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center'>Dataviz</h1>", unsafe_allow_html=True)


# Fonction pour charger des données GeoJSON
@st.cache(allow_output_mutation=True)
def load_geojson_data(path):
    with open(path, 'r') as f:
        return json.load(f)


# Création de la vue initiale de la carte centrée sur Saint-Denis, Île de la Réunion
view_state = pdk.ViewState(latitude=-20.882057, longitude=55.450675, zoom=10, bearing=0, pitch=45)
geojson_layer = pdk.Layer("GeoJsonLayer", opacity=0.0, stroked=False, filled=False, extruded=True, wireframe=True)
r = pdk.Deck(layers=[geojson_layer], initial_view_state=view_state)

# Affichage de la carte dans Streamlit
# st.pydeck_chart(r)


# Chargement des données pour la treemap
population = pd.read_csv("./data/csv_folder/population-francaise-communespublic.csv", encoding="utf-8", sep=";", na_values="-").fillna(0)

# Obtenez les années uniques dans les données
annees = population['Année utilisation'].unique()
annees.sort()  # Assurez-vous que les années sont dans l'ordre

# Créer un curseur pour sélectionner l'année
annee_selectionnee = st.slider("Sélectionnez l'année", int(annees.min()), int(annees.max()), int(annees.max()))


# Filtrer les données pour l'année sélectionnée
population_filtree = population[population['Année utilisation'] == annee_selectionnee]

# Création de la treemap
treemap = px.treemap(population_filtree,
                     path=["Code arrondissement départemental", "Nom de la commune"],
                     values="Population totale",
                     custom_data=["Population totale"])

# Ajouter des annotations pour chaque case du treemap
for trace in treemap.data:
    trace.text = trace.customdata[0]
    trace.textposition = 'middle center'
    trace.textfont = {'color':'white', 'size':15, 'family':"Arial, bold"}



sunburst = px.sunburst(population_filtree,
                  path=["Code arrondissement départemental", "Nom de la commune"],
                  values="Population totale",
                  custom_data=["Population totale"])

# Ajouter et personnaliser les annotations pour chaque section du sunburst
for trace in sunburst.data:
    trace.text = trace.customdata[0]
    trace.textfont = {'color':'white', 'size':12, 'family':"Arial, bold"}  # Ajustez selon vos besoins


# Utilisation des onglets avec des colonnes pour centrer le contenu
tab1, tab2 = st.tabs(["Répartition de la Population", "Détail par Commune"])

with tab1:
    st.plotly_chart(treemap, use_container_width=True)

with tab2:
    st.plotly_chart(sunburst, use_container_width=True)


