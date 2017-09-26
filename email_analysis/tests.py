"""Testing functions for correo."""

import os

from django.test import TestCase

from .models import Email, Host, IPAddress, Url

test_email_file_path = os.path.join(os.getcwd(),
                                    "test_resources/test.eml")
DEFAULT_FULL_TEXT = None
DEFAULT_HOSTNAME = "test.com"
DEFAULT_IP_ADDRESS = "0.0.0.0"
DEFAULT_RECIPIENT = "11hurdj@gmail"
DEFAULT_SENDER_EMAIL = "jhurd@test.com"
DEFAULT_SENDER_IP = "0.0.0.0"
DEFAULT_SUBJECT = "Email me"
DEFAULT_SUBMITTER = "12345678"
DEFAULT_URL = "http://test.com/training/bingo.php"

with open(test_email_file_path, 'r') as f:
    DEFAULT_FULL_TEXT = f.read()
    f.close()

# dict formatted as it is when posted to the review view
# EMAIL_DICT = {
#     'subject': 
# }


def create_email():
    """Create a testing email."""
    return Email.objects.create(full_text=DEFAULT_FULL_TEXT,
                                subject=DEFAULT_SUBJECT,
                                recipient_email=DEFAULT_RECIPIENT,
                                sender_email=DEFAULT_SENDER_EMAIL,
                                sender_ip=DEFAULT_SENDER_IP,
                                submitter=DEFAULT_SUBMITTER)


def create_host(host_name=DEFAULT_HOSTNAME):
    """Create a host for testing."""
    return Host.objects.create(host_name=host_name)


def create_ip_address(ip_address=DEFAULT_IP_ADDRESS):
    """Create an IP address for testing."""
    return IPAddress.objects.create(ip_address=ip_address)


def create_url(url=DEFAULT_URL):
    """Create a URL for testing."""
    return Url.objects.create(url=url, url_file="bingo.php",
                              host=create_host())


class TestUtility(TestCase):
    """Utility for performing repetitive tests."""

    def association_test(self, object1, object2, storage_location1,
                         storage_location2, many_to_one=False):
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
        """Ensure object's string matches up to the desired string."""
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

        relater.association_test(new_email, new_host, new_email.host_set,
                                 new_host.emails)

    def test_relate_email_y_ip_address(self):
        """Test relating an email with an IP address."""
        new_email = create_email()
        new_ip_address = create_ip_address()

        relater.association_test(new_email, new_ip_address,
                                 new_email.ipaddress_set,
                                 new_ip_address.emails)

    def test_relate_email_y_url(self):
        """Test relating an email with a URL."""
        new_email = create_email()
        new_url = create_url()

        relater.association_test(new_email, new_url, new_email.url_set,
                                 new_url.emails)


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

        relater.association_test(new_host, new_ip_address,
                                 new_host.ipaddress_set, new_ip_address.hosts)

    def test_relate_host_y_url(self):
        """Test relating a host with a URL."""
        new_host = create_host()
        new_url = create_url()

        relater.association_test(new_host, new_url, new_host.url_set,
                                 new_url.host, True)


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

    def test_index_view(self):
        """Test the index view."""
        response = self.client.get('/email/')
        self.assertContains(response, "Recent Emails:")

    def test_index_view_after_email_creation(self):
        """Test the index view when an email has been created."""
        new_email = create_email()
        response = self.client.get('/email/')
        self.assertContains(response, new_email.subject)

    def test_import_view(self):
        """Test the import view."""
        response = self.client.get('/email/import/')
        self.assertContains(response, "Upload")

    def test_parse_view(self):
        """Test the parse view."""
        response = self.client.post('/email/import/parse', {
            'full-text': DEFAULT_FULL_TEXT
        })
        # make sure that the parser is redirecting to the review step
        self.assertEqual(response.url, "/email/import/review")

    def test_review_view(self):
        """Test the review view."""
        # TODO: make this test more robust (currently it only tests to make sure that the review view is available)
        response = self.client.get('/email/import/review')
        self.assertEqual(response.status_code, 200)

    def test_save_view(self):
        """Test the save view."""
        response = self.client.post('/email/import/save', {
            'email_subject': DEFAULT_SUBJECT,
            'recipient_email': DEFAULT_RECIPIENT,
            'sender_email': DEFAULT_SENDER_EMAIL,
            'sender_ip': DEFAULT_SENDER_IP
        })
        # ensure email created and system redirects to new email
        self.assertEqual(response.url, "/email/1/")

    def test_email_details_view(self):
        """Test the email details view."""
        new_email = create_email()
        response = self.client.get("/email/{}/".format(new_email.id))
        self.assertContains(response, new_email.subject)
