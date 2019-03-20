import json
import pymongo
import os

connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["second-breakfast"]
user_model_collection = db["recipe-models"]

destdir = 'directory of dataset'

files = [f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f))]
print(files)
for f in files:
    user = open(destdir+f, "r")
    print(user)
    user_loaded_data = json.loads(user.read(), encoding='UTF8')
    user_model_collection.insert_one(user_loaded_data)