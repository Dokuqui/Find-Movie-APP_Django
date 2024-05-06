from django.urls import path

from . import views

urlpatterns = [
    path("", views.movie_app, name='home'),
    path("/usage", views.usage, name='usage'),
    path("/contact", views.contact, name='contact')
]
