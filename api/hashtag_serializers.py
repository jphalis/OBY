from rest_framework import serializers

from hashtags.models import Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = [
            'id',
            'tag',
        ]
