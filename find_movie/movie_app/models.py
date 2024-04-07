"""Import necessary libraries."""
from django.db import models


class Movie(models.Model):
    """Movie model."""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, help_text="The title of the movie.")
    release_date = models.DateField(help_text="The date the movie was released.")
    genre = models.CharField(max_length=255, help_text="The genre of the movie.")
    movie_id = models.CharField(max_length=255, unique=True, help_text="Enter the id of the movie.")
    imdb_id = models.CharField(max_length=255, unique=True, help_text="Enter the IMDb ID.")
    plot = models.TextField(blank=True, help_text="The plot of the movie.")
    response = models.CharField(max_length=10, choices=[("JSON", "JSON"), ("XML", "XML")],
                                default="JSON", blank=True)

    def __str__(self):
        """String for representing the Movie object."""
        return f"{self.title} ({self.release_date}) - {self.genre}"
