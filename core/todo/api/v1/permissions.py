from rest_framework import permissions


class IsAuthenticatedOwner(permissions.IsAuthenticated):
    """
    Object-level permission to only allow owners of an object to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner.user == request.user
