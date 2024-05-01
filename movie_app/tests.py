"""Import necessary libraries."""
from django.test import TestCase, RequestFactory
from .views import movie_app
from .models import Movie
from faker import Faker


class MovieAppViewTests(TestCase):
    """Tests for the Movie app views"""

    def setUp(self):
        """Set up test fixtures"""
        self.factory = RequestFactory()
        self.fake = Faker()
        self.test_movie = Movie.objects.create(
            id=1,
            title=self.fake.name(),
            release_date=self.fake.date(),
            runtime=self.fake.time(),
            genre=self.fake.words(nb=3),
            director=self.fake.name(),
            actors=self.fake.name(),
            movie_id=self.fake.uuid4(),
            imdb_id=self.fake.uuid4(),
            plot=self.fake.sentence(),
            poster_url=self.fake.url()
        )

    def test_movie_detail_by_id(self):
        """Test detail view by movie ID"""
        request = self.factory.get('/movie_app/movie/', {'id': self.test_movie.pk})
        response = movie_app(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_movie.id)

    def test_movie_search_by_title(self):
        """Test search view by movie title"""
        request = self.factory.post('/movie_app/movie/', {'title': 'Famous Nonexistent Movie Quotes (PART 1)'})
        response = movie_app(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Famous Nonexistent Movie Quotes (PART 1)')

    def test_movie_search_no_results(self):
        """Test search view with no results"""
        request = self.factory.post('/movie_app/movie/', {'title': 'AESDSQZE'})
        response = movie_app(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,  'Movie not found.')

    def test_empty_search_term(self):
        """Test search view with empty search term"""
        request = self.factory.post('/movie_app/movie/', {'title': ''})
        response = movie_app(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search term cannot be empty.')
