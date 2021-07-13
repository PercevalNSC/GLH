from flask import Flask, render_template, request, make_response
from pymongo import MongoClient
from CreateList import MakingLatLngList
import json

app = Flask(__name__)

@app.route('/')
def home():
    title = 'Flask Title'
    framework = 'Flask'
    return render_template('index2.html', title=title, framework=framework)

@app.route('/returnjson')
def testpy():
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        test_db = client.glh_db
        test_collection = test_db.glh_clct_1
        corsor = test_collection.find({"activitySegment.simplifiedRawPath": {"$exists": True}},{"activitySegment.simplifiedRawPath": 1})
    list = MakingLatLngList(corsor)
    list.makinglist()
    resultdata = {"length": len(list.latlnglists), "data": list.latlnglists}
    return make_response(json.dumps(resultdata, ensure_ascii=False))

@app.route('/1')
def home1():
    title = request.args.get("title")
    framework = 'Flask'
    okyo = ["色不異空","空不異色","色即是空","空即是色"]
    return render_template('index.html', title=title, framework=framework, okyo=okyo)

@app.route("/1", methods=["post"])
def post():
    title = request.form["name"]
    framework = 'Flask'
    okyo = ["色不異空","空不異色","色即是空","空即是色"]
    return render_template('index.html', title=title, framework=framework, okyo=okyo)

app.run(port=8000, debug=True)