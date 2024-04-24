from rest_framework import serializers

from .models import Product, ProductSize


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["id", "size", "size_inventory", "product"]


class UploadedSizesSerializer(serializers.Serializer):
    size = serializers.CharField(allow_blank=True, default="")
    size_inventory = serializers.IntegerField(default=0)


class ProductSerializer(serializers.ModelSerializer):
    sizes = ProductSizeSerializer(many=True, read_only=True)
    uploaded_sizes = serializers.ListField(
        child=UploadedSizesSerializer(), write_only=True
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
        ]

    def create(self, validated_data):
        uploaded_sizes = validated_data.pop("uploaded_sizes")

        total_inventory = sum(
            item["size_inventory"] for item in uploaded_sizes
        )
        validated_data["inventory"] = total_inventory
        product = Product.objects.create(**validated_data)
        for each_size in uploaded_sizes:
            ProductSize.objects.create(
                product=product,
                size_inventory=each_size["size_inventory"],
                size=each_size["size"],
            )

        return product
