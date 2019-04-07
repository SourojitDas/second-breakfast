import json
from bson import json_util
import pymongo
import os

connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["second-breakfast"]
user_collection = db["users"]
user_models_collection = db["user-models"]
business_collection = db['business']
recipe_collection = db['recipe']
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

        data = list(recipe_collection.find({'attributes.cuisine':cuisine}))
        # print(data.count())
        for elem in data:
            temp = {}
            # cur_li = []
            temp["_id"] = elem["_id"]
            temp["img"] = elem["images"]
            temp["name"] = elem["name"]
            # cur_li.append(temp)
            li.append(temp)
    result = json.dumps(li)
    # print(data)
    return result