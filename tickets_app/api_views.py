from rest_framework.viewsets import (
    ModelViewSet,
    )
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,)
from rest_framework import permissions
from django.contrib.auth import get_user_model

from tickets_app.models import Project, Issue
from tickets_app.serializers import (
    ProjectSerializer,
    IssueSerializer,
    UserSerializer,
    )
from .permissions import (
    IsContributor,
    IsAuthor,
    IsHimself,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = (IsHimself,)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('destroy', 'update', 'partial_update'):
            permission_classes = [IsHimself, ]
        else:
            if self.action in ('list', 'retrieve',):
                permission_classes = [IsAuthenticatedOrReadOnly, ]
            else:
                permission_classes = []
        return [permission() for permission in permission_classes]


class ProjectsViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsContributor,
        IsAuthor,
        )

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


class IssuesViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
