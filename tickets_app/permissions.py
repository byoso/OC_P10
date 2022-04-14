from rest_framework.permissions import BasePermission


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
            return True
        if view.action == 'list' and request.user.is_authenticated:
            return True
        if view.action == 'retrieve' and request.user.is_authenticated:
            return True
        if view.action == 'create' and request.user.is_authenticated:
            return True
        if view.action == 'delete' and request.user.is_authenticated:
            if request.user == obj.author:
                return True
