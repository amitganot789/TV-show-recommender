# TV Show Recommender Engine 📺

A content-based recommendation engine for TV shows that combines textual similarity and Bayesian rating aggregation to generate high-quality recommendations.
## How it Works

Instead of just looking at basic genres, this system uses a mix of content similarity and a math formula for the final score:

* **The Dataset:** I wrote a Python script (`build_dataset.py`) that gets data for hundreds of top-rated shows from the TMDB API. It also scrapes ratings from IMDb and Rotten Tomatoes to build a good dataset.
* **Finding the Connection (NLP):** For each show, the code creates a specific text block combining keywords and genres. I used `scikit-learn` to calculate the Cosine Similarity between shows.
  * *Optimization Note: To get the best recommendations, I wrote a script to test different setups. The results showed that giving genres 9 times more weight than keywords gives the most accurate matches based on a test list I created.* 
* **The API:** The backend is a simple Flask app. You send a show name, and it returns a JSON with the best recommendations, including plot summaries and YouTube trailer links.

## Tech Stack

* **Backend:** Python, Flask
* **Data & Math:** Pandas, Scikit-learn (CountVectorizer, Cosine Similarity)
* **Scraping:** Requests, BeautifulSoup4, TMDB API

## How to run it locally

1. Clone this repository.
2. Install the required packages: 
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
    python app.py
   ```
4. Go to your browser and search:
    http://127.0.0.1:5000/recommend/show_name

## How to update the dataset:

1. Create a .env file and add your key:
   ```env
    TMDB_API=your_api_key_here
   ```
2. Run the builder script:
   ```bash
    python build_dataset.py
    ```
