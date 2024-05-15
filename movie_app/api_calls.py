"""Import necessary libraries."""
import os
import requests


def get_movie_data(search_term):
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')
    api_url = 'http://www.omdbapi.com/?t=' + search_term + f'&apikey={OMDB_API_KEY}'
    response = requests.get(api_url)
    return response.json()
