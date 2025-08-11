import requests
import os
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

TMDB_API_KEY = os.getenv("API_KEY")
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_movie_id(movie_name, language='en-US'):
    """
    Searches for a movie by name and returns its TMDB ID.
    """
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {'api_key': TMDB_API_KEY, 'query': movie_name, 'language': language}
    try:
        # Added verify=False to bypass SSL certificate verification issues on strict networks
        response = requests.get(url, params=params, headers=HEADERS, verify=False)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            return data["results"][0]["id"]
    except requests.exceptions.RequestException as e:
        print(f"API request failed in get_movie_id: {e}")
    return None

def get_recommendations(movie_id, language='en-US'):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {'api_key': TMDB_API_KEY , 'language': language}
    response = requests.get(url, params=params)
    recommendations = []
    if response.status_code == 200:
        results = response.json().get('results', [])
        for movie in results[:10]:  # Fetch top 10 recommendations
            if movie.get('poster_path'): # Only include movies with a poster
                recommendations.append({
                    'id': movie.get('id'),
                    'title': movie.get('title'),
                    'overview': movie.get('overview'),
                    'poster_path': movie.get('poster_path'),
                    'vote_average': movie.get('vote_average')
                })
    return recommendations
    
def get_movie_details(movie_id, language='en-US'):
    """
    Fetches detailed information for a specific movie ID.
    """
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {'api_key': TMDB_API_KEY, 'language': language}
    try:
        # Added verify=False
        response = requests.get(url, params=params, headers=HEADERS, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed in get_movie_details: {e}")
    return None

def recommend_movies(title, language='en-US'):
    movie_id= get_movie_id(title, language='en-US')
    if movie_id is None:
        return [f"No movie found for '{title}'"]
    
    recommendations = get_recommendations(movie_id, language='en-US')
    return recommendations

# 🔁 Example usage:
if __name__ == "__main__":
    movie_title = "all the bright places"  # You can test with any movie
    language = "en-US"        
    recommendations = recommend_movies(movie_title, language)
    if recommendations and isinstance(recommendations[0], dict):
        print(f"Recommendations for '{movie_title}':")
        for rec in recommendations:
            print(f"- {rec['title']} (Rating: {rec['vote_average']})")
        else:
            print(recommendations[0])
