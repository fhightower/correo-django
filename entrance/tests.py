from django.test import TestCase
from django.urls import reverse


class ViewTests(TestCase):
    """View related tests."""

    def test_index_view(self):
        """Test entrance:index."""
        response = self.client.get(reverse("entrance:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the home page!")

    def test_about_view(self):
        """Test entrance:about."""
        response = self.client.get(reverse("entrance:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Who, Why, What, and How?")

    def test_invest_view(self):
        """Test entrance:invest."""
        response = self.client.get(reverse("entrance:invest"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upgrade your tools!")
