from adaption import modelreader
from random import choices
import pprint
recommendation_list = {}
from os import listdir
from os.path import isfile, join
chinesefiles = [f for f in listdir(r"../chinese") if isfile(join(r"../chinese/", f))]
indianfiles = [f for f in listdir(r"../indian") if isfile(join(r"../indian/", f))]
continentalfiles = [f for f in listdir(r"../continental/") if isfile(join(r"../continental/", f))]
print(len(chinesefiles))
print(len(indianfiles))
print(len(continentalfiles))


model = modelreader.get_user_model("uid01")
user_fav_cuisine = model["favourite_cuisine"]
population = []
weight = []
pprint.pprint(user_fav_cuisine)
for key, value in user_fav_cuisine.items():
    population.append(key)
    weight.append(value)

print(population)
print(weight)
for i in range(0, 10):
    print(choices(population, weight))