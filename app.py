import sys

import pandas as pd
from flask import Flask, jsonify

from recommender import Recommender

app = Flask(__name__)
app.json.ensure_ascii = False
app.config['JSON_AS_ASCII'] = False

try:
    df = pd.read_csv("final_data.csv")
except FileNotFoundError:
    print("Error")
    sys.exit(1)
names_list = df["name"].tolist()
fixed_names = []
for name in names_list:
    fixed_names.append(name.lower().replace(" ", ""))
soups_list = df["soup"].tolist()
quality_list = df["quality_score"].tolist()
overviews_list = df["overview"].tolist()
trailers_list = df["trailer"].tolist()

my_rec = Recommender()

print("calculating")
sim_matrix = my_rec.get_similarity_matrix(soups_list)


@app.route('/')
def home():
    return "Welcome to my show recommender engine!"


@app.route('/recommend/<show_name>')
def recommended(show_name):
    search_name = show_name.lower().replace(" ", "")
    if search_name not in fixed_names:
        return f"{show_name} is not in the dataset, please try another show!"
    else:
        recommendations = my_rec.get_recommendations(names_list[fixed_names.index(search_name)], names_list, sim_matrix,
                                                     quality_list, overviews_list, trailers_list)

        return jsonify({"show_name": names_list[fixed_names.index(search_name)], "recommended_shows": recommendations})


if __name__ == "__main__":
    app.run(debug=True)
