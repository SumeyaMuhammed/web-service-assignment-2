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

# AUTHENTICATION (JWT)


@app.route("/auth/login", methods=["POST"])
def login():
    body = request.json or {}
    username = body.get("username", "student")

    token = jwt.encode(
        {"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)},
        JWT_SECRET,
        algorithm="HS256",
    )

    return jsonify({"token": token})


def jwt_required(f):
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing token"}), 401

        token = auth.split()[1]

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = decoded["sub"]
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    wrapper.name = f.name
    return wrapper


@app.route("/auth/profile")
@jwt_required
def profile():
    return jsonify({
        "status": "authorized",
        "user": request.user
    })


# MOVIE DATA TRANSFORMATION

@app.route("/movies/summary")
def movie_summary():
    try:
        data = fetch_popular_movies()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    movies = data["results"]

    html = """
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            background: #f5f5f5;
            padding: 40px;
            color: #333;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .card {
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .poster {
            width: 100%;
            border-radius: 10px;
        }
        .title {
            font-weight: bold;
            font-size: 1.1rem;
            margin-top: 10px;
        }
        .overview {
            font-size: 0.9rem;
            margin-top: 8px;
        }
    </style>

    <h1>Popular Movies</h1>

    <div class="grid">
        {% for movie in movies %}
        <div class="card">
            {% if movie.poster_path %}
                <img src="https://image.tmdb.org/t/p/w500{{ movie.poster_path }}" class="poster">
            {% endif %}
            <div class="title">{{ movie.title }}</div>
            <div class="overview">{{ movie.overview }}</div>
        </div>
        {% endfor %}
    </div>
    """


    return render_template_string(html, movies=movies)


# ----------------------------------------------------------------------
# MOVIE LISTING (SHOW VALID IDs)
# ----------------------------------------------------------------------

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
