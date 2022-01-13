from flask import Flask, render_template, jsonify
from GLHMongoDB import *
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# For HTML
@app.route('/')
def home():
    return render_template('GLH.html')
@app.route('/geocoder')
def geocoderMap():
    return render_template('geocoder.html', title="Flask app", framework="Flask framework")
@app.route('/get_center')
def getcentermap():
    return render_template('get_center.html')
@app.route('/reachability')
def reach():
    return render_template("reachabilityplot.html")
@app.route('/map')
def map():
    return render_template("map.html")

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


# test
@app.route('/hello/<name>')
def hello(name = None):
    print(name)
    return name

app.run(port=8000, debug=True)