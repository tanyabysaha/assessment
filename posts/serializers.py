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
