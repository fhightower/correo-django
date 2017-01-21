from django.test import TestCase

from .models import Email, Host


class EmailTests(TestCase):

    def test_email_create(self):
        """Test email creation."""
        new_email = Email()


class HostTests(TestCase):

    def test_host_create(self):
        """Test host creation."""
        new_host = Host()


