"""assessment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from assessment import SWAGGER_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('posts.urls')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Test API",
      default_version='v1',
      description="Test description",
      contact=openapi.Contact(email="tanyabysaha@gmail.com"),
      license=openapi.License(name="BSD License"),
      authentication_classes='rest_framework_simplejwt.authentication.JWTAuthentication'
   ),
   url=SWAGGER_URL,
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
