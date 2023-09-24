from flask import request, Flask
from flask_api import status
from app.knn import knn_result
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
    
@app.route('/zones', methods=['get'])
def puntos():
    conn = sqlite3.connect('./knn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM puntos")
    names = list(map(lambda x: x[0], c.description))
    zones = c.fetchall()
    zones = list(map(lambda x: dict(zip(names, x)), zones))
    return {
        "zones": zones
    }, status.HTTP_200_OK

if __name__ == '__main__': 
    app.run()

# Esta es la línea que añadimos para que gunicorn pueda encontrar la instancia de Flask
application = app
