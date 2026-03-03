import pandas as pd
from recommender import Recommender

shows_pairs = {
    "The Wire": "The Sopranos",
    "Friends": "How I Met Your Mother",
    "Curb Your Enthusiasm": "Seinfeld",
    "Boardwalk Empire": "The Sopranos",
    "Breaking Bad": "Better Call Saul",
    "True Detective": "Mindhunter",
    "Narcos": "Peaky Blinders",
    "Succession": "Six Feet Under",
    "Mad Men": "The Crown",
    "The Office": "Parks and Recreation",
    "Game of Thrones": "House of the Dragon",
    "Black Mirror": "Severance",
}

df = pd.read_csv("final_data.csv")

weights_to_test = range(1, 10)
my_rec = Recommender()
names_list = df["name"].tolist()
quality_list = df["quality_score"].tolist()
overviews_list = df["overview"].tolist()
trailers_list = df["trailer"].tolist()

best_score = 0
best_weight = 0

for weight in weights_to_test:
    curr_score = 0
    curr_soup = df["keyword"] + " " + (df["genres"] + " ") * weight
    sim_mat = my_rec.get_similarity_matrix(curr_soup)

    for show, expected_pair in shows_pairs.items():
        rec = my_rec.get_recommendations(show, names_list, sim_mat, quality_list, overviews_list, trailers_list)
        for i in rec:
            if i["name"] == expected_pair:
                curr_score += 1
        print(f"Weight {weight:.1f} scored: {curr_score}/{len(shows_pairs)}")
        if curr_score >= best_score:
            best_score = curr_score
            best_weight = weight

print(f"\nOptimization Complete!")
print(f"Best weight multiplier is: {best_weight:.1f} (Score: {best_score})")
