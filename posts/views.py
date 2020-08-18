from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Like
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status


class PostsViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(responses={204: ""}, methods=['post', 'delete'])
    @action(detail=True, methods=['POST', 'DELETE'], permission_classes=[IsAuthenticated], serializer_class=None)
    def like(self, request, pk, *args, **kwargs):
        """Set like for Comment or Unlike if Like already exists."""
        if request.method == 'POST':
            Like.objects.get_or_create(user=self.request.user, post_id=pk)
        else:
            Like.objects.filter(user=self.request.user, post_id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


