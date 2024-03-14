from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "You do not have permission to perform this action."
    print("First Print")

    def has_object_permission(self, request, view, obj):
        print("Second Print")
        print("obj", obj)
        print("req", request.user)
        # Check if the user is the owner of the object
        return obj == request.user
