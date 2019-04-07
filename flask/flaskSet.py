from flask import Flask
import mongo_db_client

app = Flask(__name__)

@app.route("/second-breakfast/show-recipe/")
def show_recipe():
    return mongo_db_client.get_data_to_set_pref()


if __name__ == '__main__':
    app.run(debug=True)

