from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=32)


def create_activation_serializer(base_model):
    class BaseActivationSerializer(serializers.ModelSerializer):
        class Meta:
            model = base_model
            fields = ["title", "is_active", "slug"]

    return BaseActivationSerializer


def create_full_serializer(base_model):
    class BaseFullSerialzier(serializers.ModelSerializer):
        class Meta:
            model = base_model
            fields = "__all__"

    return BaseFullSerialzier