from .models import User, Role
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

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
            "avatar_url",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_avatar_url(self, user):
        request = self.context.get("request")
        avatar_url = user.avatar
        return request.build_absolute_uri(avatar_url)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save(validated_data)
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]
