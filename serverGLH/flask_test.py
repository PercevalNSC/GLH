from threading import Condition
from flask import Flask, render_template, request, make_response
from pymongo import MongoClient
from CreateList import AsSimplifiedRawPath, AsWaypointPath, PvSimplifiedRawPath, BaseLngLatList
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/api/<path>')
def serveapi(path):

    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_2
        corsor = test_collection.find({path: {"$exists": True}},{path: 1})

    if path == "activitySegment.simplifiedRawPath" :
        listObj = AsSimplifiedRawPath(corsor)
    elif path == "activitySegment.waypointPath" :
        listObj = AsWaypointPath(corsor)
    elif path == "placeVisit.simplifiedRawPath" :
        listObj = PvSimplifiedRawPath(corsor)
    else :
        path = "unexpected query: " + path
        listObj = BaseLngLatList(corsor)
    listObj.makingFieldList()
    resultdata = {"dataType": path, "data": listObj.lnglatlist}

    #with open("dbload.json", "w") as f :
        #json.dump(resultdata, f, indent=2,ensure_ascii=False)
        
    return make_response(json.dumps(resultdata, indent=2, ensure_ascii=False))

@app.route('/geocoder')
def geocoderMap():
    title = "Flask app"
    framework = "Flask"
    return render_template('index.html', title=title, framework=framework)

@app.route('/<name>')
def test(name):
    return name

app.run(port=8000, debug=True)