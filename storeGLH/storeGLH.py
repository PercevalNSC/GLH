import json
from os import wait
import GLHload
from pymongo import MongoClient

if __name__ == '__main__' :
    with open('2018_APRIL.json', 'r') as f : 
        dict = json.load(f)

    glhdata = GLHload.GLHinit(dict, 0)
    glhdata.glhinit()

    with MongoClient("mongodb://127.0.0.1:27017") as client:
        glh_db = client.glh_db
        glh_clct_1 = glh_db.glh_clct_1

        glh_clct_1.insert_many(glhdata.dict["timelineObjects"])

        # glh_clct_1.delete_many({})

        # mongodb command
            # sudo service mongodb start/stop/status




