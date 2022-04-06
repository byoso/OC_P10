from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from tickets_app.models import Project, Ticket
from tickets_app.serializers import ProjectSerializer, TicketSerializer
from .permissions import (
    IsContributor,
    IsAuthor,
)


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsContributor,
        IsAuthor,
        )

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


class TicketViewset(ModelViewSet):

    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
