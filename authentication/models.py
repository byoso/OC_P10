from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    # FK 'tickets' to tickets_app Ticket
    # FK 'projectss' to tickets_app Project
    pass
