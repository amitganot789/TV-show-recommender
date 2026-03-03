import time

import pandas as pd

from recommender import Recommender
from scraper import RatingScraper
from tmdb_api import TMDB


def main():
    my_tmdb = TMDB()
    my_scraper = RatingScraper()
    my_rec = Recommender()
    dataset_rows = []

    shows_dict = my_tmdb.get_show_list(120)

    for show_name, tmdb_id in shows_dict.items():
        show_inf = my_tmdb.get_show_details(tmdb_id)
        imdb_rating = my_scraper.get_imdb_rating(show_inf["imdb_id"])
        rt_rating = my_scraper.get_rt_rating(show_name)
        print(show_name)
        quality_score = my_rec.get_quality_modifier(imdb_rating, rt_rating)
        show_inf["quality_score"] = quality_score
        soup = my_rec.data_soup(show_inf)
        show_inf["soup"] = soup

        dataset_rows.append(show_inf)

        time.sleep(1.5)

    # v = Number of votes (vote_count)
    # m = Minimum votes required (70th percentile)
    # R = Average rating of the specific show
    # c = Mean rating across the entire dataset
    df = pd.DataFrame(dataset_rows)
    R = (df["vote_average"] + (df["quality_score"] * 10) * 2)/3
    c = R.mean()
    m = df["vote_count"].quantile(0.7)
    v = df["vote_count"]
    bayesian_score = (v / (v + m) * R) + (m / (v + m) * c)
    df["quality_score"] = bayesian_score / 10
    df.to_csv("final_data.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
