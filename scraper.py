import requests
from bs4 import BeautifulSoup


class RatingScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def get_imdb_rating(self, imdb_id):
        try:
            url = f"https://www.imdb.com/title/{imdb_id}/"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            rating = soup.find(name="span", class_="sc-4dc495c1-1 lbQcRY")
            if rating:
                score = float(rating.text)
                return score
            else:
                return None
        except Exception as e:
            print(f"error: {e}")
        return None

    def get_rt_rating(self, show_name):
        formatted_name = show_name.lower().replace(" ", "_")
        url = f"https://www.rottentomatoes.com/tv/{formatted_name}"
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")
            rating = soup.find(name="rt-text", attrs={"slot": "critics-score"})
            if rating:
                score = rating.text.replace("%", "")
                return int(score)
            else:
                return None
        except Exception as e:
            print(f"error: {e}")
        return None
