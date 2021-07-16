from flask import Flask, render_template, request, make_response
from pymongo import MongoClient
from CreateList import MakingLngLatList
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/returnjson')
def returnjson():
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_1
        corsor = test_collection.find({"activitySegment.simplifiedRawPath": {"$exists": True}},{"activitySegment.simplifiedRawPath": 1})
    listObj = MakingLngLatList(corsor)
    resultdata = {"dataType": "AcitivitySegment.simplifiedRawPath", "data": listObj.clctAsSrpList()}
    with open("dbload.json", "w") as f :
        json.dump(resultdata, f, indent=2,ensure_ascii=False)
    return make_response(json.dumps(resultdata, indent=2, ensure_ascii=False))

@app.route('/geocoder')
def geocoderMap():
    title = "Flask app"
    framework = "Flask"
    return render_template('index.html', title=title, framework=framework)

app.run(port=8000, debug=True)