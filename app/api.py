import requests
import pandas as pd
import streamlit as st


# @st.cache_data
def fetch_data_from_api(url: str, offset: int, limit: int) -> dict:
    params = {'limit': limit, 'offset': offset}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed API request: Status {response.status_code}")
    

# @st.cache_data
def fetch_all_data(url: str) -> pd.DataFrame:
    all_data = []
    limit = 100
    offset = 0
    total_records = None

    while total_records is None or offset < total_records:
        data = fetch_data_from_api(url, offset, limit)
        all_data.extend(data['results'])

        if total_records is None:
            total_records = data['total_count']
        offset += limit

    return pd.json_normalize(all_data)

# Utilisez la fonction fetch_all_data et gérez les exceptions ou les notifications en dehors de la fonction
try:
    url_api = "https://data.regionreunion.com/api/explore/v2.1/catalog/datasets/population-francaise-communespublic/records"
    population = fetch_all_data(url_api)
except Exception as e:
    print(f"Erreur lors de la récupération des données : {e}")