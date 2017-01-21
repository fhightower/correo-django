from django.db import models


class User(models.Model):
    """Database model for users."""
    emails = models.ManyToManyField("emailanalysis.Email",
                                     verbose_name="related_emails")
    # field = models.ForeignKey("emailanalysis.Email", verbose_name="email", related_name="my_models2")
     # todo: add more fields here...
