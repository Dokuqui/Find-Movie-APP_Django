"""Import necessary libraries."""
from django.shortcuts import render
import requests
from .models import Movie
from datetime import datetime


def movie_app(request):
    """View function for home page"""
    if request.method == 'POST':
        search_term = request.POST.get('title')
        movie = Movie.objects.filter(title__icontains=search_term).first()
        if movie:
            return render(request, 'movie_app/movie_detail.html', {'movie': movie})
        else:
            if search_term.isdigit():
                api_url = 'http://www.omdbapi.com/?i=' + search_term + '&apikey=8dcbd9c7'
            else:
                api_url = 'http://www.omdbapi.com/?t=' + search_term + '&apikey=8dcbd9c7'

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
                return render(request, 'movie_app/movie_detail.html', {'movie': movie})
            else:
                return render(request, 'movie_app/error.html', {'message': 'No results found.'})
    else:
        return render(request, 'movie_app/home.html')
