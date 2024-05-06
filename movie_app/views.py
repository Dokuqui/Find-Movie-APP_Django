"""Import necessary libraries."""
import os
from datetime import datetime

from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
import requests
from dotenv import load_dotenv

from .form import ContactForm
from .models import Movie


load_dotenv()


def movie_app(request):
    """Search movies"""
    if request.method == 'POST':
        search_term = request.POST.get('title')
        if search_term:
            # Check if the search term is a valid movie ID
            if search_term.isdigit():
                try:
                    movie = Movie.objects.get(pk=int(search_term))
                    return render(request, 'movie_app/movie_detail.html', {'movie': movie})
                except ObjectDoesNotExist:
                    return render(request, 'movie_app/error.html', {'message': 'Movie not found.'})
            else:
                # Search by title using OMDB API
                OMDB_API_KEY = os.getenv('OMDB_API_KEY')
                api_url = 'http://www.omdbapi.com/?t=' + search_term + f'&apikey={OMDB_API_KEY}'
                response = requests.get(api_url)
                data = response.json()

                if data.get('Response') == 'True':
                    # Parse the release_date into a valid date format
                    release_year = ''.join(filter(str.isdigit, data['Year']))
                    try:
                        release_date = datetime.strptime(release_year, '%Y').date()
                    except ValueError:
                        release_date = None

                    # Check if the movie already exists in the database
                    movie, created = Movie.objects.get_or_create(
                        title=data['Title'],
                        defaults={
                            'release_date': release_date,
                            'runtime': data['Runtime'],
                            'genre': data['Genre'],
                            'director': data['Director'],
                            'actors': data['Actors'],
                            'movie_id': data['imdbID'],
                            'imdb_id': data['imdbID'],
                            'plot': data['Plot'],
                            'response': data['Type']
                        }
                    )

                    if created:
                        # Save the poster URL if it exists
                        poster_url = data.get('Poster')
                        if poster_url:
                            movie.poster_url = poster_url
                            movie.save()

                    return render(request, 'movie_app/movie_detail.html', {'movie': movie})
                else:
                    return render(request, 'movie_app/error.html', {'message': 'Movie not found.'})
        else:
            return render(request, 'movie_app/error.html', {'message': 'Search term cannot be empty.'})
    else:
        return render(request, 'movie_app/home.html')


def usage(request):
    """Render usage page."""
    return render(request, 'movie_app/usage.html')


def contact(request):
    """Render contact page."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            recipient_email = 'i.semenov6990@gmail.com'

            email_message = EmailMessage(
                subject=subject,
                body=content,
                from_email=sender_email,
                to=[recipient_email],
                reply_to=[sender_email]
            )
            email_message.send(fail_silently=False)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = ContactForm()
    return render(request, 'movie_app/contact.html', {'form': form})
