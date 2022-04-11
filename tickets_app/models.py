from django.db import models
from django.conf import settings


class Project(models.Model):
    TYPE_CHOICES = [
        ("FE", "FRONT-END"),
        ("BE", "BACK-END"),
        ("IO", "IOS"),
        ("AN", "ANDROID"),
    ]
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Contributor',
        related_name="contributing",
        )

    def __str__(self):
        return f"<project {self.id}:{self.title}>"


class Issue(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=255, null=True)
    tag = models.CharField(max_length=16, null=True)
    priority = models.CharField(max_length=16, null=True)
    project = models.ForeignKey(
        "tickets_app.Project",
        on_delete=models.CASCADE,
        related_name="issues"
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, related_name="written_issues")
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
        related_name="assignee_to_issues")
    created_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"<Issue {self.id}:{self.title}>"


class Comment(models.Model):
    description = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(
        'tickets_app.Issue',
        on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"<Comment {self.id}: author:{self.author}>"


class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='contributing_users', null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='projects',
        null=True)
    # TODO: permission (choicefield)
    role = models.CharField(max_length=80, null=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return (f"<Contributor {self.user.id}:{self.user.username}"
                f" on project {self.project.id}:{self.project.title}>")
