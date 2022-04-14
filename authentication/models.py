from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    # FK 'issues' to tickets_app Issue
    # FK 'projects' to tickets_app Project

    def __str__(self):
        return f"<User {self.id}: {self.username}>"
