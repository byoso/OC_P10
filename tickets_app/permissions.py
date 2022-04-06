from rest_framework.permissions import BasePermission


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
