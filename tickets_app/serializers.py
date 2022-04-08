from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


from tickets_app.models import Projects, Issues

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
                validated_data['username'])
        user.set_password(
                validated_data['password'])
        user.save()
        return user


class ProjectsSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'title', 'author', 'description', 'tickets']


class IssuesSerializer(ModelSerializer):

    class Meta:
        model = Issues
        fields = ['id', 'title', 'description', 'referent', 'project']
