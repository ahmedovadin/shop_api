from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField

from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class OauthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_staff"] = user.is_staff

        if user.birthdate:
            token["birthdate"] = user.birthdate.isoformat()
        else:
            token["birthdate"] = None

        return token

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserRegisterSerializer(UserBaseSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = PhoneNumberField(required=False, region='KG')
    birth_date = serializers.DateField(required=False) 

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('User already exists!')

class AuthValidateSerializer(UserBaseSerializer):
    pass

class ConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)