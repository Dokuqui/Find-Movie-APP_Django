from django.urls import path

from . import views

urlpatterns = [
    path("movie/", views.movie_app, name='movie_app'),
]