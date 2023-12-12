import streamlit as st
import pandas as pd
import numpy as np
from api import population, df_population_codcom, df_conso_edf_codcom,populations
import plotly.express as px
import random  # Ajout de l'importation du module random
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


# Configurer la page pour utiliser une mise en page en pleine largeur
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .reportview-container .markdown-text-container {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center'>Evolution démographique et consommmation élèctrique à la Réunion</h1>", unsafe_allow_html=True)




# Obtenez les années uniques dans les données
annees = population['annee'].astype(str).unique()
annees.sort()  # Assurez-vous que les années sont dans l'ordre

annee_conso = population['annee'].astype(str).unique()
annee_conso.sort() 

annees = np.union1d(annees, annee_conso)

# Créer un curseur pour sélectionner l'année
annee_selectionnee = st.slider("Sélectionnez l'année", int(annees.min()), int(annees.max()), int(annees.max()))
annee_selectionnee_str = str(annee_selectionnee)
population_filtree = population[population['annee'] == annee_selectionnee_str]


#annee n-1
annee_n_1 = annee_selectionnee - 1
annee_selectionnee_str_n_1 = str(annee_n_1)
population_filtree_n_1 = population[population['annee'] == annee_selectionnee_str_n_1]

#annee n-2
annee_n_2 = annee_selectionnee - 2
annee_selectionnee_str_n_2 = str(annee_n_2)
population_filtree_n_2 = population[population['annee'] == annee_selectionnee_str_n_2]


#indicateur kpi population total
# Calculer votre indicateur KPI (par exemple, la somme de la population)
kpi_value = population_filtree['population_totale'].sum()
if kpi_value == 0:
    kpi_value = "donnée manquante"
kpi_value_n1 = population_filtree_n_1['population_totale'].sum()
if kpi_value_n1 == 0:
    kpi_value_n1 = "donnée manquante"
kpi_value_n2 = population_filtree_n_2['population_totale'].sum()
if kpi_value_n2 == 0:
    kpi_value_n2 = "donnée manquante"

kpi_conso_edf_2 = population_filtree_n_2['consommation_mwh'].sum()
if kpi_conso_edf_2 == 0:
    kpi_conso_edf_2 = "donnée manquante"
kpi_conso_edf_1 = population_filtree_n_1['consommation_mwh'].sum()
if kpi_conso_edf_1 == 0:
    kpi_conso_edf_1 = "donnée manquante"
kpi_conso_edf = population_filtree['consommation_mwh'].sum()
if kpi_conso_edf == 0:
    kpi_conso_edf = "donnée manquante"

# Afficher l'indicateur KPI
#st.markdown(f"### Population Totale {annee_selectionnee_str}: {kpi_value}")

# Afficher l'indicateur KPI
#st.markdown(f"### Population Totale Annee {annee_selectionnee_str_n_1} : {kpi_value_n1}")

# Afficher les indicateurs KPI dans deux colonnes
col1, col2, col3 = st.columns(3)

# Afficher l'indicateur KPI pour l'année sélectionnée dans la première colonne
#col1.markdown(f"### Population en {annee_n_2}: {kpi_value_n2}")


# Ajouter un style de carte à l'élément Markdown
# Afficher l'indicateur KPI pour l'année sélectionnée dans la première colonne
#col1.markdown(f"### Population en {annee_n_2}: {kpi_value_n2}")



with col1.container():
    st.subheader(f"Population {annee_n_2}")
    #st.info("Ceci est le nombre démographique pour l'année sélectionnée.")
    
    # Utiliser des balises HTML pour ajuster la taille de police
    st.markdown(f"<p style='font-size:36px; font-weight:bold'>{kpi_value_n2}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:24px; font-weight:bold'>{kpi_conso_edf_2} mwh</p>", unsafe_allow_html=True)

#col2.markdown(f"### Population en {annee_n_1}: {kpi_value_n1}")
with col2.container():
    st.subheader(f"Population {annee_n_1}")
    #st.info("Ceci est le nombre démographique pour l'année sélectionnée.")
    
    # Utiliser des balises HTML pour ajuster la taille de police
    st.markdown(f"<p style='font-size:36px; font-weight:bold'>{kpi_value_n1}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:24px; font-weight:bold'>{kpi_conso_edf_1} mwh</p>", unsafe_allow_html=True)


#col3.markdown(f"### Population en {annee_selectionnee}: {kpi_value}")
# Afficher l'indicateur KPI pour l'année précédente dans la deuxième colonne
with col3.container():
    st.subheader(f"Population {annee_selectionnee}")
    #st.info("Ceci est le nombre démographique pour l'année sélectionnée.")
    
    # Utiliser des balises HTML pour ajuster la taille de police
    st.markdown(f"<p style='font-size:36px; font-weight:bold'>{kpi_value}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:24px; font-weight:bold'>{kpi_conso_edf} mwh</p>", unsafe_allow_html=True)




# Ajouter un séparateur (ligne horizontale)
# Ajouter une ligne horizontale (séparateur)
#st.markdown('<hr>', unsafe_allow_html=True)
# Créer une ligne horizontale personnalisée comme séparateur
st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)


#chargement du fichier geoson
import json

with open("communes-974-la-reunion.geojson") as f:
    communes = json.loads(f.read())
codes3 = sorted([f["properties"]["code"] for f in communes["features"]])

