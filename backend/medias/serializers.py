from rest_framework import serializers

from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ["post", "slug", "id"]

    def update(self, instance, validated_data):
        instance.is_active = False
        return super().update(instance, validated_data)