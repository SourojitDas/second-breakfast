import pymongo
import json
import pprint
connection = pymongo.MongoClient("mongodb://localhost:27017")

db = connection["second-breakfast"]
user_models_collection = db["user-models"]


def get_user_model(userid):
    return user_models_collection.find_one({"user_id": userid})


#user_model_object = get_user_model("uid01")
#pprint.pprint(user_model_object)
