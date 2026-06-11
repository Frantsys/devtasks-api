from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        help_text="Senha do usuário (write-only).",
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password", "group",
            "is_active", "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "is_deleted", "created_at", "updated_at"]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "group",
            "is_active", "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = fields
