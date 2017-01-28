from django.test import TestCase
from django.urls import reverse

from .models import Email, Host, IPAddress, Url


DEFAULT_SUBJECT = "Email me"
DEFAULT_HOSTNAME = "test.com"
DEFAULT_IP_ADDRESS = "0.0.0.0"
DEFAULT_URL = "http://test.com/training/bingo.php"

def create_email():
    return Email.objects.create(full_text="Full email text here", subject=DEFAULT_SUBJECT, recipient_email="11hurdj@gmail.com", sender_email="jhurd@test.com", sender_ip="0.0.0.0", submitter="12345678")


def create_host(host_name=DEFAULT_HOSTNAME):
    return Host.objects.create(host_name=host_name)


def create_ip_address(ip_address=DEFAULT_IP_ADDRESS):
    return IPAddress.objects.create(ip_address=ip_address)


def create_url(url=DEFAULT_URL):
    return Url.objects.create(url=url, url_file="bingo.php", host=create_host())


class TestUtility(TestCase):
    """Utility for performing repetative tests."""

    def association_test(self, object1, object2, storage_location1, storage_location2, many_to_one=False):
        """Test two-way associations."""
        # test relating the first object with the second
        storage_location1.add(object2)
        self.assertEqual(storage_location1.all()[0].id, 1)

        # test relating the second object with the first
        if not many_to_one:
            storage_location2.add(object1)
            self.assertEqual(storage_location2.all()[0].id, 1)
        else:
            storage_location2 = object1
            self.assertEqual(storage_location2.id, 1)

    def string_test(self, incoming_object, desired_string):
        """Test to make sure and object's string matches up to the desired string."""
        self.assertEqual(str(incoming_object), desired_string)


relater = TestUtility()


class EmailTests(TestCase):
    """Email related tests."""

    def test_create_email(self):
        """Test email creation."""
        new_email = create_email()
        self.assertIs(type(new_email.id), int)

    def test_email_str(self):
        """Test email string."""
        new_email = create_email()
        relater.string_test(new_email, "1")

    def test_relate_email_y_host(self):
        """Test relating an email with a host."""
        new_email = create_email()
        new_host = create_host()

        relater.association_test(new_email, new_host, new_email.host_set, new_host.emails)

    def test_relate_email_y_ip_address(self):
        """Test relating an email with an IP address."""
        new_email = create_email()
        new_ip_address = create_ip_address()

        relater.association_test(new_email, new_ip_address, new_email.ipaddress_set, new_ip_address.emails)

    def test_relate_email_y_url(self):
        """Test relating an email with a URL."""
        new_email = create_email()
        new_url = create_url()

        relater.association_test(new_email, new_url, new_email.url_set, new_url.emails)


class HostTests(TestCase):
    """Host related tests."""

    def test_create_host(self):
        """Test host creation."""
        new_host = create_host()
        self.assertIs(type(new_host.id), int)

    def test_host_str(self):
        """Test host string."""
        new_host = create_host()
        relater.string_test(new_host, DEFAULT_HOSTNAME)

    def test_relate_host_y_ip_address(self):
        """Test relating a host with an ip address."""
        new_host = create_host()
        new_ip_address = create_ip_address()

        relater.association_test(new_host, new_ip_address, new_host.ipaddress_set, new_ip_address.hosts)

    def test_relate_host_y_url(self):
        """Test relating a host with a URL."""
        new_host = create_host()
        new_url = create_url()

        relater.association_test(new_host, new_url, new_host.url_set, new_url.host, True)


class IPAddressTests(TestCase):
    """IP Address related tests."""

    def test_ip_address_create(self):
        """Test IP Address creation."""
        new_ip_address = create_ip_address()
        self.assertIs(type(new_ip_address.id), int)

    def test_ip_address_str(self):
        """Test ip_address string."""
        new_ip_address = create_ip_address()
        relater.string_test(new_ip_address, DEFAULT_IP_ADDRESS)



class UrlTests(TestCase):
    """URL related tests."""

    def test_url_create(self):
        """Test URL creation."""
        new_url = create_url()
        self.assertIs(type(new_url.id), int)

    def test_url_str(self):
        """Test url string."""
        new_url = create_url()
        relater.string_test(new_url, DEFAULT_URL)

class ViewTests(TestCase):
    """View related tests."""

    def test_email_analysis_index_view(self):
        """Test emailanalysis:index."""
        response = self.client.get(reverse("emailanalysis:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No emails are available.")
        self.assertQuerysetEqual(response.context['recent_emails'], [])

    def test_email_analysis_index_view_after_email_creation(self):
        """Test emailanalysis:index after an email has been created."""
        # create a new email
        new_email = create_email()
        # get the response from the emailanalysis index page
        response = self.client.get(reverse("emailanalysis:index"))
        self.assertEqual(response.status_code, 200)
        # check for newly created email's id on page
        self.assertContains(response, new_email.id)
        self.assertQuerysetEqual(response.context['recent_emails'], ["<Email: 1>"])

    def test_upload_view(self):
        """Test emailanalysis:upload."""
        response = self.client.get(reverse("emailanalysis:upload"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Full Email Text")

    def test_review_view(self):
        """Test emailanalysis:review."""
        response = self.client.get(reverse("emailanalysis:review"))
        self.assertEqual(response.status_code, 200)

    def test_email_detail_view(self):
        """Test emailanalysis:details."""
        new_email = create_email()
        # be sure to pass the id of the new email into the client as an argument
        response = self.client.get(reverse("emailanalysis:details", args=(new_email.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are looking at email: {}".format(new_email.id))
