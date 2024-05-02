from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("movie/", views.movie_app, name='home'),
    path("movie/usage", views.usage, name='usage'),
    path("movie/contact", views.contact, name='contact')
]
