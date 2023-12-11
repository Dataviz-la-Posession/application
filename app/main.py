import streamlit as st
import pandas as pd
import numpy as np
from api import population
from api import conso_nrj
import plotly.express as px
import random  # Ajout de l'importation du module random
#import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Configurer la page pour utiliser une mise en page en pleine largeur
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .reportview-container .markdown-text-container {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center'>Evolution de la population et de la consommmation élèctrique dans les collectivités territoriales</h1>", unsafe_allow_html=True)

# Obtenez les années uniques dans les données
annees = population['annee_utilisation'].astype(str).unique()
annees.sort()  # Assurez-vous que les années sont dans l'ordre

annee_conso = conso_nrj['annee'].astype(str).unique()
annee_conso.sort() 

# Fusionnez les années uniques tout en maintenant l'ordre
annees = np.union1d(annees, annee_conso)


# Créer un curseur pour sélectionner l'année
annee_selectionnee = st.slider("Sélectionnez l'année", int(annees.min()), int(annees.max()), int(annees.max()))
annee_selectionnee_str = str(annee_selectionnee)
population_filtree = population[population['annee_utilisation'] == annee_selectionnee_str]


#annee n-1
annee_n_1 = annee_selectionnee - 1
annee_selectionnee_str_n_1 = str(annee_n_1)
population_filtree_n_1 = population[population['annee_utilisation'] == annee_selectionnee_str_n_1]

#annee n-2
annee_n_2 = annee_selectionnee - 2
annee_selectionnee_str_n_2 = str(annee_n_2)
population_filtree_n_2 = population[population['annee_utilisation'] == annee_selectionnee_str_n_2]


#indicateur kpi population total
# Calculer votre indicateur KPI (par exemple, la somme de la population)
kpi_value = population_filtree['population_totale'].sum()
kpi_value_n1 = population_filtree_n_1['population_totale'].sum()
if kpi_value_n1 == 0:
    kpi_value_n1 = "donnée manquante"
kpi_value_n2 = population_filtree_n_2['population_totale'].sum()
if kpi_value_n2 == 0:
    kpi_value_n2 = "donnée manquante"

kpi_conso_edf = conso_nrj['consommation_mwh'].sum()

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
    st.subheader(f"Population en {annee_n_2}")
    #st.info("Ceci est le nombre démographique pour l'année sélectionnée.")
    
    # Utiliser des balises HTML pour ajuster la taille de police
    st.markdown(f"<p style='font-size:48px; font-weight:bold'>{kpi_value_n2}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:24px; font-weight:bold'>{kpi_conso_edf} mwh</p>", unsafe_allow_html=True)

#col2.markdown(f"### Population en {annee_n_1}: {kpi_value_n1}")
with col2.container():
    st.subheader(f"Population en {annee_n_1}")
    #st.info("Ceci est le nombre démographique pour l'année sélectionnée.")
    
    # Utiliser des balises HTML pour ajuster la taille de police
    st.markdown(f"<p style='font-size:48px; font-weight:bold'>{kpi_value_n1}</p>", unsafe_allow_html=True)


#col3.markdown(f"### Population en {annee_selectionnee}: {kpi_value}")
# Afficher l'indicateur KPI pour l'année précédente dans la deuxième colonne
with col3.container():
    st.subheader(f"Population en {annee_selectionnee}")
    #st.info("Ceci est le nombre démographique pour l'année sélectionnée.")
    
    # Utiliser des balises HTML pour ajuster la taille de police
    st.markdown(f"<p style='font-size:48px; font-weight:bold'>{kpi_value}</p>", unsafe_allow_html=True)




# Ajouter un séparateur (ligne horizontale)
# Ajouter une ligne horizontale (séparateur)
#st.markdown('<hr>', unsafe_allow_html=True)
# Créer une ligne horizontale personnalisée comme séparateur
st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)


