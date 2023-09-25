from math import radians, cos, sin, asin, sqrt
import dotenv
import os
import sqlite3
import requests
from zone import Zone

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def haversine(zone1: Zone, zone2: Zone):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1 = zone1.geolocalizacion[1:-1].split(",")
    lon2, lat2 = zone2.geolocalizacion[1:-1].split(",")
    lon1, lat1 = float(lon1), float(lat1)
    lon2, lat2 = float(lon2), float(lat2)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000
    return c * r

def call_reverse_geocode(lat : float, lon : float):
    """
    Calls the reverse geocoding API to get the address of the given latitude and longitude
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}&language=es"
    response = requests.get(url)
    json = response.json()
    if len(json["results"]) == 0:
        return {
            "error" : "No se encontró la dirección"
        }
    return json["results"][0]

def knn(lat : float, lon : float, k : int):
    """
    Returns the k nearest neighbors to the given latitude and longitude
    """
    location = call_reverse_geocode(lat, lon)
    if "error" in location:
        raise Exception(location["error"])
    
    conn = sqlite3.connect('./knn.db')
    new_zone = Zone(color="-", geolocalizacion=f"({lat}, {lon})", lugar=location["formatted_address"])
    c = conn.cursor()
    c.execute("SELECT * FROM puntos")
    names = list(map(lambda x: x[0], c.description))
    zones = c.fetchall()
    zones = list(map(lambda x: dict(zip(names, x)), zones))

    zones2 = []
    for zone in zones:
        zone : Zone = Zone(color=zone["COLOR"], geolocalizacion=zone["GEOLOCALIZACION"], lugar=zone["LUGAR"], suma_x=zone["SUMA_X"], index=zone["index"])
        zones2.append({
            "zone" : zone,
            "distance" : haversine(zone, new_zone),
        })
    conn.close()
    zones2 = list(filter(lambda x: x["distance"] <= 1500, zones2))
    zones2.sort(key=lambda x: x["distance"])
    zones2 = zones2[:k]

    if len(zones2) == 0:
        return {
            "current_location" : location,
            "danger_code" : "gray",
        }
    
    colors = {}
    for zone in zones2:
        colors[zone["zone"].color] = colors.get(zone["zone"].color, 0) + 1
    colors = list(colors.items())
    colors.sort(key=lambda x: x[1])
    colors.reverse()
    colors = colors[0][0]

    return {
        "current_location" : location,
        "danger_code" : colors,
    }

def knn_result(lat : float, lon : float):
    """
    Returns the k nearest neighbors to the given latitude and longitude
    """
    return knn(lat, lon, 4)
