from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from project_SoftDesk.tools import expected_values
import traceback

from tickets_app.models import (
    Project,
    Issue,
    Contributor,
)

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
        rules = [
            ('username', lambda x: len(x) > 4),
            ('first_name', lambda x: x == '' or len(x) > 1),
            ('last_name', lambda x: x == '' or len(x) > 1),
            ('email', lambda x: x == '' or ("@" in x and len(x) > 5)),

        ]
        if expected_values(data, *rules):
            return data
        raise serializers.ValidationError('Unexpected values recieved')

    def create(self, validated_data):
        """For creation, only username and password are required,
        the other attributes are optionnal."""
        if 'first_name' not in validated_data:
            validated_data['first_name'] = None
        if 'last_name' not in validated_data:
            validated_data['last_name'] = None
        if 'email' not in validated_data:
            validated_data['email'] = None
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
            traceback.print_exc()
            raise serializers.ValidationError('a required field is missing')


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'type', 'author',
            'contributors', 'issues']

    def get_request_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return user

    def create(self, validated_data):
        user = self.get_request_user()
        try:
            project = Project.objects.create(
                    title=validated_data['title'],
                    description=validated_data['description'],
                    type=validated_data['type'],
                    author=user,
                    )
            contributor = Contributor()
            contributor.user = user
            contributor.project = project
            contributor.permission = "LE"
            contributor.save()
            project.save()
            return project
        except KeyError:
            traceback.print_exc()
            raise serializers.ValidationError(
                'a required field is missing')

    def update(self, instance, validated_data):
        user = self.get_request_user()
        contributor = get_object_or_404(Contributor, user_id=user.id)
        if contributor.permission == "CO":
            raise serializers.ValidationError(
                "You don't have the permission to do that")
        if validated_data['title'] != '':
            instance.title = validated_data['title']
        if validated_data['description'] != '':
            instance.description = validated_data['description']
        # import pdb; pdb.set_trace()
        for choice in instance.TYPE_CHOICES:
            if validated_data['type'] == choice[0]:
                instance.type = validated_data['type']
        instance.save()
        return instance

    def delete(self, instance):
        print("=== delete")


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'assignee', 'project']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'role', 'permission']
