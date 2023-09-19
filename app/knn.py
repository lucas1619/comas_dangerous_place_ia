from math import radians, cos, sin, asin, sqrt
import dotenv
import os
import requests
import json

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
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
    return json["results"][0]

def knn_result(lat : float, lon : float):
    """
    Returns the k nearest neighbors to the given latitude and longitude
    """
    return {
        "current_location" : call_reverse_geocode(lat, lon),
        "danger_code" : "red"
    }
