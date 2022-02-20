from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Signup Serializer
    """

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    token = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username",
                  "email", "token")

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Public Profile Serializer
    """

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username",
                  "email")


class UserLoginSerializer(serializers.Serializer):
    """
    User Login Serializer
    """

    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                msg = _('User doesnot exist.')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = _('You haven’t verified your email yet.')
                raise serializers.ValidationError(msg, code='authorization')

            user = authenticate(request=self.context.get('request'),
                                username=user.username, password=password)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
