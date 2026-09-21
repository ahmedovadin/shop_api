from .serializers import (
    UserRegisterSerializer, 
    ConfirmSerializer,
    AuthValidateSerializer
)
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import random
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from users.models import ConfirmationCode, CustomUser

def generate_code():
    return str(random.randint(100000, 999999))

class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer

    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'User credentials are wrong!'}
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data.get('phone_number')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            is_active=False
        )

        code = generate_code()
        ConfirmationCode.objects.create(user=user, code=code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code,
            }
        )

class ConfirmAPIView(CreateAPIView):
    serializer_class = ConfirmSerializer

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        try:
            confirmation = ConfirmationCode.objects.get(code=code)
        except ConfirmationCode.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Неверный код подтверждения'}
            )

        user = confirmation.user
        user.is_active = True
        user.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'Пользователь успешно активирован, можно авторизоваться',
            }
        )

@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registration_api_view(request):
    # step 0: validation
    serializer = UserRegisterSerializer(data=request.data)
    
    serializer.is_valid(raise_exception=True)

    # step 1: receive data
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    # step 2: create user
    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        is_active=False
    )

    code = generate_code()
    ConfirmationCode.objects.create(user=user, code=code)

    # step 3: return response
    return Response(status=status.HTTP_201_CREATED, data={
        'user_id': user.id,
        'confirmation_code': code
    })


from users.serializers import UserRegisterSerializer, ConfirmSerializer


@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    code = serializer.validated_data['code']

    try:
        confirmation = ConfirmationCode.objects.get(code=code)
    except ConfirmationCode.DoesNotExist:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Неверный код подтверждения'}
        )

    user = confirmation.user
    user.is_active = True
    user.save()

    return Response(
        status=status.HTTP_200_OK,
        data={
            'message': 'Пользователь успешно активирован, можно авторизоваться',
        }
    )

