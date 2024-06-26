"""Import necessary libraries."""
from datetime import datetime

from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .form import ContactForm
from .models import Movie
from .api_calls import get_movie_data


def movie_app(request):
    """Search movies"""
    search_term = request.GET.get('title')
    if not search_term:
        return render(request, 'movie_app/home.html')

    # Check if the search term is a valid movie ID
    if search_term.isdigit():
        try:
            movie = Movie.objects.get(pk=int(search_term))
            return render(request, 'movie_app/movie_detail.html', {'movie': movie})
        except ObjectDoesNotExist:
            return render(request, 'movie_app/error.html', {'message': 'Movie not found.'})
    else:
        # Search by title using OMDB API
        data = get_movie_data(search_term)

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

        return render(request, 'movie_app/error.html', {'message': 'Movie not found.'})


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
