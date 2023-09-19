import requests
import json
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def search_by_adress(adress):
  url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={adress}&key={GOOGLE_API_KEY}"
  response = requests.get(url)
  data = json.loads(response.text)
  return data

def get_point_google_response(response):
  return (response["geometry"]["location"]["lat"], response["geometry"]["location"]["lng"])

def assign_color(score):
    color = [
        {
            "max": 2,
            "color": "yellow"
        },
        {
            "max": 4,
            "color": "orange"
        },
        {
            "max": 11,
            "color": "red"
        },
    ]
    for item in color:
        if score <= item["max"]:
            return item["color"]
    return "gray"

df = pd.read_excel(r'GEOPORTAL PUNTOS CRITICOS AGOSTO2023 (1) (1).xlsx')
df = df.fillna(0)
df['SUMA_X'] = (df == 'X').sum(axis=1)
df = df[df['DISTRITO'] == 'COMAS']
df = df[["LUGAR", "SUMA_X"]]
puntos = []
for index, row in df.iterrows():
    data = search_by_adress(row["LUGAR"] + " COMAS LIMA")
    if len(data["results"]):
      puntos.append(get_point_google_response(data["results"][0]))
    else:
      puntos.append("a")
df["GEOLOCALIZACION"] = puntos
df = df[df['GEOLOCALIZACION'] != "a"]
df = df.reset_index()
colors = []
for index, row in df.iterrows():
    score = row["SUMA_X"]
    assigned_color = assign_color(score)
    colors.append(assigned_color)
df["COLOR"] = colors
conn = sqlite3.connect('./app/knn.db')
df["GEOLOCALIZACION"] = df["GEOLOCALIZACION"].astype(str)
df.to_sql('puntos', conn, if_exists='replace', index=False)