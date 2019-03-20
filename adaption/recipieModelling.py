import json
import pymongo
import os

connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["second-breakfast"]
user_model_collection = db["recipie-model"]
directory_path = r"C:/Users/souro/OneDrive/Desktop/TrialData/"

for r, d, f in os.walk(directory_path):
    for file in f:
        try:

            user = open(directory_path + file, "r")
            user_loaded_data = json.loads(user.read(),encoding='utf-8')
            user_model_collection.insert_one(user_loaded_data)
        except:
            print(file)

# user = open("C:\\Users\\souro\\Downloads\\Yummly28K\\metadata27638\\meta00001.json", "r")
