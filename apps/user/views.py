from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .serializers import UserSerializer

# from .permissions import UserPermission
from .models import User


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")
