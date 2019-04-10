from flask import Flask, request
import mongo_db_client

app = Flask(__name__)

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




if __name__ == '__main__':
    app.run(debug=True)

