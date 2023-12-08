import streamlit as st
import pydeck as pdk
import json

# Fonction pour charger des données GeoJSON
@st.cache(allow_output_mutation=True)
def load_geojson_data(path):
    with open(path, 'r') as f:
        return json.load(f)

# Création de la couche GeoJsonLayer
geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    opacity=0.0,
    stroked=False,
    filled=False,
    extruded=True,
    wireframe=True,
)

# Création de la vue initiale de la carte centrée sur Saint-Denis, Île de la Réunion
view_state = pdk.ViewState(latitude=-20.882057, longitude=55.450675, zoom=10, bearing=0, pitch=45)
r = pdk.Deck(layers=[geojson_layer], initial_view_state=view_state)

# Affichage de la carte dans Streamlit
st.pydeck_chart(r)
