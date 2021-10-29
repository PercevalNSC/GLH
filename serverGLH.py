from flask import Flask, render_template, jsonify
import json
from libraries.MongoDBSetting import MongoDBSet
from libraries.GLH import GLHCollectionAsSrp, GLHCollectionAsWp, GLHCollectionPvSrp, GLHCollectionPvLoc, RoutePath, AllTrajectoryData

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

def storejson(data, name = "dbdata.json"):
    with open(name, "w") as f :
        json.dump(data, f, indent=2,ensure_ascii=False)


@app.route('/')
def home():
    return render_template('GLH.html')

@app.route('/api/json/point/activitySegment.simplifiedRawPath')
def jsonAsSrp():
    collection = GLHCollectionAsSrp(MongoDBSet().asSrpQuery())
    collection.trajectoryList()
    result = collection.exportJson()
    return jsonify(result)
@app.route('/api/json/point/activitySegment.waypointPath')
def jsonAsWp():
    collection = GLHCollectionAsWp(MongoDBSet().asWpQuery())
    collection.trajectoryList()
    result = collection.exportJson()
    return jsonify(result)
@app.route('/api/json/point/placeVisit.simplifiedRawPath')
def jsonPvSrp():
    collection = GLHCollectionPvSrp(MongoDBSet().pvSrpQuery())
    collection.trajectoryList()
    result = collection.exportJson()
    return jsonify(result)
@app.route('/api/json/point/placeVisit.location')
def jsonPvLoc():
    collection = GLHCollectionPvLoc(MongoDBSet().pvLocatinQuery())
    collection.trajectoryList()
    result = collection.exportJson()
    return jsonify(result)

@app.route('/api/geojson/line/route')
def geojsonline():
    routepath = RoutePath(MongoDBSet().query({}))
    routepath.createRoutePath()
    result = routepath.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/dbscan')
def dbscanPoint():
    eps = 0.0001
    min_samples = 4
    as_srp_collection = MongoDBSet().asSrpQuery()
    pv_srp_collection = MongoDBSet().pvSrpQuery()
    std = AllTrajectoryData(as_srp_collection, pv_srp_collection)
    app.logger.debug("Clustering: DBSCAN(eps: " + str(eps) + ", min_samples: " + str(min_samples) + ")" )
    return jsonify(std.dbscan(eps, min_samples))

@app.route('/api/geojson/point/activitySegment.simplifiedRawPath')
def geojsonAsSrp():
    collection = GLHCollectionAsSrp(MongoDBSet().asSrpQuery())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/activitySegment.waypointPath')
def geojsonAsWp():
    collection = GLHCollectionAsWp(MongoDBSet().asWpQuery())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/placeVisit.simplifiedRawPath')
def geojsonPvSrp():
    collection = GLHCollectionPvSrp(MongoDBSet().pvSrpQuery())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/placeVisit.location')
def geojsonPvLoc():
    collection = GLHCollectionPvLoc(MongoDBSet().pvLocatinQuery())
    collection.trajectoryList()
    result = collection.exportGeoJson()
    return jsonify(result)

@app.route('/geocoder')
def geocoderMap():
    return render_template('geocoder.html', title="Flask app", framework="Flask framework")

app.run(port=8000, debug=True)