from flask import Flask, render_template, jsonify
import json
from libraries.MongoDBSetting import MongoDBSet
import libraries.GLH as GLH

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

def storejson(data, name = "dbdata.json"):
    with open(name, "w") as f :
        json.dump(data, f, indent=2,ensure_ascii=False)


@app.route('/')
def home():
    return render_template('GLH.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("img/favicon.ico")

@app.route('/api/json/point/activitySegment.simplifiedRawPath')
def jsonAsSrp():
    collection = GLH.GLHCollectionAsSrp(MongoDBSet().asSrpQuery())
    collection.trajectlyList()
    result = collection.exportJson()
    return jsonify(result)
@app.route('/api/json/point/activitySegment.waypointPath')
def jsonAsWp():
    collection = GLH.GLHCollectionAsWp(MongoDBSet().asWpQuery())
    collection.trajectlyList()
    result = collection.exportJson()
    return jsonify(result)
@app.route('/api/json/point/placeVisit.simplifiedRawPath')
def jsonPvSrp():
    collection = GLH.GLHCollectionPvSrp(MongoDBSet().pvSrpQuery())
    collection.trajectlyList()
    result = collection.exportJson()
    return jsonify(result)
@app.route('/api/json/point/placeVisit.location')
def jsonPvLoc():
    collection = GLH.GLHCollectionPvLoc(MongoDBSet().pvLocatinQuery())
    collection.trajectlyList()
    result = collection.exportJson()
    return jsonify(result)

@app.route('/api/geojson/line')
def geojsonline():
    routepath = GLH.RoutePath(MongoDBSet().query({}))
    routepath.createRoutePath()
    result = routepath.exportGeoJson()
    return jsonify(result)

@app.route('/api/geojson/point/activitySegment.simplifiedRawPath')
def geojsonAsSrp():
    collection = GLH.GLHCollectionAsSrp(MongoDBSet().asSrpQuery())
    collection.trajectlyList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/activitySegment.waypointPath')
def geojsonAsWp():
    collection = GLH.GLHCollectionAsWp(MongoDBSet().asWpQuery())
    collection.trajectlyList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/placeVisit.simplifiedRawPath')
def geojsonPvSrp():
    collection = GLH.GLHCollectionPvSrp(MongoDBSet().pvSrpQuery())
    collection.trajectlyList()
    result = collection.exportGeoJson()
    return jsonify(result)
@app.route('/api/geojson/point/placeVisit.location')
def geojsonPvLoc():
    collection = GLH.GLHCollectionPvLoc(MongoDBSet().pvLocatinQuery())
    collection.trajectlyList()
    result = collection.exportGeoJson()
    return jsonify(result)

@app.route('/geocoder')
def geocoderMap():
    return render_template('geocoder.html', title="Flask app", framework="Flask framework")

app.run(port=8000, debug=True)