# choropleth_mapbox
fig = px.choropleth_mapbox(data_frame=df_population_codcom,
                     geojson=communes,
                     locations='code_insee_commune',
                     color='population_totale',
                     featureidkey='properties.code',
                     color_continuous_scale="reds",
                     mapbox_style="open-street-map",
                     zoom=8.9,
                     center = {"lat": -21.115141, "lon": 55.536384},
                     opacity=0.5,
                     labels={'Population totale': 'Population totale'}
                    )

fig1 = px.choropleth_mapbox(data_frame=df_conso_edf_codcom,
                     geojson=communes,
                     locations='code_insee',
                     color='consommation_mwh',
                     featureidkey='properties.code',
                     color_continuous_scale="reds",
                     mapbox_style="open-street-map",
                     zoom=8.5,
                     center = {"lat": -21.115141, "lon": 55.536384},
                     opacity=0.3,
                     labels={'Consamation EDF': 'Cosommation EDF en mwh'}
                    )
# Afficher la carte dans Streamlit
#st.plotly_chart(fig)
#st.plotly_chart(fig)
# Données
annee = population["annee"]
consommation_mwh = population["consommation_mwh"]
population_totale = population["population_totale"]

# Créer une figure plus grande





coll1, coll2, = st.columns(2)
with coll1.container():
    # Créer un curseur pour sélectionner l'année
    st.subheader(f"Concentration de la population réunionnaise")
# Afficher les deux cartes dans une même ligne
    st.plotly_chart(fig, use_container_width=True)

with coll2.container():
    st.subheader(f"Consommation élètrique par année")
# Afficher les deux cartes dans une même ligne
    # Afficher le graphique
    # Créer une figure Matplotlib
    fig3, ax1 = plt.subplots(figsize=(10, 6))

    # Barres pour la consommation d'énergie
    ax1.bar(annee, consommation_mwh, color='skyblue', label='Consommation d\'énergie (MWh)')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Consommation d\'énergie (MWh)', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    # Ajuster les limites de l'axe y pour la consommation d'énergie (utiliser un range plus grand)
    ax1.set_ylim(0, max(consommation_mwh) * 1.2)

    # Créer un deuxième axe partageant le même axe x
    ax2 = ax1.twinx()

    # Courbe pour la population
    ax2.plot(annee, population_totale, color='tomato', marker='o', label='Population totale', linewidth=2)
    ax2.set_ylabel('Population totale', color='tomato')
    ax2.tick_params(axis='y', labelcolor='tomato')

    # Ajouter une légende pour la consommation d'énergie
    ax1.legend(loc='upper left')

    # Masquer la légende en haut
    ax2.legend().set_visible(False)

    # Ajouter un titre
    plt.title('Consommation électrique et Population totale par année', fontsize=16)

    # Placer la légende en dehors du graphique
    fig3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)

    # Ajuster la disposition pour éviter que la légende ne chevauche le graphique
    plt.tight_layout()

    # Afficher la figure dans Streamlit
    st.pyplot(fig3)














st.markdown("### Population par n° arrondissement", unsafe_allow_html=True)
# Création de la treemap
# Création de la treemap
treemap = px.treemap(populations,
                     path=["code_arrondissement", "nom_de_la_commune"],
                     values="population_totale",
                     custom_data=["population_totale"])

# Ajouter des annotations pour chaque case du treemap
for trace in treemap.data:
    trace.text = trace.customdata[0]
    trace.textposition = 'middle center'
    trace.textfont = {'color':'white', 'size':15, 'family':"Arial, bold"}



sunburst = px.sunburst(populations,
                  path=["code_arrondissement", "nom_de_la_commune"],
                  values="population_totale",
                  custom_data=["population_totale"])

# Ajouter et personnaliser les annotations pour chaque section du sunburst
for trace in sunburst.data:
    trace.text = trace.customdata[0]
    trace.textfont = {'color':'white', 'size':12, 'family':"Arial, bold"}  # Ajustez selon vos besoins



col1, col2 = st.columns(2)

# Afficher le treemap dans la première colonne
with col1:
    st.plotly_chart(treemap, use_container_width=True)

# Afficher le sunburst dans la deuxième colonne
with col2:
    st.plotly_chart(sunburst, use_container_width=True)

# Exemple de données
annees = pd.DataFrame({'annee_utilisation': pd.date_range(start='2009', end='2019', freq='Y')})

# Ajouter un volet de filtre dans une barre latérale distincte
#sidebar = st.sidebar
#annee_selectionnee = sidebar.slider("Sélectionnez l'année", int(annees['annee_utilisation'].dt.year.min()), int(annees['annee_utilisation'].dt.year.max()), int(annees['annee_utilisation'].dt.year.max()))

st.markdown("###  La population réunionnaise par commune", unsafe_allow_html=True)

# Créer un graphique avec Plotly Express
fig = px.bar(populations, x='nom_de_la_commune', y=['population_totale', 'population_totale'],
             labels={'value': 'Population', 'variable': 'Indicateur'},
             #title=f'Population réunionnaise par commune'
             )

# Afficher le graphique avec Streamlit
st.plotly_chart(fig, use_container_width=True)


###############################################graphique en barre horyzontal

#fig1 = px.bar(populations, x='annee', y='population_totale', orientation='h',
#             labels={'annee': 'Année', 'population_totale': 'Population total'},
#             title=f"Évolution de la population {annee_selectionnee}")

# Inverser l'ordre des barres pour avoir la plus récente en haut
#fig1.update_yaxes(categoryorder='total ascending')

# Afficher le graphique avec Streamlit
#st.plotly_chart(fig1, use_container_width=True)










