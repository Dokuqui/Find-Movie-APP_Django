"""Import necessary libraries."""
from django.db import models
from datetime import datetime


class Movie(models.Model):
    """Movie model."""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, help_text="The title of the movie.")
    runtime = models.CharField(max_length=255, help_text="The duration of the movie.")
    release_date = models.DateField(null=True, blank=True, help_text="The date the movie was released.")
    genre = models.CharField(max_length=255, help_text="The genre of the movie.")
    director = models.CharField(max_length=255, help_text="The director of the movie.")
    actors = models.CharField(max_length=255, help_text="The actors in the movie.")
    movie_id = models.CharField(max_length=255, unique=True, help_text="Enter the id of the movie.")
    imdb_id = models.CharField(max_length=255, unique=True, help_text="Enter the IMDb ID.")
    plot = models.TextField(blank=True, help_text="The plot of the movie.")
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    response = models.CharField(max_length=10, choices=[("JSON", "JSON"), ("XML", "XML")],
                                default="JSON", blank=True)

    def __str__(self):
        """String for representing the Movie object."""
        return f"{self.title} ({self.release_date}) - {self.genre}"

    def save(self, *args, **kwargs):
        if isinstance(self.release_date, str):
            try:
                self.release_date = datetime.strptime(self.release_date, "%Y-%m-%d").date()
            except ValueError:
                pass
        super().save(*args, **kwargs)
