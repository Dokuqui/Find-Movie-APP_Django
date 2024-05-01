# Generated by Django 5.0.3 on 2024-05-01 14:20

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
                (
                    "response",
                    models.CharField(
                        blank=True,
                        choices=[("JSON", "JSON"), ("XML", "XML")],
                        default="JSON",
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]