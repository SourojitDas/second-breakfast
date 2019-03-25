import json
import pymongo

connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["second-breakfast"]
user_model_collection = db["user-models"]

user = open("../user1-model.json", "r")
user_loaded_data = json.loads(user.read())
user_model_collection.insert(user_loaded_data)