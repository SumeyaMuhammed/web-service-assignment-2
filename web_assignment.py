from flask import Flask, request, jsonify, render_template_string
import requests
import logging
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load API Key from .env
load_dotenv()
TMDB_KEY = os.getenv("API_KEY")
JWT_SECRET = "my_jwt_assignment_secret"  

app = Flask(__name__)

# Logging
logging.basicConfig(
    filename="movie_app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# MOVIE DATA FETCHING (TMDB API)


def fetch_movie(movie_id=550):
    """Fetch specific movie details from TMDB."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_KEY}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_popular_movies():
    """Fetch a list of popular movies from TMDB."""
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": TMDB_KEY}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

@app.route("/movie")
def get_movie():
    movie_id = request.args.get("id", "550")

    try:
        data = fetch_movie(movie_id)
        logging.info(f"Movie fetch SUCCESS: Movie {movie_id}")
        return jsonify({"status": "success", "movie": data})
    except Exception as e:
        logging.error(f"Movie fetch ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# MOVIE LISTING (SHOW VALID IDs)

@app.route("/movies/list")
def list_movies():
    """Return a list of popular movies with their IDs so users know what ID to use."""
    try:
        data = fetch_popular_movies()
        movies = [
            {"id": movie["id"], "title": movie["title"]}
            for movie in data.get("results", [])
        ]
        return jsonify({"available_movies": movies})
    except Exception as e:
        logging.error(f"Movie list error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask Application on port 5050")
    app.run(debug=True, port=5050)(debug=True, port=5050)
