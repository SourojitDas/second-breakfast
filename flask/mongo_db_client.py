import json
from bson import json_util
import pymongo
import re
from adaption import adjust_model
import math
import time
from random import shuffle
from pymongo import ReturnDocument
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
    insertion_result = user_models_collection.insert_one(model)
    inserted_id = insertion_result.inserted_id
    new_user = user_models_collection.find_one({'_id': inserted_id})
    del new_user["_id"]
    return dict(new_user)

def get_user_activity(user_id):
    return list(activity_collection.find({"user_id": user_id}, {"_id": 0}))

def save_user_activity(activity):
    activity_collection.insert(activity)

def update_user_model(user_id, long_model, short_model):
    user_models_collection.find_one_and_update({"user_id": user_id},
                                               {"$set": {"favourite_cuisine": dict(long_model),
                                               "shortterm_favourite_cuisine": dict(short_model)
                                               }})
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
    # result = json.dumps(li)
    # print(data)
    return li


def get_user_model(userid):
    return user_models_collection.find_one({"user_id": userid})

def get_recommendation(user_id):
    user_model = get_user_model(user_id)
    # print(user_model)
    user_fav_cuisine = user_model['favourite_cuisine']
    user_short_term_cuisine = user_model['shortterm_favourite_cuisine']
    recommendations = []
    # allergens = ["Soy", "Butter", "Cheese"]
    allergens = user_model["allergen"]
    cuisine_explore = list(set(cuisine_static_list) - set(user_fav_cuisine.keys()) - set(user_short_term_cuisine.keys()))
    regexes = []
    for item in allergens:
        regexes.append(re.compile(".*" + item + ".*", re.IGNORECASE))
    sumVal = sum([x for x in user_fav_cuisine.values() if x > 0])
    sumValShort = sum([x for x in user_short_term_cuisine.values() if x > 0])
    reco_fav = []
    reco_short = []
    reco_explore = []
    for cuisine, value in user_fav_cuisine.items():
        if value > 0:
            reco_fav.extend(list(recipe_collection.aggregate([{"$match":{"attributes.cuisine":cuisine,"ingredientLines": { "$nin": regexes }}},
                    {"$sample":{"size": ((int(value)/sumVal) * 100)}},
                    { "$project" : { "_id" : 1 , "ingredientLines" : 1, "images":1, "attributes": 1, "name": 1 }}])))
    for cuisine, value in user_short_term_cuisine.items():
        if value > 0:
            reco_short.extend(list(recipe_collection.aggregate(
            [{"$match": {"attributes.cuisine": cuisine, "ingredientLines": {"$nin": regexes}}},
             {"$sample": {"size": (math.ceil(value) / sumValShort) * 50}},
             {"$project": {"_id": 1, "ingredientLines": 1, "images": 1, "attributes": 1, "name": 1}}])))

    # for cuisine in cuisine_explore:
    reco_explore.extend(list(recipe_collection.aggregate(
        [{"$match": {"attributes.cuisine": {'$in': cuisine_explore}}},
        {"$sample": {"size": 20}},
        {"$project": {"_id": 1, "ingredientLines": 1, "images": 1, "attributes": 1, "name": 1}}])))

    res = {}
    for elem in reco_fav:
        temp = {}
        temp["cuisine"] = list(set(user_fav_cuisine.keys()).intersection(
            set(elem["attributes"]["cuisine"])))[0]
        temp["cuisines"] = elem["attributes"]["cuisine"]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        temp["reasoning"] = "This item is shown to you based on your likes and dislikes"
        res[elem["name"]] = temp
        # res[str(elem["_id"])] = temp
    
    recommendations = recommendations + list(res.values())[0:28]
    res = {}
    for elem in reco_short:
        temp = {}
        temp["cuisine"] = list(set(user_short_term_cuisine).intersection(
            set(elem["attributes"]["cuisine"])))[0]
        temp["cuisines"] = elem["attributes"]["cuisine"]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        temp["reasoning"] = "This item is shown to you based on your current mood"
        res[elem["name"]] = temp
        # res[str(elem["_id"])] = temp

    recommendations = recommendations + list(res.values())[0:23]
    res = {}
    for elem in reco_explore:
        temp = {}
        temp["cuisine"] = list(set(cuisine_explore).intersection(
            set(elem["attributes"]["cuisine"])))[0]
        temp["cuisines"] =elem["attributes"]["cuisine"]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        temp["reasoning"] = "This item is shown to you to help you explore"
        res[elem["name"]] = temp
        # res[str(elem["_id"])] = temp
    recommendations = recommendations + list(res.values())[0:5]
    shuffle(recommendations)
    # result =json.dumps(recommendations)

    return recommendations[0:48]

