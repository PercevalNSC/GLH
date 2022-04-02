import json
import os
import glob
from pymongo import MongoClient

import manage_modules.GLHload as GLHload
from GLHMongoDB import OPTICSConstruct
from GLH.Clustering import OPTICSTrajectoryData
from Setting.MongoDBSetting import GLHDB


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
            print(filename)
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

# streamingで集計していけるようにするのが理想

def store() :
    rootpath = "./jsondata/"

    filelist = getjsondata(rootpath)
    assert len(filelist) > 0, "filelist is None. Check carrent directory: " + os.getcwd()

    insertGLH(filelist)

def init_clustering() :
    min_samples = 4

    construct = OPTICSConstruct(min_samples)
    optics_trajectory_data : OPTICSTrajectoryData = construct.clustering_obj.clustering
    mongodb = GLHDB("glh_reach", "data2")

    optics_array = optics_trajectory_data.create_optics_arrays()
    optics_array.status()
    dicted_data = optics_array.to_dict_list()
    #print(dicted_data)
    mongodb.insertmany(dicted_data)

if __name__ == '__main__' :
    
    store()
    # mongodb command
        # sudo service mongodb start/stop/status




