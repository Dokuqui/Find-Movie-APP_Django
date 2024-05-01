"""Import necessary libraries."""
import os
from datetime import datetime
from django.shortcuts import render
import requests
from dotenv import load_dotenv
from .models import Movie


load_dotenv()


def movie_app(request):
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')
    """View function for home page"""
    if request.method == 'POST':
        search_term = request.POST.get('title')
        movie = Movie.objects.filter(title__icontains=search_term).first()
        if movie:
            return render(request, 'movie_app/movie_detail.html', {'movie': movie})
        else:
            if search_term.isdigit():
                api_url = 'http://www.omdbapi.com/?i=' + search_term + f'&apikey={OMDB_API_KEY}'
            else:
                api_url = 'http://www.omdbapi.com/?t=' + search_term + f'&apikey={OMDB_API_KEY}'

            response = requests.get(api_url)
            data = response.json()

            print(data)

            if data.get('Response') == 'True':
                # Parse the release_date into a valid date format
                release_year = ''.join(filter(str.isdigit, data['Year']))
                print("Release year:", release_year)
                try:
                    release_date = datetime.strptime(release_year, '%Y').date()
                    print("Parsed release date:", release_date)
                except ValueError:
                    release_date = None
                    print("Failed to parse release date")

                movie = Movie.objects.create(
                    title=data['Title'],
                    release_date=release_date,
                    runtime=data['Runtime'],
                    genre=data['Genre'],
                    director=data['Director'],
                    actors=data['Actors'],
                    movie_id=data['imdbID'],
                    imdb_id=data['imdbID'],
                    plot=data['Plot'],
                    response=data['Type']
                )

                poster_url = data.get('Poster')
                if poster_url:
                    movie.poster_url = poster_url
                    movie.save()

                return render(request, 'movie_app/movie_detail.html', {'movie': movie})
            else:
                return render(request, 'movie_app/error.html', {'message': 'No results found.'})
    else:
        return render(request, 'movie_app/home.html')
