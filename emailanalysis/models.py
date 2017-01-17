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
    # todo: add more stuff here...
    emails = models.ManyToManyField(Email)


class Host(models.Model):
    """Host class for the hosts' table."""
    # todo: add more stuff here...
    emails = models.ManyToManyField(Email)


class Url(models.Model):
    """URL class for the URLs' table."""
    # todo: add more stuff here...
    emails = models.ManyToManyField(Email)
