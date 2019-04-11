#!/usr/bin/env python3

from flask import Flask, request
from flask_cors import CORS
import mongo_db_client

app = Flask(__name__)
CORS(app)

@app.route("/second-breakfast/show-recipe/")
def show_recipe():
    return app.response_class(
        response=mongo_db_client.get_data_to_set_pref(),
        mimetype='application/json'
    )

@app.route("/second-breakfast/save_user_model/", methods=['POST'])
def save_new_user_model():
    req_data = request.get_json()
    return app.response_class(
        response=mongo_db_client.save_user_model(req_data),
        mimetype='application/json'
    )

@app.route("/second-breakfast/activity", methods=['POST'])
def submit_activity():
    req_data = request.get_json()
    return app.response_class(
        response=mongo_db_client.track_activity(req_data),
        mimetype='application/json'
    )

@app.route("/second-breakfast/recommendation/<uid>")
def recommend(uid):
    return app.response_class(
        response=mongo_db_client.get_recommendation(uid),
        mimetype='application/json'
    )

@app.route("/second-breakfast/test/")
def test():
    return app.response_class(
        response=mongo_db_client.get_recommendation("uid01"),
        mimetype='application/json'
    )

@app.route("/second-breakfast/statsitics/", methods=['POST'])
def statsitics():
    req_data = request.get_json()
    print(req_data)
    return app.response_class(
        response=mongo_db_client.get_dashboard(req_data['user_id']),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True)

