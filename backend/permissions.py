from rest_framework import permissions


class HasAdminRole(permissions.BasePermission):
    """
    Custom permission to only allow users with admin role.
    """

    def has_permission(self, request, view):
        # Check if the user has the required role
        return request.user.roles.filter(name="Admin").exists()
