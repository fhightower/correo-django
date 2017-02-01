from django.test import TestCase

class ViewTests(TestCase):
    """View related tests."""

    def test_home_page_view(self):
        """Test the home page view."""
        response = self.client.get('/')
        self.assertContains(response, "Welcome to the home page!")

    def test_about_view(self):
        """Test the about view."""
        response = self.client.get('/about/')
        self.assertContains(response, "Who, Why, What, and How?")

    def test_invest_view(self):
        """Test the invest view."""
        response = self.client.get('/buy/')
        self.assertContains(response, "Upgrade your tools!")
