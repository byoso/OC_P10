from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from tickets_app.models import Project, Ticket
from tickets_app.serializers import ProjectSerializer, TicketSerializer


class ProjectViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectSerializer

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
