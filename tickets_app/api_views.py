# from rest_framework import response
# from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAuthenticated, ValidationError
from django.db.utils import IntegrityError
from rest_framework.reverse import reverse

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    # IsAuthenticated,
    )
# from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from tickets_app.models import (
    Project,
    Issue,
    Contributor,
    )
from tickets_app.serializers import (
    ProjectSerializer,
    IssueSerializer,
    UserSerializer,
    ContributorSerializer,
    )
from .permissions import (
    ProjectPermissions,
    IsHimself,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this
        view requires.
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
    permission_classes = (ProjectPermissions,)

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.filter(contributors=user.id)
        return queryset


@api_view(['GET', 'POST'])
def contributors(request, project_id=None):
    if not request.user.is_authenticated:
        return NotAuthenticated
    if request.method == 'GET':
        project = get_object_or_404(Project, id=project_id)
        serializer = UserSerializer(project.contributors, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        if not Contributor.objects.filter(
                user_id=request.user.id, project_id=project_id).exists():
            raise ValidationError("You are not a contributor to this project")
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        role = request.POST.get('role')
        permission = request.POST.get('permission')
        asker_contributor = get_object_or_404(
            Contributor, user_id=request.user.id, project_id=project_id)
        # permission attribution depends on the asker own permission
        if permission not in ('CO', 'ST', 'LE'):
            raise ValidationError(
                "Wrong permission value")
        if asker_contributor.permission == 'CO':
            raise ValidationError(
                "Your permission level doesn't allow you to add contributors")
        if asker_contributor.permission == 'ST' and permission == 'LE':
            raise ValidationError(
                "You can not allow such a high permission")
        try:
            contributor = Contributor.objects.create(
                user=user,
                project_id=project_id,
                role=role,
                permission=permission)
        except IntegrityError:
            raise ValidationError("This user is already contributing to the project")
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data)


class IssuesViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
