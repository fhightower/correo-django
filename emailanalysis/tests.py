from django.test import TestCase

from .models import Email, Host, IPAddress, Url


DEFAULT_HOSTNAME = "test.com"
DEFAULT_IP_ADDRESS = "0.0.0.0"
DEFAULT_URL = "http://test.com/training/bingo.php"

def create_email():
    return Email.objects.create(full_text="Full email text here", subject="Email me", recipient_email="11hurdj@gmail.com", sender_email="jhurd@test.com", sender_ip="0.0.0.0", submitter="12345678")


def create_host(host_name=DEFAULT_HOSTNAME):
    return Host.objects.create(host_name=host_name)


def create_ip_address(ip_address=DEFAULT_IP_ADDRESS):
    return IPAddress.objects.create(ip_address=ip_address)


def create_url(url=DEFAULT_URL):
    return Url.objects.create(url=url, url_file="bingo.php", host=create_host())


# class TestUtility(TestCase):
#     """Utility for performing repetative tests."""

#     def test_associations(object1, object2, storage_location1, storage_location2):
#         """Test associations in two different ways:
#             object1 and object 2 are two, newly created items which will be associated with one another. Object1 will be associated with object2 by adding object2 to object1.storage_location1. If that works, object 1 will then be associated with object2 by adding object1 to object2.storage_location2.
#         """
#         # test out the first
#         object1.storage_location1.add(object2)
#         object1.storage_location1.remove(object2)

#         # test out the second relationship
#         object2.storage_location2.add(object1)


class EmailTests(TestCase):
    """Email related tests."""

    def test_create_email(self):
        """Test email creation."""
        new_email = create_email()
        self.assertIs(type(new_email.id), int)

    def test_create_and_relate_email_with_host(self):
        """Test relating an email with a host."""
        new_email = create_email()
        new_host = create_host()

        new_email.host_set.add(Host.objects.get(pk=1))
        self.assertEqual(new_email.host_set.all()[0].host_name, DEFAULT_HOSTNAME)

    def test_create_and_relate_email_with_ip_address(self):
        """Test relating an email with an ip address."""
        new_email = create_email()
        new_ip_address = create_ip_address()

        new_email.ipaddress_set.add(IPAddress.objects.get(pk=1))
        self.assertEqual(new_email.ipaddress_set.all()[0].ip_address, DEFAULT_IP_ADDRESS)

    def test_create_and_relate_email_with_url(self):
        """Test relating an email with a URL."""
        new_email = create_email()
        new_url = create_url()

        new_email.url_set.add(Url.objects.get(pk=1))
        self.assertEqual(new_email.url_set.all()[0].url, DEFAULT_URL)


class HostTests(TestCase):
    """Host related tests."""

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

    def test_create_and_relate_host_with_ip_address(self):
        """Test relating a host with an ip address."""
        new_host = create_host()
        new_ip_address = create_ip_address()

        new_host.ipaddress_set.add(IPAddress.objects.get(pk=1))
        self.assertEqual(new_host.ipaddress_set.all()[0].id, 1)

    def test_create_and_relate_host_with_url(self):
        """Test relating a host with a URL."""
        new_host = create_host()
        new_url = create_url()

        new_host.url_set.add(Url.objects.get(pk=1))
        self.assertEqual(new_host.url_set.all()[0].id, 1)


class IPAddressTests(TestCase):
    """IP Address related tests."""

    def test_ip_address_create(self):
        """Test IP Address creation."""
        new_ip_address = create_ip_address()
        self.assertIs(type(new_ip_address.id), int)

    def test_create_and_relate_ip_address_with_email(self):
        """Test relating an ip address with an email."""
        new_ip_address = create_ip_address()
        new_email = create_email()

        new_ip_address.emails.add(Email.objects.get(pk=1))
        self.assertEqual(new_ip_address.emails.all()[0].id, 1)

    def test_create_and_relate_ip_address_with_host(self):
        """Test relating an ip address with a host."""
        new_ip_address = create_ip_address()
        new_host = create_host()

        new_ip_address.hosts.add(Host.objects.get(pk=1))
        self.assertEqual(new_ip_address.hosts.all()[0].id, 1)


class UrlTests(TestCase):
    """URL related tests."""

    def test_url_create(self):
        """Test URL creation."""
        new_url = create_url()
        self.assertIs(type(new_url.id), int)

    def test_create_and_relate_url_with_email(self):
        """Test relating an ip address with an email."""
        new_url = create_url()
        new_email = create_email()

        new_url.emails.add(Email.objects.get(pk=1))
        self.assertEqual(new_url.emails.all()[0].id, 1)






# class AttachmentTests(TestCase):
#     """Attachment related tests."""
    
#     