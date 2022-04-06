from rest_framework.permissions import BasePermission


class IsHimself(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ('create', 'list', 'retrieve'):
            return True
        if view.action in ('update', 'partial_update', 'destroy'):
            if request.user.id == obj.pk:
                return True


class IsContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'delete':
            return False
        contributors = obj.contributors
        if request.user in contributors:
            return True


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
