from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import (
    NotAuthenticated,
    ValidationError,
    PermissionDenied)
from django.db.utils import IntegrityError

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    )
from django.contrib.auth import get_user_model

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
    CONTRIB_LEVEL,
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
        # check if the asker is himself contributing to the project
        if not Contributor.objects.filter(
                user_id=request.user.id, project_id=project_id).exists():
            raise PermissionDenied("You are not a contributor to this project")
        # get the datas from form
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        role = request.POST.get('role')
        permission = request.POST.get('permission')

        # permission attribution depends on the asker's own permission:
        asker_contributor = get_object_or_404(
            Contributor, user_id=request.user.id, project_id=project_id)
        if permission not in ('CO', 'ST', 'LE'):
            raise ValidationError(
                "Wrong permission value")
        if asker_contributor.permission == 'CO':
            raise PermissionDenied(
                "Your permission level doesn't allow you to add contributors")
        if asker_contributor.permission == 'ST' and permission == 'LE':
            raise PermissionDenied(
                "You can not allow such a high permission")
        try:
            contributor = Contributor.objects.create(
                user=user,
                project_id=project_id,
                role=role,
                permission=permission)
        except IntegrityError:  # contributor already exists
            raise ValidationError(
                "This user is already contributing to the project")
        data = ContributorSerializer(contributor).data
        return Response(data)


class ContributorDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id, user_id):
        asker = request.user
        asker_contributor = get_object_or_404(
            Contributor, user_id=asker.id, project_id=project_id)
        user_contributor = get_object_or_404(
            Contributor, user_id=user_id, project_id=project_id)
        # asker of deletion must have higher contribution permission
        # level to be allowed to delete the asked contributor
        if CONTRIB_LEVEL[asker_contributor.permission] > \
                CONTRIB_LEVEL[user_contributor.permission]:
            user_contributor.delete()
            return Response("Contributor successfully deleted")
        else:
            raise PermissionDenied("Your contribution level is too low")


class GetPostIssues(APIView):
    permisson_classes = [IsAuthenticated]

    def get(self, request, project_id=None):
        request.user.is_contributor_or_denied(project_id)
        issues = IssueSerializer(Issue.objects.all(), many=True).data
        return Response(issues)

    def post(self, request, project_id=None):
        request.user.is_contributor_or_denied(project_id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        tag = request.POST.get('tag')
        priority = request.POST.get('priority')
        project = get_object_or_404(Project, id=project_id)
        author = request.user
        assignee_id = request.POST.get('assignee_id')
        if assignee_id != '' and assignee_id is not None:
            assignee = get_object_or_404(User, id=assignee_id)
            if not assignee.is_contributor(project_id):
                raise ValidationError("the assignee is not a contributor")
        else:
            assignee = None

        Issue.objects.create(
            title=title,
            description=description,
            tag=tag,
            priority=priority,
            project=project,
            author=author,
            assignee=assignee,
        )
        return Response("Issue successfully created")


class UpdateDeleteIssues(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, issue_id):
        request.user.is_issue_author_or_denied(issue_id)
        issue = get_object_or_404(Issue, id=issue_id)
        issue.title = request.POST.get('title')
        issue.description = request.POST.get('description')
        issue.tag = request.POST.get('tag')
        issue.priority = request.POST.get('priority')
        assignee_id = request.POST.get('assignee_id')
        if assignee_id != '' and assignee_id is not None:
            assignee = get_object_or_404(User, id=assignee_id)
            if not assignee.is_contributor(project_id):
                raise ValidationError("the assignee is not a contributor")
            issue.assignee_id = request.POST.get('assignee_id')
        else:
            assignee = None
        issue.save()
        return Response("Issue successfully updated")

    def delete(self, request, project_id, issue_id):
        request.user.is_issue_author_or_denied(issue_id)
        issue = get_object_or_404(Issue, id=issue_id)
        issue.delete()
        return Response("Issue successfully deleted")
