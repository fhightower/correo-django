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
