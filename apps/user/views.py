from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import APIException


from .serializers import UserSerializer

# from .permissions import UserPermission
from .models import User


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")


class ListUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetrieveUpdateDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
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
        raise APIException({"detail": "Password cannot be updated."})
