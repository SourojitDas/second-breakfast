from adaption import modelreader
from random import choices
import pprint

recommendation_list = []

model = modelreader.get_user_model("uid01")
user_fav_cuisine = model["favourite_cuisine"]
user_allergen = model["allergen"]
print(user_allergen)
for key, value in user_fav_cuisine.items():
    temp = {}
    temp[key] = value
    print(key)
    data = modelreader.get_recipie_data(key)
    # pprint.pprint(data[0])

    for elem in data:
        for content in elem["ingredientLines"]:
            li = [x.lower() for x in user_allergen]
            allergen_set = set(li)
            content_set = set(content.lower().split())
            if len(allergen_set.intersection(content_set)) > 0:
                break;
            else:
                recommendation_list.append(elem)
                break;
    print(len(recommendation_list))
