import json
from bson import json_util
import pymongo
import re
from adaption import adjust_model
import math
import time
from random import shuffle

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

def update_user_model(user_id, long_model, short_model):
    user_models_collection.find_one_and_update({"user_id": user_id},
                                               {"$set": {"favourite_cuisine": dict(long_model),
                                               "shortterm_favourite_cuisine": dict(short_model)
                                               }})

def fade_one_user(user_model):
  user_id = user_model["user_id"]
  short_term_fav_cuisine = user_model["shortterm_favourite_cuisine"]
  fav_cuisine = user_model["favourite_cuisine"]

  new_short_term_value = 0
  new_long_term_value = 0

  for cuisine in fav_cuisine.keys():
    new_long_term_value = adjust_model.get_faded_value_for_long_term_attribute(fav_cuisine[cuisine])
    if new_long_term_value==0:
      del fav_cuisine[cuisine]
    else:
      fav_cuisine[cuisine] = new_long_term_value

  for cuisine in short_term_fav_cuisine.keys():
    new_short_term_value = adjust_model.get_faded_value_for_short_term_attribute(short_term_fav_cuisine[cuisine])
    if new_short_term_value==0:
      del short_term_fav_cuisine[cuisine]
    else:
      short_term_fav_cuisine[cuisine] = new_short_term_value

  update_user_model(user_id, fav_cuisine, short_term_fav_cuisine)
  return "ok"

def loop_all_users():
  all_users = user_models_collection.find({})
  for user in all_users:
    fade_one_user(user)


if __name__ == '__main__':
  loop_all_users()