from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender():
    def __init__(self):
        pass

    def data_soup(self, show_inf):
        word_list = show_inf["keyword"] + show_inf["genres"] * 9
        return " ".join(word_list)

    def get_similarity_matrix(self, soup_list):
        cv = CountVectorizer(stop_words='english')
        count_matrix = cv.fit_transform(soup_list)
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        return cosine_sim

    def get_recommendations(self, target_show_name, names_list, sim_matrix, quality_list, overviews_list,
                            trailers_list):
        recommended_shows = []
        shows_rating = []
        show_index = names_list.index(target_show_name)
        line = sim_matrix[show_index]
        index_scores = list(enumerate(line))
        for j in index_scores:
            if j[0] == show_index:
                continue
            shows_rating.append((j[0], j[1] * quality_list[j[0]]))
        shows_rating.sort(key=lambda x: x[1], reverse=True)
        rec_list = shows_rating[0:5]
        for i in rec_list:
            show_dict = {
                "name": names_list[i[0]],
                "overview": overviews_list[i[0]],
                "trailer": trailers_list[i[0]],
            }
            recommended_shows.append(show_dict)
        return recommended_shows

    def get_quality_modifier(self, imdb_rating, rt_rating):
        if imdb_rating and rt_rating:
            rating = (imdb_rating / 10 + rt_rating / 100) / 2
        elif imdb_rating:
            rating = imdb_rating / 10
        elif rt_rating:
            rating = rt_rating / 100
        else:
            rating = 0.5

        return rating
