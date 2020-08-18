from rest_framework.routers import DefaultRouter

from posts.views import PostsViewSet

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')

urlpatterns = [
]

urlpatterns += router.urls
