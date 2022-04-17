import json
import os
import glob

from manage_modules.GLHLoad import GLHInitialize
from lib.MongoDBSetting import GLHDB

class GLHStore :
    def __init__(self, rootpath) -> None:
        self.rootpath = rootpath
    
    def insert_GLH(self):
        file_list = self.get_file_list(self.rootpath)
        glh_db = GLHDB()

        for file_name in file_list :
            glh_data = self.decode_jsonfile(file_name)
            glh_db.insertmany(glh_data.dict["timelineObjects"])
            print("Loaded:", file_name)

    def decode_jsonfile(self, filename):
        """
        Open a GLH json file, and return decoded and initialized GLH data(:dictionary). "filename" is a GLH json file.
        """
        with open(filename, 'r') as f : 
            dict = json.load(f)

        glhdata = GLHInitialize(dict)
        glhdata.initialize()
        return glhdata
    
    def get_file_list(self):
        years = [2017, 2018, 2019, 2020, 2021]
        filelist = []

        for y in years:
            path = self.rootpath + str(y) + "/*.json"
            filelist.extend(glob.glob(path))
        
        assert len(filelist) > 0, "filelist is None. Check carrent directory: " + os.getcwd()

        return filelist


def store_GLH() :
    rootpath = "./jsondata/"

    glh_store = GLHStore(rootpath)
    glh_store.insert_GLH()

if __name__ == '__main__' :
    
    store_GLH()
    # mongodb command
        # sudo service mongodb start/stop/status




