# Generated by Django 5.0.3 on 2024-05-01 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(
                        help_text="The title of the movie.", max_length=255
                    ),
                ),
                (
                    "runtime",
                    models.CharField(
                        help_text="The duration of the movie.", max_length=255
                    ),
                ),
                (
                    "release_date",
                    models.DateField(help_text="The date the movie was released."),
                ),
                (
                    "genre",
                    models.CharField(
                        help_text="The genre of the movie.", max_length=255
                    ),
                ),
                (
                    "director",
                    models.CharField(
                        help_text="The director of the movie.", max_length=255
                    ),
                ),
                (
                    "actors",
                    models.CharField(
                        help_text="The actors in the movie.", max_length=255
                    ),
                ),
                (
                    "movie_id",
                    models.CharField(
                        help_text="Enter the id of the movie.",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "imdb_id",
                    models.CharField(
                        help_text="Enter the IMDb ID.", max_length=255, unique=True
                    ),
                ),
                (
                    "plot",
                    models.TextField(blank=True, help_text="The plot of the movie."),
                ),
                ("poster_url", models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
