from rest_framework import serializers

from .models import User, Role, Cart, CartItem
from apps.product.models import Product
from apps.product.serializers import ProductSerializer, ProductImageSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "mobile_no",
            "avatar",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save(validated_data)
        return user


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile_no",
            "gender",
            "roles",
        ]

    def create(self, validated_data):
        uploaded_roles = validated_data.pop("roles")
        user = User.objects.create(**validated_data)
        user.roles.set(uploaded_roles)
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class ProductSerializerForCart(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "images"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerForCart()

    class Meta:
        model = CartItem
        fields = ["id", "product", "size", "quantity", "cart"]
        extra_kwargs = {"cart": {"write_only": True}}


class UploadedCartItemsSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)
    size = serializers.CharField(required=True, max_length=5)
    quantity = serializers.IntegerField(required=True, min_value=1)


class CartSerializer(serializers.ModelSerializer):
    uploaded_cart_items = serializers.ListField(
        child=UploadedCartItemsSerializer(), write_only=True
    )
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "uploaded_cart_items", "cart_items"]
        extra_kwargs = {"user": {"write_only": True}}

    def create(self, validated_data):
        uploaded_cart_items = validated_data.pop("uploaded_cart_items")

        cart = Cart.objects.create(**validated_data)

        for item in uploaded_cart_items:
            try:
                product = Product.objects.get(id=item["product"])
            except Product.DoesNotExist:
                product = None
            CartItem.objects.create(
                cart=cart,
                product=product,
                size=item["size"],
                quantity=item["quantity"],
            )

        return cart
