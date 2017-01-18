from django.db import models


class Email(models.Model):
    """Database model for handling emails."""
    full_text = models.TextField()
    header = models.TextField()
    body = models.TextField()
    subject = models.CharField(max_length=500)
    recipient_email = models.EmailField()
    recipient_ip = models.GenericIPAddressField()
    sender_email = models.EmailField()
    sender_ip = models.GenericIPAddressField()
    attachment = models.TextField()
    submitter = models.CharField("provider", max_length=8)


class Attachment(models.Model):
    """Attachment class for the attachments' table."""
    file = models.FileField() # todo: add better handling of files with the file field (https://docs.djangoproject.com/en/1.10/topics/files/ and https://docs.djangoproject.com/en/1.10/ref/models/fields/#filefield)
    md5 = models.CharField(max_length=32)
    sha1 = models.CharField(max_length=40)
    sha256 = models.CharField(max_length=64)
    # todo: add more stuff here...
    emails = models.ManyToManyField(Email)


class Host(models.Model):
    """Host class for the hosts' table."""
    # todo: add more stuff here...

    emails = models.ManyToManyField(Email)


class IPAddress(models.Model):
    """Database model for handling IP addresses."""
    # todo: add more stuff here...
    hosts = models.ManyToManyField(Host)
    emails = models.ManyToManyField(Email)


class Url(models.Model):
    """URL class for the URLs' table."""
    # todo: add more stuff here...
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    # many to one relationship between URLs and hosts
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    emails = models.ManyToManyField(Email)
