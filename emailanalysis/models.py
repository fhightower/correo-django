from django.db import models


class Email(models.Model):
    """Database model for handling emails."""

    full_text = models.TextField()
    # header = models.TextField()
    # body = models.TextField()
    # todo: make the recipient email optional (null=True, blank=True)
    recipient_email = models.EmailField()
    # recipient_ip = models.GenericIPAddressField()
    sender_email = models.EmailField()
    sender_ip = models.GenericIPAddressField(null=True, blank=True)
    subject = models.CharField(max_length=500)
    submission_date = models.DateTimeField(auto_now_add=True)
    submitter = models.CharField(max_length=8)

    def __str__(self):
        return str(self.id)


# class Attachment(models.Model):
#     """Attachment class for the attachments' table."""

#     file = models.FileField() # todo: add better handling of files with the file field (https://docs.djangoproject.com/en/1.10/topics/files/ and https://docs.djangoproject.com/en/1.10/ref/models/fields/#filefield)
#     md5 = models.CharField(max_length=32)
#     sha1 = models.CharField(max_length=40)
#     sha256 = models.CharField(max_length=64)
#     # todo: add more stuff here...
#     emails = models.ManyToManyField(Email)


class Host(models.Model):
    """Host class for the hosts' table."""

    host_source_choices = (
        ("B", "Email Body"),
        ("R", "Recipient email address"),
        ("S", "Sender email address"),
        ("U", "From URL"),
    )

    # todo: add more stuff here...
    emails = models.ManyToManyField(Email)
    host_name = models.CharField(max_length=255)
    source = models.CharField(max_length=1, choices=host_source_choices)

    def __str__(self):
        return self.host_name


class IPAddress(models.Model):
    """Database model for handling IP addresses."""

    # todo: add more stuff here...
    ip_address = models.CharField(max_length=15)
    hosts = models.ManyToManyField(Host)
    emails = models.ManyToManyField(Email)

    def __str__(self):
        return self.ip_address


class Url(models.Model):
    """URL class for the URLs' table."""

    url = models.CharField(max_length=2000)
    url_query_string = models.CharField(null=True, blank=True, max_length=2000)
    url_path = models.CharField(default="/", max_length=500)
    url_file = models.CharField(null=True, blank=True, max_length=255)
    # many to one relationship between URLs and hosts
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    emails = models.ManyToManyField(Email)
    # todo: add more stuff here...

    def __str__(self):
        return self.url
