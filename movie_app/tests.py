"""Import necessary libraries."""
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.mail import EmailMessage
from unittest.mock import patch
from .views import movie_app, usage, contact
from .models import Movie
from .form import ContactForm
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
        """Test search view with invalid movie title"""
        request = self.factory.post('/movie_app/movie/', {'title': 'AESDSQZE'})
        response = movie_app(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,  'Movie not found.')

    def test_movie_search_invalid_id(self):
        """Test search view with invalid movie ID"""
        request = self.factory.post('/movie_app/movie/', {'title': 10})
        response = movie_app(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie not found.')

    def test_empty_search_term(self):
        """Test search view with empty search term"""
        request = self.factory.post('/movie_app/movie/', {'title': ''})
        response = movie_app(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search term cannot be empty.')

    def test_movie_search_api_failure(self):
        """Test search view when OMDB API returns failure response"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {'Response': 'False'}
            request = self.factory.post('/movie_app/movie/', {'title': 'InvalidMovie'})
            response = movie_app(request)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Movie not found.')

    def test_usage_view(self):
        """Test usage view"""
        request = self.factory.post('/usage')
        response = usage(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'How to Use Film Hunt')

    def test_contact_view_get(self):
        """Test contact view for GET request"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertContains(response, 'Contact Us')

    @patch('movie_app.views.EmailMessage')
    def test_contact_view_post(self, mock_email_message):
        """Test contact view for POST request"""
        data = {
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'content': 'Test Content'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        mock_email_message.assert_called_once_with(
            subject='Test Subject',
            body='Test Content',
            from_email='test@example.com',
            to=['i.semenov6990@gmail.com'],
            reply_to=['test@example.com']
        )
        mock_email_message.return_value.send.assert_called_once_with(fail_silently=False)
