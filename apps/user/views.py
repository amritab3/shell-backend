from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from backend.permissions import IsAdminUser
from .permissions import IsOwner


from .serializers import UserSerializer

# from .permissions import UserPermission
from .models import User


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")


class ListUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class RetrieveUpdateDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    # Permission classes for various methods
    permission_classes_by_method = {
        "get": [IsAuthenticated, IsOwner],  # Permission for retrieve (GET)
        "put": [IsAuthenticated, IsOwner],  # Permission for update (PUT)
        "patch": [
            IsAuthenticated,
            IsOwner,
        ],  # Permission for partial update (PATCH)
        "delete": [IsAuthenticated, IsOwner],  # Permission for delete (DELETE)
    }

    def get_permissions(self):
        # Return the appropriate permission_classes based on the request method
        return [
            permission()
            for permission in self.permission_classes_by_method.get(
                self.request.method.lower(), [IsAuthenticated]
            )
        ]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        self.check_object_permissions(request, user)
        user.delete()
        return Response("User deleted", status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        validate_request(request)
        user = get_object_or_404(User, pk=kwargs["pk"])
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def validate_request(request):
    if "password" in request.data:
        raise APIException({"detail": "Password cannot be updated from here."})


class ListRolesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
