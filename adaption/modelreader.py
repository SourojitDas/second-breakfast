import pymongo
import json
import pprint
connection = pymongo.MongoClient("mongodb://localhost:27017")

db = connection["second-breakfast"]
user_models_collection = db["user-models"]
recipie_data_collection = db["recipie-model"]

def get_user_model(userid):
    return user_models_collection.find_one({"user_id": userid})

def get_recipie_data(sa):
    data = recipie_data_collection.find({'attributes.cuisine': [sa]})
    print(data.count())
    return data