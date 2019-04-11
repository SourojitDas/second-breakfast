import json
from bson import json_util
import pymongo
import re
import adaption

import os
from config_loader import config

connection = pymongo.MongoClient(config['mongo']['host'],
                     username=config['mongo']['username'],
                     password=config['mongo']['password'],
                     authSource=config['mongo']['authSource'],
                     authMechanism=config['mongo']['authMechanism'])

db = connection[config['mongo']['db']]
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

def update_user_model(user_id, long_model, short_model):
    user_models_collection.findOneAndUpdate({"user_id": id}, {"$set":{"favorite_cuisine": long_model,
                                                                      "shortterm_favourite_cuisine": short_model}})
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
    print(user_model)
    user_fav_cuisine = user_model['favourite_cuisine']
    recommendations = []
    allergens = ["Soy", "Butter", "Cheese"]
    regexes = []
    for item in allergens:
        regexes.append(re.compile(".*" + item + ".*", re.IGNORECASE))
    for cuisine, value in user_fav_cuisine.items():
        recommendations.extend(list(recipe_collection.aggregate([{"$match":{"attributes.cuisine":cuisine,"ingredientLines": { "$nin": regexes }}},
                    {"$sample":{"size": value}},
                    { "$project" : { "_id" : 1 , "ingredientLines" : 1, "images":1, "attributes": 1, "name": 1 }}])))

    res = []
    for elem in recommendations:
        temp = {}
        temp["cuisine"] = elem["attributes"]["cuisine"][0]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        res.append(temp)

    result =json.dumps(res)


    return result


def track_activity(req_data):
    user_id = req_data["user_id"]
    action_cusine = req_data["cuisine"]
    action = req_data["action"]
    user_model = get_user_model(user_id)
    short_term_fav_cuisine = user_model["shortterm_favourite_cuisine"]
    fav_cuisine = user_model["favourite_cuisine"]

    new_short_term_value = 0
    new_long_term_value = 0

    if action_cusine in fav_cuisine.keys():
        if action == 'like':
            new_short_term_value = adaption.get_new_value_for_short_term_attribute('like', fav_cuisine[action_cusine])
            new_long_term_value = adaption.get_new_value_for_long_term_attribute('like', fav_cuisine[action_cusine])
        if action == 'dislike':
            new_short_term_value = adaption.get_new_value_for_short_term_attribute('dislike', fav_cuisine[action_cusine])
            new_long_term_value = adaption.get_new_value_for_long_term_attribute('dislike', fav_cuisine[action_cusine])
        short_term_fav_cuisine[action_cusine] = new_short_term_value
        fav_cuisine[action_cusine] = new_long_term_value
    else:
        if action == 'like':
            new_short_term_value = adaption.get_new_value_for_short_term_attribute('like', 0)
            new_long_term_value = adaption.get_new_value_for_long_term_attribute('like', 0)
        if action == 'dislike':
            new_short_term_value = adaption.get_new_value_for_short_term_attribute('dislike', 0)
            new_long_term_value = adaption.get_new_value_for_long_term_attribute('dislike', 0)
            fav_cuisine[action_cusine] = new_short_term_value
        short_term_fav_cuisine[action_cusine] = new_short_term_value
        fav_cuisine[action_cusine] = new_long_term_value
    update_user_model(user_id, fav_cuisine, short_term_fav_cuisine)
    return "ok"
# action = {
#     image data
# }
# def process_feedback(action):


# get_recommendation("uid01")



