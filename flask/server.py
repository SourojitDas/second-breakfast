from flask import Flask, request
from flask_cors import CORS
import mongo_db_client

app = Flask(__name__)
CORS(app)

@app.route("/second-breakfast/show-recipe/")
def show_recipe():
    return mongo_db_client.get_data_to_set_pref()

@app.route("/second-breakfast/save_user_model/", methods=['POST'])
def save_new_user_model():
    req_data = request.get_json()
    return mongo_db_client.save_user_model(req_data)

@app.route("/second-breakfast/activity", methods=['POST'])
def submit_activity():
    req_data = request.get_json()
    return mongo_db_client.track_activity(req_data)

@app.route("/second-breakfast/recommendation", methods=['POST'])
def recommend():
    req_data = request.get_json()
    return mongo_db_client.get_recommendation(req_data["user_id"])

@app.route("/second-breakfast/test/")
def test():
    return mongo_db_client.get_recommendation("uid01")

@app.route("/second-breakfast/test/", method=["POST"])
def statsitics():
    req_data = request.get_json()
    return mongo_db_client.get_dashboard(req_data["user_id"])

if __name__ == '__main__':
    app.run(debug=True)

