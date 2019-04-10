import json
from bson import json_util
import pymongo
import os
username = "AA"
password = "hayabusa"
connection = pymongo.MongoClient("vm-18-202-35-71.rosettavm.com:27017",
                     username='AA',
                     password='hayabusa',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-256')

db = connection["sophie_dev_1"]
recipe_collection = db['recipes']

def get_recommendation():
    recommendations = []
    data = list(recipe_collection.aggregate([{"$match": {"attributes.cuisine": "Barbecue"}},
                                                         {"$sample": {"size": 10}}]))
    for elem in data:
        recommendations.append(elem)
    print(len(recommendations))




get_recommendation()