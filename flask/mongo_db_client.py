import json
from bson import json_util
import pymongo
import re
import adaption
import math
import time

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
activity_collection = db['activity']
# user_models_collection = db["user-models"]

cuisine_static_list = []
auth_data = {}
with open(r'res/cuisine.json', 'r') as cuisinefile:
    cuisine_static_list = json.load(cuisinefile)

def save_user_details(user, user_model):
    user_collection.insert(user)
    user_models_collection.insert(user_model)

def save_user_model(model):
    user_models_collection.insert(model)
    return "Saved"

def get_user_activity(user_id):
    activity_collection.find({"user_id": user_id})


def save_user_activity(activity):
    activity_collection.insert(activity)

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
    cuisine_list = ['Italian', 'Mexican', 'Chinese', 'American', 'Indian']
    # data = []
    li = []
    #data = recipie_data_collection.find({'attributes.cuisine': [sa]})
    for cuisine in cuisine_list:

        data = list(recipe_collection.aggregate([
            {"$match": {"attributes.cuisine": cuisine}},
            {"$sample": {"size": 7}}
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
    user_short_term_cuisine = user_model['shortterm_favourite_cuisine']
    recommendations = {}
    # allergens = ["Soy", "Butter", "Cheese"]
    allergens = user_model["allergen"]
    cuisine_explore = list(set(cuisine_static_list) - set(user_fav_cuisine.keys()) - set(user_short_term_cuisine.keys()))
    regexes = []
    for item in allergens:
        regexes.append(re.compile(".*" + item + ".*", re.IGNORECASE))
    sumVal = sum(user_fav_cuisine.values())
    sumValShort = sum(user_short_term_cuisine.values())
    reco_fav = []
    reco_short = []
    reco_explore = []
    for cuisine, value in user_fav_cuisine.items():
        if value >= 0:
            reco_fav.extend(list(recipe_collection.aggregate([{"$match":{"attributes.cuisine":cuisine,"ingredientLines": { "$nin": regexes }}},
                    {"$sample":{"size": (int(value)/sumVal) * 30}},
                    { "$project" : { "_id" : 1 , "ingredientLines" : 1, "images":1, "attributes": 1, "name": 1 }}])))
    for cuisine, value in user_short_term_cuisine.items():
        if value >= 0:
            reco_short.extend(list(recipe_collection.aggregate(
            [{"$match": {"attributes.cuisine": cuisine, "ingredientLines": {"$nin": regexes}}},
             {"$sample": {"size": (math.ceil(value) / sumValShort) * 15}},
             {"$project": {"_id": 1, "ingredientLines": 1, "images": 1, "attributes": 1, "name": 1}}])))

    for cuisine in cuisine_explore:
            reco_explore.extend(list(recipe_collection.aggregate(
            [{"$match": {"attributes.cuisine": cuisine}},
             {"$sample": {"size": 5}},
             {"$project": {"_id": 1, "ingredientLines": 1, "images": 1, "attributes": 1, "name": 1}}])))

    res = []
    for elem in reco_fav:
        temp = {}
        temp["cuisine"] = elem["attributes"]["cuisine"][0]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        res.append(temp)
    recommendations["favourite"] = res
    res = []
    for elem in reco_short:
        temp = {}
        temp["cuisine"] = elem["attributes"]["cuisine"][0]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        res.append(temp)
    recommendations["short_favourite"] = res
    res = []
    for elem in reco_explore:
        temp = {}
        temp["cuisine"] = elem["attributes"]["cuisine"][0]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        res.append(temp)
    recommendations["explore_favourite"] = res
    result =json.dumps(recommendations)

    return result


def track_activity(req_data):
    activity_data = req_data
    ts = time.time()
    activity_data["timestamp"] = ts
    user_id = req_data["user_id"]
    action_cusine = req_data["cuisine"]
    action = req_data["action"]
    save_user_activity(activity_data)
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


def get_dashboard(userid):
    user_activity = get_user_activity(userid)
    model = get_user_model(userid)
    res = {}
    res["activity_data"] = []
    if user_activity != None:
        res["activity_data"] = user_activity
    res["favourites"] = model["favourite_cuisine"]
    res["short_term_favourites"] = model["shortterm_favourite_cuisine"]

    return json.dumps(res)



