from flask import Flask, render_template, jsonify
from Setting.MongoDBSetting import MongoDBSet
from GLH import GLH
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route('/')
def home():
    """
    root neko
    """
    return render_template('GLH.html')


@app.route('/api/json/point/activitySegment.simplifiedRawPath')
def jsonAsSrp():
    collection = GLH.GLHCollectionAsSrp(MongoDBSet().assrp_query())
    collection.trajectoryList()
    return jsonify(collection.exportJson())
@app.route('/api/json/point/activitySegment.waypointPath')
def jsonAsWp():
    collection = GLH.GLHCollectionAsWp(MongoDBSet().aswp_query())
    collection.trajectoryList()
    return jsonify(collection.exportJson())
@app.route('/api/json/point/placeVisit.simplifiedRawPath')
def jsonPvSrp():
    collection = GLH.GLHCollectionPvSrp(MongoDBSet().pvsrp_query())
    collection.trajectoryList()
    return jsonify(collection.exportJson())
@app.route('/api/json/point/placeVisit.location')
def jsonPvLoc():
    collection = GLH.GLHCollectionPvLoc(MongoDBSet().pvlocation_query())
    collection.trajectoryList()
    return jsonify(collection.exportJson())

@app.route('/api/geojson/line/route')
def geojsonline():
    routepath = GLH.RoutePath(MongoDBSet().query({}))
    routepath.createRoutePath()
    return jsonify(routepath.exportGeoJson())
@app.route('/api/geojson/point/dbscan')
def dbscanPoint():
    eps = 0.001
    min_samples = 4
    as_srp_collection = MongoDBSet().assrp_query()
    pv_srp_collection = MongoDBSet().pvsrp_query()
    std = GLH.AllTrajectoryData(as_srp_collection, pv_srp_collection)
    return jsonify(std.dbscan(eps, min_samples))

@app.route('/api/geojson/point/activitySegment.simplifiedRawPath')
def geojsonAsSrp():
    collection = GLH.GLHCollectionAsSrp(MongoDBSet().assrp_query())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/activitySegment.waypointPath')
def geojsonAsWp():
    collection = GLH.GLHCollectionAsWp(MongoDBSet().aswp_query())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/placeVisit.simplifiedRawPath')
def geojsonPvSrp():
    collection = GLH.GLHCollectionPvSrp(MongoDBSet().pvsrp_query())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/placeVisit.location')
def geojsonPvLoc():
    collection = GLH.GLHCollectionPvLoc(MongoDBSet().pvlocation_query())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)

@app.route('/geocoder')
def geocoderMap():
    return render_template('geocoder.html', title="Flask app", framework="Flask framework")

app.run(port=8000, debug=True)