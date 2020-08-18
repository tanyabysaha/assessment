from rest_framework import serializers

from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Serializer for post"""

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}


class LikeAnalyticsSerializer(serializers.Serializer):
    """Serializer for query parameters like analytics"""

    date_from = serializers.DateField()
    date_to = serializers.DateField()


class ResponseLikeAnalyticsSerializer(serializers.Serializer):
    """Serializer for response like analytics"""

    post = serializers.UUIDField()
    likes = serializers.IntegerField()
