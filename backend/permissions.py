from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with admin role.
    """

    def has_permission(self, request, view):
        # Check if the user has the required role
        return request.user.roles.filter(name="Admin").exists()


class IsOwner(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object
        return obj == request.user
