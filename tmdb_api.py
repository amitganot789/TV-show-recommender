import os

import requests
from dotenv import load_dotenv

load_dotenv()


class TMDB:
    def __init__(self):
        self.api = os.getenv("TMDB_API")

    def search_show(self, query):
        search_url = "https://api.themoviedb.org/3/search/tv"
        params = {
            "api_key": self.api,
            "query": query
        }
        try:
            response = requests.get(url=search_url, params=params)
            data = response.json()
            ID = data["results"][0]["id"]
            return ID
        except Exception as e:
            print(f"error: {e}")
        return None

    def get_show_details(self, show_id):
        details_url = f"https://api.themoviedb.org/3/tv/{show_id}"
        params = {
            "api_key": self.api,
            "append_to_response": "videos,keywords,external_ids"
        }

        try:
            response = requests.get(url=details_url, params=params)
            data = response.json()
            # print(data)
            show_inf = {
                "name": data["name"],
                "vote_average": data["vote_average"],
                "vote_count": data["vote_count"],
                "overview": data["overview"],
                "genres": [],
                "keyword": [],
                "trailer": None,
                "imdb_id": data["external_ids"]["imdb_id"]
            }
            for i in data["genres"]:
                show_inf["genres"].append(i["name"])

            for i in data["keywords"]["results"]:
                show_inf["keyword"].append(i["name"])

            for i in data["videos"]["results"]:
                if i["type"] == "Trailer" and i["site"] == "YouTube":
                    key = i["key"]
                    show_inf["trailer"] = f"https://www.youtube.com/watch?v={key}"
                    break

            return show_inf
        except Exception as e:
            print(f"error: {e}")
        return None

    def get_show_list(self, pages):
        top_shows_url = f"https://api.themoviedb.org/3/tv/top_rated"
        show_info = {}
        for page in range(1, pages + 1):
            params = {
                "api_key": self.api,
                "page": page
            }
            response = requests.get(url=top_shows_url, params=params)
            data = response.json()
            for i in data["results"]:
                if i["original_language"] == "en":
                    show_info[i["original_name"]] = i["id"]
        return show_info