st.markdown("### Répartition de la population :", unsafe_allow_html=True)
# Création de la treemap
treemap = px.treemap(population_filtree,
                     path=["code_arrondissement", "nom_de_la_commune"],
                     values="population_totale",
                     custom_data=["population_totale"])

# Ajouter des annotations pour chaque case du treemap
for trace in treemap.data:
    trace.text = trace.customdata[0]
    trace.textposition = 'middle center'
    trace.textfont = {'color':'white', 'size':15, 'family':"Arial, bold"}



sunburst = px.sunburst(population_filtree,
                  path=["code_arrondissement", "nom_de_la_commune"],
                  values="population_totale",
                  custom_data=["population_totale"])

# Ajouter et personnaliser les annotations pour chaque section du sunburst
for trace in sunburst.data:
    trace.text = trace.customdata[0]
    trace.textfont = {'color':'white', 'size':12, 'family':"Arial, bold"}  # Ajustez selon vos besoins


# Utilisation des onglets avec des colonnes pour centrer le contenu
#tab1, tab2 = st.tabs(["Répartition de la Population", "Détail par Commune"])


#with tab1:
#st.plotly_chart(treemap, use_container_width=True)

#with tab2:
#st.plotly_chart(sunburst, use_container_width=True)
col1, col2 = st.columns(2)

# Afficher le treemap dans la première colonne
with col1:
    st.plotly_chart(treemap, use_container_width=True)

# Afficher le sunburst dans la deuxième colonne
with col2:
    st.plotly_chart(sunburst, use_container_width=True)


# Diviser l'espace en deux colonnes pour la nouvelle ligne
#col3, col4 = st.columns(2)

# Ajouter du contenu dans la première colonne de la nouvelle ligne
#with col3:
#    st.write("Contenu de la colonne 1 de la nouvelle ligne")

# Ajouter du contenu dans la deuxième colonne de la nouvelle ligne
#with col4:
#    st.write("Contenu de la colonne 2 de la nouvelle ligne")




# Exemple de données
annees = pd.DataFrame({'annee_utilisation': pd.date_range(start='2009', end='2019', freq='Y')})

# Ajouter un volet de filtre dans une barre latérale distincte
sidebar = st.sidebar
annee_selectionnee = sidebar.slider("Sélectionnez l'année", int(annees['annee_utilisation'].dt.year.min()), int(annees['annee_utilisation'].dt.year.max()), int(annees['annee_utilisation'].dt.year.max()))

# Afficher seulement le filtre
#st.write(f"Année sélectionnée : {annee_selectionnee}")

# Afficher la population filtrée (ou d'autres contenus si nécessaire)
#population_filtree = annees[annees['annee_utilisation'].dt.year == annee_selectionnee]
#st.write(population_filtree)



annee_selectionner = sidebar.selectbox("Sélectionnez l'année", annees['annee_utilisation'].dt.year.unique())




# Afficher deux graphiques pour les indicateurs barre horyzonta
#st.subheader("Année N")
#st.metric("Population", kpi_value)

#st.subheader("Année N-1")
#st.metric("Population", kpi_value * 2)

# Créer un graphique avec Plotly Express
fig = px.bar(population_filtree, x='nom_de_la_commune', y=['population_totale', 'population_totale'],
             labels={'value': 'Population', 'variable': 'Indicateur'},
             title=f'Indicateurs superposés pour {annee_selectionnee}')

# Afficher le graphique avec Streamlit
st.plotly_chart(fig, use_container_width=True)


###############################################graphique en barre horyzontal

fig1 = px.bar(population_filtree, x='population_totale', y='nom_de_la_commune', orientation='h',
             labels={'population_totale': 'Population Totale', 'nom_de_la_commune': 'Nom de la Commune'},
             title=f"Évolution de la population en {annee_selectionnee}")

# Inverser l'ordre des barres pour avoir la plus récente en haut
fig1.update_yaxes(categoryorder='total ascending')

# Afficher le graphique avec Streamlit
st.plotly_chart(fig1, use_container_width=True)

