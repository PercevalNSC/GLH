from flask import Flask, jsonify, request
from flask_cors import CORS
from lib.GLHMongoDB import *

app = Flask(__name__, template_folder="static-node/templates")
app.config["JSON_AS_ASCII"] = False
CORS(app)

# For HTML
@app.route('/')
def home():
    return "Flask server run."

# For GET
@app.route('/post_data', methods = ['POST'])
def check():
    print("data listen")
    if request.method == 'POST':
        data = request.json
        print(data)
    return "receive neko"


# For API
@app.route('/api/json/point/activitySegment.simplifiedRawPath')
def jsonAsSrp():
    return jsonify(GetGLHAssrp().json())
@app.route('/api/json/point/activitySegment.waypointPath')
def jsonAsWp():
    return jsonify(GetGLHAswp().json())
@app.route('/api/json/point/placeVisit.simplifiedRawPath')
def jsonPvSrp():
    return jsonify(GetGLHPvsrp().json())
@app.route('/api/json/point/placeVisit.location')
def jsonPvLoc():
    return jsonify(GetGLHPvloc().json())

@app.route('/api/geojson/point/activitySegment.simplifiedRawPath')
def geojsonAsSrp():
    return jsonify(GetGLHAssrp().geojson())
@app.route('/api/geojson/point/activitySegment.waypointPath')
def geojsonAsWp():
    return jsonify(GetGLHAswp().geojson())
@app.route('/api/geojson/point/placeVisit.simplifiedRawPath')
def geojsonPvSrp():
    return jsonify(GetGLHPvsrp().geojson())
@app.route('/api/geojson/point/placeVisit.location')
def geojsonPvLoc():
    return jsonify(GetGLHPvloc().geojson())

@app.route('/api/geojson/line/route')
def geojsonline():
    return jsonify(route_path())

@app.route('/api/geojson/point/dbscan')
def dbscanPoint():
    eps = 1
    min_samples = 4
    return jsonify(get_dbscan_point(eps, min_samples))
@app.route('/api/geojson/point/dbscan/<float:eps>')
def eps_dbscan_point(eps = 1.0):
    min_samples = 4
    return jsonify(get_dbscan_point(eps, min_samples))
@app.route('/api/geojson/polygon/dbscan')
def dbscan_polygon():
    eps = 1
    min_samples = 4
    return jsonify(get_dbscan_polygon(eps, min_samples))
@app.route('/api/geojson/polygon/dbscan/<float:eps>')
def eps_dbscan_polygon(eps = 1.0):
    min_samples = 4
    return jsonify(get_dbscan_polygon(eps, min_samples))

@app.route('/api/geojson/point/optics')
def optics_point():
    eps = 1
    min_samples = 4
    return jsonify(get_optics_point(eps, min_samples))
@app.route('/api/geojson/point/optics/<float:eps>')
def eps_optics_point(eps = 1.0):
    min_samples = 4
    return jsonify(get_optics_point(eps, min_samples))
@app.route('/api/geojson/polygon/optics')
def optics_polygon():
    eps = 1.0
    min_samples = 4
    return jsonify(get_optics_polygon(eps, min_samples))
@app.route('/api/geojson/polygon/optics/<float:eps>')
def eps_optics_polygon(eps = 1.0):
    min_samples = 4
    return jsonify(get_optics_polygon(eps, min_samples))
@app.route('/api/geojson/viewport')
def view_port():
    center = [139.545, 35.655]
    zoom = 15
    size = [1080, 720]
    return jsonify(get_viewport(center, zoom, *size))

@app.route('/api/get_reachability')
def api_get_reachability():
    return jsonify(get_reachability())


def server_run() :
    app.run(port=8000, debug=True)

if __name__ == "__main__" :
    server_run()

