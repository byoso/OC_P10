from django.db import models
from django.contrib.auth.models import AbstractUser
from tickets_app.models import Contributor
from rest_framework.exceptions import PermissionDenied


class User(AbstractUser):
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    # FK 'issues' to tickets_app Issue
    # FK 'projects' to tickets_app Project

    def __str__(self):
        return f"<User {self.id}: {self.username}>"

    def is_contributor(self, project_id) -> bool:
        return Contributor.objects.filter(
            user_id=self.id, project_id=project_id).exists()

    def is_contributor_or_denied(self, project_id):
        """Check if user is a contributor to a project"""
        if not self.is_contributor(project_id):
            raise PermissionDenied(
                "you are not contributing to this project")

    def get_contributor(self, project_id):
        contributor = Contributor.objects.filter(
            user_id=self.id, project_id=project_id)
        return contributor
