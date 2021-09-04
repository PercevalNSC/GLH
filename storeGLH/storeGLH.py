import json
import os
import glob
import GLHload
from pymongo import MongoClient

# fileを開いて初期化したオブジェクトを返す
def jsonOpen(filename):
    with open(filename, 'r') as f : 
        dict = json.load(f)

    glhdata = GLHload.GLHinit(dict, 0)
    glhdata.glhinit()
    return glhdata

# ファイル名のリストからファイルを開いてMongoDBへ格納
def insertGLH(filelist):

    with MongoClient("mongodb://127.0.0.1:27017") as client:
        glh_db = client.glh_db

        glh_clct = glh_db.glh_clct_full
        glh_clct.delete_many({})

        for filename in filelist :
            glhdata = jsonOpen(filename)
            glh_clct.insert_many(glhdata.dict["timelineObjects"])
            print("loaded: " + filename)

# rootpath以下の月別GLHjsonファイル名のリストを返す
def getjsondata(rootpath):
    years = [2017, 2018, 2019, 2020, 2021]
    filelist = []

    for y in years:
        path = rootpath + str(y) + "/*.json"
        filelist.extend(glob.glob(path))

    return filelist

if __name__ == '__main__' :
    
    rootpath = "./jsondata/"

    filelist = getjsondata(rootpath)
    assert len(filelist) > 0, "filelist is None. Check carrent directory: " + os.getcwd()
    insertGLH(filelist)

    # mongodb command
        # sudo service mongodb start/stop/status




