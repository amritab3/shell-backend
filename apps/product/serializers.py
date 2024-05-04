from rest_framework import serializers

from .models import Product, ProductSize, ProductImage, CartItem, Cart


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["id", "size", "size_inventory", "product"]


class UploadedSizesSerializer(serializers.Serializer):
    size = serializers.CharField(allow_blank=True, default="")
    size_inventory = serializers.IntegerField(default=0)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductSerializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True, read_only=True)
    uploaded_sizes = serializers.ListField(
        child=UploadedSizesSerializer(many=True), write_only=True
    )

    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "inventory",
            "color",
            "style",
            "material",
            "category",
            "sizes",
            "gender",
            "uploaded_sizes",
            "images",
            "uploaded_images",
        ]

    def create(self, validated_data):
        uploaded_sizes = validated_data.pop("uploaded_sizes")
        uploaded_images = validated_data.pop("uploaded_images")

        total_inventory = sum(
            item["size_inventory"] for item in uploaded_sizes[0]
        )
        validated_data["inventory"] = total_inventory

        product = Product.objects.create(**validated_data)

        for each_size in uploaded_sizes[0]:
            ProductSize.objects.create(
                product=product,
                size_inventory=each_size["size_inventory"],
                size=each_size["size"],
            )

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "size", "quantity", "cart"]


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
