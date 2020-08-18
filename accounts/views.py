from datetime import datetime, timezone

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import LoginSerializer, CurrentUserSerializer, RegistrationSerializer, \
    ResponseUserActivitySerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(responses={200: "{'refresh': 'token', 'access': 'token', 'user': {} }"})
    def post(self, request, *args, **kwargs):
        """Login User using email and password"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        user.last_login = datetime.now(timezone.utc)
        user.save()

        response = {
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': CurrentUserSerializer(user).data,
        }

        return Response(status=status.HTTP_200_OK, data=response)


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(responses={204: ""})
    def post(self, request, *args, **kwargs):
        """Register new User"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActivityView(generics.RetrieveAPIView):
    """Get activity info for specific user"""
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ResponseUserActivitySerializer
