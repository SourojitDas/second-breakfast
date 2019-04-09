import json
from bson import json_util
import pymongo
import os
username = "AA"
password = "hayabusa"
connection = pymongo.MongoClient("vm-18-203-247-130.rosettavm.com:27017",
                     username='AA',
                     password='hayabusa',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-256')

db = connection["sophie_dev_1"]
user_collection = db["users"]
user_models_collection = db["user-models"]
business_collection = db['business']
recipe_collection = db['recipes']
# user_models_collection = db["user-models"]


def save_user_details(user, user_model):
    user_collection.insert(user)
    user_models_collection.insert(user_model)

def save_user_model(model):
    user_models_collection.insert(model)
    return "Saved"

# def save_business_data():
#     with open('Business.json') as business_json:
#         business_data = json.load(business_json)
#         for elem in business_data:
#             business_collection. insert_one(elem)
#
# def save_recipe_data():
#     with open('Recipie.json') as recipe_json:
#         recipe_data = json.load(recipe_json)
#         for elem in recipe_data:
#             recipe_collection.insert_one(elem)

def get_data_to_set_pref():
    cuisine_list = ['Italian', 'Barbecue', 'French', 'American']
    # data = []
    li = []
    #data = recipie_data_collection.find({'attributes.cuisine': [sa]})
    for cuisine in cuisine_list:

        data = list(recipe_collection.aggregate([
            {"$match": {"attributes.cuisine": cuisine}},
            {"$sample": {"size": 10}}
        ]))

        for elem in data:
            # print(elem)
            temp = {}
            temp["cuisine"] = elem["attributes"]["cuisine"][0]
            temp["_id"] = str(elem["_id"])
            temp["img"] = elem["images"][0]["hostedLargeUrl"]
            temp["name"] = elem["name"]
            li.append(temp)
    result = json.dumps(li)
    # print(data)
    return result


def get_user_model(userid):
    return user_models_collection.find_one({"user_id": userid})

def get_recommendation(user_id):
    user_model = get_user_model(user_id)
    user_fav_cuisine = user_model["favourite_cuisine"]
    recommendations = []
    for cuisine, value in user_fav_cuisine.items():
        recommendations.append(recipe_collection.aggregate({"attributes.cuisine":cuisine}, {"$sample":{"size": value}}))

def track_activity():
    return "ok"
# action = {
#     image data
# }
# def process_feedback(action):






