from django.test import TestCase

from .models import Email, Host


DEFAULT_HOSTNAME = "test.com"

def create_email():
    return Email.objects.create(full_text="Full email text here", subject="Email me", recipient_email="11hurdj@gmail.com", sender_email="jhurd@test.com", sender_ip="0.0.0.0", submitter="12345678")

def create_host(host_name=DEFAULT_HOSTNAME):
    return Host.objects.create(host_name=host_name)


class EmailTests(TestCase):

    def test_create_email(self):
        """Test email creation."""
        new_email = create_email()
        self.assertIs(type(new_email.id), int)

    def test_create_and_relate_email_with_host(self):
        """Test relating an email with a host."""
        new_email = create_email()
        new_host = create_host()

        new_email.host_set.add(new_host)
        self.assertEqual(new_email.host_set.all()[0].host_name, DEFAULT_HOSTNAME)


class HostTests(TestCase):

    def test_create_host(self):
        """Test host creation."""
        new_host = create_host()
        self.assertIs(type(new_host.id), int)


    def test_create_and_relate_host_with_email(self):
        """Test relating a host with an email."""
        new_host = create_host()
        new_email = create_email()

        new_host.emails.add(Email.objects.get(pk=1))
        self.assertEqual(new_host.emails.all()[0].id, 1)
