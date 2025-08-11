from flask import Flask, render_template, request, abort
from algorithm import recommend_movies, get_movie_details
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
TMDB_API_KEY = os.getenv("API_KEY")

@app.route('/')
def home():
    """
    Renders the main form page.
    """
    return render_template('form.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Handles the movie recommendation logic.
    """
    title = request.form['title'].strip()
    language = request.form['language']
    
    if not title:
        return render_template('error.html', message="Please enter a movie title.")

    recommendations = recommend_movies(title, language)
    
    # This check correctly handles both error messages (strings) and empty lists.
    if not recommendations or isinstance(recommendations[0], str):
        error_message = recommendations[0] if recommendations else f"Could not find recommendations for '{title}'."
        return render_template('error.html', message=error_message)

    # Pass the selected language to the results template for the next step
    return render_template('result.html', title=title, recommendations=recommendations, language=language)

@app.route('/movie/<int:movie_id>')
def movie_details_page(movie_id):
    """
    Displays the details for a specific movie.
    """
    language = request.args.get('language', 'en-US') 
    
    details = get_movie_details(movie_id, language)
    
    if details is None:
        return render_template('error.html', message="Could not retrieve details for this movie.")

    return render_template('movie_details.html', movie=details)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
