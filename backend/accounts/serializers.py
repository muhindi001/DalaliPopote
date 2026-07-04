from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            'id','username','email','phone','role','password'
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            phone=validated_data['phone']
        )

        return user


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=False, allow_blank=True, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True, write_only=True)

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].allow_blank = True
        self.fields['email'].required = False
        self.fields['email'].allow_blank = True

    def validate(self, attrs):
        identifier = attrs.get("username") or attrs.get("email")
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError({
                "detail": "Please provide either an email or username and a password."
            })

        user = self.get_user(identifier)
        if user is None or not user.check_password(password):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        if not user.is_active:
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        self.user = user
        data = self.user_token_payload(user)
        token, _ = Token.objects.get_or_create(user=user)
        data["token"] = token.key
        return data

    def get_user(self, identifier):
        user_model = get_user_model()
        if "@" in identifier:
            return user_model.objects.filter(email__iexact=identifier).first()
        return user_model.objects.filter(username__iexact=identifier).first()

    def user_token_payload(self, user):
        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }