from django.db import models
# from django.contrib.auth import get_user_model


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
        "authentication.User",
        on_delete=models.CASCADE, null=True)
    contributors = models.ManyToManyField(
        "authentication.User", related_name="contributing")

    def __repr__(self):
        return f"<{self.title}>"

    def __str__(self):
        return self.title


class Issue(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=255)
    project = models.ForeignKey(
        "tickets_app.Project",
        on_delete=models.CASCADE,
        related_name="issues"
        )
    referent = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f"<{self.title}>"

    def __str__(self):
        return self.title
