from django.test import TestCase

from .models import Email, Host

def create_email():
    return Email.objects.create(full_text="Full email text here", subject="Email me", recipient_email="11hurdj@gmail.com", sender_email="jhurd@test.com", sender_ip="0.0.0.0", submitter="12345678")

def create_host(host_name="test.com"):
    return Host.objects.create(host_name=host_name)


class EmailTests(TestCase):

    def test_email_create(self):
        """Test email creation."""
        new_email = create_email()
        self.assertIs(type(new_email.id), int)


class HostTests(TestCase):

    def test_host_create(self):
        """Test host creation."""
        new_host = create_host()
        self.assertIs(type(new_host.id), int)


    def test_create_host_y_add_email(self):
        """Test relating an email with this host."""
        new_host = create_host()
        new_email = create_email()

        new_host.emails.add(Email.objects.get(pk=1))
        self.assertIs(new_host.emails.all()[0].id, 1)
