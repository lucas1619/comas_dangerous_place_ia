from flask import request, Flask
from flask_api import status
from knn import knn_result, call_reverse_geocode
from zone import Zone
import sqlite3


app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/classify', methods=['GET'])
def classify():
    try:
        args = request.args
        lat, lon = args['lat'], args['lon']
        lat, lon = float(lat), float(lon)
        return knn_result(lat, lon), status.HTTP_200_OK
    except KeyError:
        return {
            "error" : "lat and lon are required"
        }, status.HTTP_412_PRECONDITION_FAILED
    except ValueError:
        return {
            "error" : "lat and lon must be floats"
        }, status.HTTP_412_PRECONDITION_FAILED
    except Exception as e:
        return {
            "error" : str(e)
        }, status.HTTP_412_PRECONDITION_FAILED
    
@app.route('/zones', methods=['GET'])
def puntos():
    conn = sqlite3.connect('./knn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM puntos")
    names = list(map(lambda x: x[0], c.description))
    zones = c.fetchall()
    zones = list(map(lambda x: dict(zip(names, x)), zones))
    
    n = len(zones)
    for i in range(n):
        geolocation = zones[i]['GEOLOCALIZACION']
        geolocation = geolocation[1:-1].split(',')
        lat, lon = geolocation[0], geolocation[1]
        zones[i]['latitud'] = lat
        zones[i]['longitud'] = lon

    return {
        "zones": zones
    }, status.HTTP_200_OK

@app.route('/zones', methods=['POST'])
def create_puntos():
    try:
        conn = sqlite3.connect('./knn.db')
        args = request.args
        color, lat, lon = args['color'], args['lat'], args['lon']
        color, lat, lon = str(color), float(lat), float(lon)
        location = call_reverse_geocode(lat, lon)
        lugar = location['formatted_address']
        zone = Zone(color, f"({lat}, {lon})", lugar)
        zone.save_to_db(conn)
        return {
            "zones": dict(zone)
        }, status.HTTP_200_OK
    except KeyError:
        return {
            "error" : "color, geolocalizacion, lugar, are required"
        }, status.HTTP_412_PRECONDITION_FAILED
    except ValueError:
        return {
            "error" : "lat and lon must be floats"
        }, status.HTTP_412_PRECONDITION_FAILED 
    except Exception as e:
        return {
            "error" : str(e)
        }, status.HTTP_412_PRECONDITION_FAILED

if __name__ == '__main__': 
    app.run()

# Esta es la línea que añadimos para que gunicorn pueda encontrar la instancia de Flask
application = app
