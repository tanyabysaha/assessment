from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Serializer for Login using email number and password"""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError({"email": "User is not found"})
        if not user.check_password(data['password']):
            raise serializers.ValidationError({"password": "Password is not correct"})

        data['user'] = user

        return data


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)

        return new_user


class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer for Current User"""

    class Meta:
        model = User
        exclude = ('password', 'last_login')
        read_only_fields = ('email',)