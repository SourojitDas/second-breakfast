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

@app.route("/second-breakfast/show-recipe")
@app.route("/second-breakfast/show-recipe/")
def show_recipe():
    return send_json_response(mongo_db_client.get_data_to_set_pref())

@app.route("/second-breakfast/save_user_model", methods=['POST'])
@app.route("/second-breakfast/save_user_model/", methods=['POST'])
def save_new_user_model():
    req_data = request.get_json()
    return send_json_response(mongo_db_client.save_user_model(req_data))

@app.route("/second-breakfast/modify", methods=['POST'])
@app.route("/second-breakfast/modify/", methods=['POST'])
def modify_long_term_model():
    req_data = request.get_json()
    return send_json_response(mongo_db_client.modify_long_term_model(req_data["user_id"], req_data["attributes"]))

@app.route("/second-breakfast/activity", methods=['POST'])
@app.route("/second-breakfast/activity/", methods=['POST'])
def submit_activity():
    req_data = request.get_json()
    return send_json_response(mongo_db_client.track_activity(req_data))

@app.route("/second-breakfast/recommendation/<uid>")
@app.route("/second-breakfast/recommendation/<uid>/")
def recommend(uid):
    return send_json_response(mongo_db_client.get_recommendation(uid))

@app.route("/second-breakfast/explore/<uid>")
@app.route("/second-breakfast/explore/<uid>/")
def explore(uid):
    return send_json_response(mongo_db_client.get_explorations(uid))

@app.route("/second-breakfast/statistics/<uid>")
@app.route("/second-breakfast/statistics/<uid>/")
def statistics(uid):
    # req_data = request.get_json()
    # print(req_data)
    return send_json_response(mongo_db_client.get_dashboard(uid))

if __name__ == '__main__':
    app.run(debug=False)

