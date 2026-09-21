from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField

from users.models import CustomUser 

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserRegisterSerializer(UserBaseSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = PhoneNumberField(required=False, region='KG')


    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('User already exists!')

class AuthValidateSerializer(UserBaseSerializer):
    pass

class ConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)