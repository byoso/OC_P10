from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # FK 'tickets' to tickets_app Ticket
    # FK 'projectss' to tickets_app Project
    pass
