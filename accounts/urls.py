from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LoginView, RegistrationView, UserActivityView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='user-login'),
    path('auth/register/', RegistrationView.as_view(), name='user-register'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user-activity/<pk>/', UserActivityView.as_view(), name='user-activity'),

]
