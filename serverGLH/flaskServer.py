from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import CreateList
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

def mongodbPointRequest(path):
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_2
        corsor = test_collection.find({path: {"$exists": True}})

    if path == "activitySegment.simplifiedRawPath" :
        listObj = CreateList.AsSimplifiedRawPath(corsor)
    elif path == "activitySegment.waypointPath" :
        listObj = CreateList.AsWaypointPath(corsor)
    elif path == "placeVisit.simplifiedRawPath" :
        listObj = CreateList.PvSimplifiedRawPath(corsor)
    elif path == "placeVisit.location" :
        listObj = CreateList.PvLocation(corsor)
    else :
        listObj = CreateList.BaseLngLatList(corsor)

    listObj.makingCollectionList()
    return listObj

def mongodbLineRequest():
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_2
        corsor = test_collection.find()

    routepath = CreateList.RoutePath(corsor)
    routepath.createRoutePath()
    return routepath
    

def storejson(data, name = "dbdata.json"):
    with open(name, "w") as f :
        json.dump(data, f, indent=2,ensure_ascii=False)

@app.route('/')
def home():
    return render_template('GLH.html')

@app.route('/api/json/<path>')
def jsonapi(path):
    listObj = mongodbPointRequest(path)
    resultdata = listObj.jsonBluster()

    #storejson(resultdata)
    return jsonify(resultdata)

@app.route('/api/geojson/line')
def geojsonline():
    routepath = mongodbLineRequest()
    resultdata = routepath.geojsonbluster()

    return jsonify(resultdata)

@app.route('/api/geojson/point/<path>')
def geojsonapi(path):
    listObj = mongodbPointRequest(path)
    resultdata = listObj.geojsonBluster()

    #storejson(resultdata)
    return jsonify(resultdata)


@app.route('/geocoder')
def geocoderMap():
    return render_template('geocoder.html', title="Flask app", framework="Flask framework")

app.run(port=8000, debug=True)