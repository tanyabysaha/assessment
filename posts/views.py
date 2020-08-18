from django.db.models import DateField, Count
from django.db.models.functions import Cast
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Like
from posts.serializers import PostSerializer, LikeAnalyticsSerializer, ResponseLikeAnalyticsSerializer
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


class LikeAnalyticsView(APIView):
    """Get analytics info for specific date range"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        base = Like.objects.annotate(created=Cast('created_at', output_field=DateField()))\
            .filter(created__range=(self.request.query_params.get('date_from'), self.request.query_params.get('date_to')))\
            .values('post').annotate(likes=Count('pk'))
        return base

    @swagger_auto_schema(request_body=None, responses={200: ResponseLikeAnalyticsSerializer}, query_serializer=LikeAnalyticsSerializer)
    def get(self, request, *args, **kwargs):
        return Response(self.get_queryset())
