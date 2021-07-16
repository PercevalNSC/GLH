import json
from os import wait
import GLHload
from pymongo import MongoClient

if __name__ == '__main__' :
    with open('./jsondata/2020/2020_MARCH.json', 'r') as f : 
        dict = json.load(f)

    glhdata = GLHload.GLHinit(dict, 0)
    glhdata.glhinit()

    with MongoClient("mongodb://127.0.0.1:27017") as client:
        glh_db = client.glh_db
        glh_clct = glh_db.glh_clct_2

        glh_clct.insert_many(glhdata.dict["timelineObjects"])

        # glh_clct_1.delete_many({})

        # mongodb command
            # sudo service mongodb start/stop/status




