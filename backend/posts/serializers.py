from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """ Returns: ("title", "slug", "body", "pub_date", "last_modify", "user") """

    class Meta:
        model = Post
        exclude = ["id", "is_active", "summary"]
        read_only_fields = ["slug", "pub_date", "last_modify", "user"]

    def update(self, instance, validated_data):
        instance.is_active = False
        return super().update(instance, validated_data)


class PostManagerSerializer(serializers.ModelSerializer):
    """ Returns: ("title", "slug", "body", "pub_date",
        "last_modify", "summary", "user") """

    class Meta:
        model = Post
        exclude = ["id", "is_active"]
        read_only_fields = ["slug", "last_modify", "user"]

    def update(self, instance, validated_data):
        instance.is_active = False
        return super().update(instance, validated_data)


class PostOverviewSerializer(serializers.ModelSerializer):
    """ Returns: ("title", "slug", "pub_date", "summary", "user") """

    class Meta:
        model = Post
        exclude = ["id", "is_active", "body", "last_modify",]