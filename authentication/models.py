from django.db import models
from django.contrib.auth.models import AbstractUser
from tickets_app.models import Contributor, Issue, Comment
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
                "You are not contributing to this project")

    def is_issue_author(self, issue_id) -> bool:
        return Issue.objects.filter(id=issue_id, author=self).exists()

    def is_issue_author_or_denied(self, issue_id):
        if not self.is_issue_author(issue_id):
            raise PermissionDenied(
                "You are not the author of this issue."
            )

    def get_contributor(self, project_id):
        contributor = Contributor.objects.filter(
            user_id=self.id, project_id=project_id)
        return contributor
