from rest_framework.routers import DefaultRouter
from django.urls import path

from posts.views import PostsViewSet, LikeAnalyticsView

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')

urlpatterns = [
    path('analytics/', LikeAnalyticsView.as_view(), name='like-analytics'),
]

urlpatterns += router.urls
