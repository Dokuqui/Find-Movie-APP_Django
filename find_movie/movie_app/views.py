from django.shortcuts import render
from .models import Movie
import requests


def index(request):
    """View function for home page"""
    if request.method == 'POST':
        title = request.POST.get('title')
        movie = Movie.objects.filter(title__icontains=title).first()
        if movie:
            return render(request, 'movies/movie_detail.html', {'movie': movie})
        else:
            api_url = 'http://www.omdbapi.com/?apikey=8dcbd9c7&t=' + title
            response = requests.get(api_url)
            data = response.json()
            if data['Response'] == 'True':
                movie = Movie.objects.create(
                    title=data['Title'],
                    release_date=data['Year'],
                    genre=data['Genre'],
                    movie_id=data['imdbID'],
                    imdb_id=data['imdbID'],
                    plot=data['Plot'],
                    response=data['Type']
                )
                return render(request, 'movies/movie_detail.html', {'movie': movie})
            else:
                return render(request, 'movies/error.html', {'message': 'No results found.'})
    else:
        return render(request, 'movies/home.html')
