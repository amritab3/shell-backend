from rest_framework import generics, status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from backend.permissions import IsAdminUser
from .permissions import IsOwner
from .serializers import UserSerializer, UserAdminSerializer, CartSerializer
from .models import User, CartItem, Cart
from apps.product.models import Product, ProductSize


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
        serializer = UserSerializer(user, context={"request": request})

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


class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return super(CartViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

    def get_object(self):
        obj = Cart.objects.get(user=self.request.user)
        return obj

    @action(
        methods=["post"],
        detail=False,
        url_path="add-item",
        url_name="add-item",
    )
    def add_item_to_cart(self, request, *args, **kwargs):
        user_id = kwargs.get("userId")
        data = request.data

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "User Does Not Exist"},
            )

        try:
            product = Product.objects.get(id=data["product"])
        except Product.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "Product you are trying to add does not exist"
                },
            )

        try:
            product_size = ProductSize.objects.get(
                product=product, size=data["size"]
            )
            if product_size.size_inventory < data["quantity"]:
                return Response(
                    {
                        "message": f"Quantity exceeded the inventory size for {product.name} size {data['size']}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ProductSize.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "Product Size you are trying to add does not exist"
                },
            )

        cart, created = Cart.objects.get_or_create(user=user)

        if not created:
            cart_item = CartItem.objects.get(
                product=product, cart=cart, size=data["size"]
            )
            cart_item.quantity = data["quantity"]
            cart_item.save()

        else:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=data["quantity"],
                size=data["size"],
            )

        serializer = CartSerializer(cart)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path="user-cart",
        url_name="user-cart",
    )
    def get_user_cart(self, request, *args, **kwargs):
        user_id = kwargs.get("userId")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "User Does Not Exist"},
            )

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Cart not found for user"},
            )

        serializer = CartSerializer(cart)

        return Response(
            status=status.HTTP_200_OK, data=serializer.data["cart_items"]
        )
