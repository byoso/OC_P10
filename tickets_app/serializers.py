from rest_framework.serializers import ModelSerializer

from tickets_app.models import Project, Ticket


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'author', 'description', 'tickets']


class TicketSerializer(ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'referent', 'project']
