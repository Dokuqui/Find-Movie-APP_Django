from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("movie_app/", include("movie_app.urls")),
    path("admin/", admin.site.urls),
]