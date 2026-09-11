from .serializers import UserRegisterSerializer, ConfirmSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import random
from rest_framework.views import APIView

from users.models import ConfirmationCode

def generate_code():
    return str(random.randint(100000, 999999))

class AuthorizationAPIView(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create_user(
            username=username,
            password=password,
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

class ConfirmAPIView(APIView):

    def post(self, request):
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
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # step 2: create user
    user = User.objects.create_user(
        username=username,
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

