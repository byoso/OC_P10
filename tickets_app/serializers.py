from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from project_SoftDesk.tools import check_type, expected_values


from tickets_app.models import Project, Issue

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'written_issues',
            'assignee_to_issues',
            'contributing')
        extra_kwargs = {
            'password': {'write_only': True},
            'written_issues': {'read_only': True},
            'assignee_to_issues': {'read_only': True},
            'contributing': {'read_only': True},
        }

    def validate(self, data):
        checkers = [
            ('username', lambda x: len(x) > 4),
            ('first_name', lambda x: x == '' or len(x) > 1),
            ('last_name', lambda x: x == '' or len(x) > 1),
            ('email', lambda x: x == '' or ("@" in x and len(x) > 5)),

        ]
        if expected_values(data, *checkers):
            return data
        raise serializers.ValidationError('Unexpected values recieved')

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    )
            user.set_password(
                    validated_data['password'])
            user.save()
            return user
        except KeyError:
            raise serializers.ValidationError('a required field is missing')


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'author', 'description', 'issues']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'assignee', 'project']
