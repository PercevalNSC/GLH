from pymongo import MongoClient

if __name__ == '__main__' :
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        glh_db = client.glh_db
        glh_clct = glh_db.glh_clct_2
        corsor = glh_clct.find()

    for i in corsor :
        print(i)