def get_explorations(user_id):
    user_model = get_user_model(user_id)
    # print(user_model)
    user_fav_cuisine = user_model['favourite_cuisine']
    user_short_term_cuisine = user_model['shortterm_favourite_cuisine']
    recommendations = []
    # allergens = ["Soy", "Butter", "Cheese"]
    allergens = user_model["allergen"]
    cuisine_explore = list(set(cuisine_static_list) - set(user_fav_cuisine.keys()) - set(user_short_term_cuisine.keys()))
    for cuisine in user_fav_cuisine:
        if cuisine in user_model['favourite_cuisine'] and user_model['favourite_cuisine'][cuisine] < 1:
            cuisine_explore.append(cuisine)
    for cuisine in user_short_term_cuisine:
        if cuisine in user_model['shortterm_favourite_cuisine'] and user_model['shortterm_favourite_cuisine'][cuisine] < 1:
            cuisine_explore.append(cuisine)
    regexes = []
    for item in allergens:
        regexes.append(re.compile(".*" + item + ".*", re.IGNORECASE))
    sumVal = sum(user_fav_cuisine.values())
    sumValShort = sum(user_short_term_cuisine.values())
    reco_fav = []
    reco_short = []
    reco_explore = []
    for cuisine in cuisine_explore:
            reco_explore.extend(list(recipe_collection.aggregate(
            [{"$match": {"attributes.cuisine": cuisine}},
             {"$sample": {"size": 48}},
             {"$project": {"_id": 1, "ingredientLines": 1, "images": 1, "attributes": 1, "name": 1}}])))

    res = []
    for elem in reco_explore:
        temp = {}

        temp["cuisine"] = elem["attributes"]["cuisine"][0]
        temp["_id"] = str(elem["_id"])
        temp["img"] = elem["images"][0]["hostedLargeUrl"]
        temp["name"] = elem["name"]
        temp["reasoning"] = "This item is shown to you to help you explore"
        res.append(temp)
    recommendations = recommendations + res
    shuffle(recommendations)
    # result =json.dumps(recommendations)

    return recommendations

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
        new_long_term_value = adjust_model.get_new_value_for_long_term_attribute(action, fav_cuisine[action_cusine])
    else:
        new_long_term_value = adjust_model.get_new_value_for_long_term_attribute(action, 0)

    if action_cusine in short_term_fav_cuisine.keys():
        new_short_term_value = adjust_model.get_new_value_for_short_term_attribute(
            action, short_term_fav_cuisine[action_cusine])
    else:
        new_short_term_value = adjust_model.get_new_value_for_short_term_attribute(
            action, 0)

    if action_cusine in short_term_fav_cuisine.keys() and new_short_term_value <= 0:
        del short_term_fav_cuisine[action_cusine]
    else:
        short_term_fav_cuisine[action_cusine] = new_short_term_value

    if action_cusine in fav_cuisine.keys() and new_long_term_value <= 0:
        del fav_cuisine[action_cusine]
    else:
        fav_cuisine[action_cusine] = new_long_term_value

    update_user_model(user_id, fav_cuisine, short_term_fav_cuisine)
    return "ok"

def modify_long_term_model(user_id, long_model):
    long_model_modified = {}
    for i in long_model:
        if float(long_model[i]) > 0:
            long_model_modified[i] =  float(long_model[i])
    new_user_model = user_models_collection.find_one_and_update({"user_id": user_id},
                                               {"$set": {"favourite_cuisine": dict(long_model_modified)}},
                                               return_document=ReturnDocument.AFTER)
    del new_user_model['_id']
    # print(new_user_model)
    return new_user_model

def get_dashboard(userid):
    user_activity = get_user_activity(userid)
    model = get_user_model(userid)
    res = {}
    res["allergen"] = model["allergen"]
    res["activity_data"] = []
    if user_activity != None:
        res["activity_data"] = user_activity
    res["favourites"] = model["favourite_cuisine"]
    res["short_term_favourites"] = model["shortterm_favourite_cuisine"]
    # print(res)
    # return json.dumps(res)
    return res



