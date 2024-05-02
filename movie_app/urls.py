from django.urls import path

from . import views

urlpatterns = [
    path("movie/", views.movie_app, name='home'),
    path("movie/usage", views.movie_app, name='usage'),
    path("movie/contact", views.movie_app, name='contact')
]
