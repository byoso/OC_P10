from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from .models import Contributor
from project_SoftDesk.tools import get_params_from_request
from .models import Issue


CONTRIB_LEVEL = {
    'CO': 1,
    'ST': 2,
    'LE': 3
}


class IsHimself(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ('create', 'list', 'retrieve'):
            return True
        if view.action in ('update', 'partial_update', 'destroy'):
            if request.user.id == obj.pk:
                return True


class ProjectPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if view.action == 'update' and request.user.is_authenticated:
            contributor = get_object_or_404(
                Contributor, user_id=request.user.id, project_id=obj.id)
            if contributor.permission in ["ST", "LE"]:
                return True
            return True
        if view.action == 'list' and request.user.is_authenticated:
            return True
        if view.action == 'retrieve' and request.user.is_authenticated:
            return True
        if view.action == 'create' and request.user.is_authenticated:
            return True
        if view.action == 'destroy' and request.user.is_authenticated:
            contributor = get_object_or_404(
                Contributor, user_id=request.user.id, project_id=obj.id)
            if contributor.permission == "LE":
                return True


class CommentPermissions(BasePermission):

    def has_permission(self, request, view):
        params = get_params_from_request(request)
        request.user.is_contributor_or_denied(params[0])
        issue = get_object_or_404(Issue, id=params[1])
        issue.is_in_project_or_denied(params[0])
        return True

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
