from flask import Flask, render_template, make_response
from pymongo import MongoClient
import CreateList
import json

app = Flask(__name__)

def mongodbRequest(path):
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_2
        corsor = test_collection.find({path: {"$exists": True}},{path: 1})

    if path == "activitySegment.simplifiedRawPath" :
        listObj = CreateList.AsSimplifiedRawPath(corsor)
    elif path == "activitySegment.waypointPath" :
        listObj = CreateList.AsWaypointPath(corsor)
    elif path == "placeVisit.simplifiedRawPath" :
        listObj = CreateList.PvSimplifiedRawPath(corsor)
    elif path == "placeVisit.location" :
        listObj = CreateList.PvCoordinate(corsor)
    else :
        listObj = CreateList.BaseLngLatList(corsor)

    listObj.makingFieldList()
    return listObj

def storejson(data, name = "dbdata.json"):
    with open(name, "w") as f :
        json.dump(data, f, indent=2,ensure_ascii=False)

@app.route('/')
def home():
    return render_template('GLH.html')

@app.route('/api/json/<path>')
def jsonapi(path):
    listObj = mongodbRequest(path)
    resultdata = listObj.jsonBluster()

    #storejson(resultdata)
        
    return make_response(json.dumps(resultdata, indent=2, ensure_ascii=False))

@app.route('/api/geojson/<path>')
def geojsonapi(path):
    listObj = mongodbRequest(path)
    resultdata = listObj.geojsonBluster()

    #storejson(resultdata)
        
    return make_response(json.dumps(resultdata, indent=2, ensure_ascii=False))


@app.route('/geocoder')
def geocoderMap():
    title = "Flask app"
    framework = "Flask"
    return render_template('geocoder.html', title=title, framework=framework)


app.run(port=8000, debug=True)