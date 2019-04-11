#!/usr/bin/env python3

from flask import Flask, request
from flask_cors import CORS
import mongo_db_client
import json

app = Flask(__name__)
CORS(app)

def send_json_response(result):
    return app.response_class(
        response=json.dumps(result),
        mimetype='application/json'
    )

@app.route("/second-breakfast/show-recipe/")
def show_recipe():
    return send_json_response(mongo_db_client.get_data_to_set_pref())

@app.route("/second-breakfast/save_user_model/", methods=['POST'])
def save_new_user_model():
    req_data = request.get_json()
    return send_json_response(mongo_db_client.save_user_model(req_data))

@app.route("/second-breakfast/activity", methods=['POST'])
def submit_activity():
    req_data = request.get_json()
    return send_json_response(mongo_db_client.track_activity(req_data))

@app.route("/second-breakfast/recommendation/<uid>")
def recommend(uid):
    return send_json_response(mongo_db_client.get_recommendation(uid))

@app.route("/second-breakfast/explore/<uid>")
def explore(uid):
    things = mongo_db_client.get_recommendation(uid)
    list_of_things = things["favourite"] + things["short_favourite"] + things["explore_favourite"]
    return send_json_response(list_of_things)

@app.route("/second-breakfast/statistics/<uid>")
def statistics(uid):
    # req_data = request.get_json()
    # print(req_data)
    return send_json_response(mongo_db_client.get_dashboard(uid))

if __name__ == '__main__':
    app.run(debug=True)

