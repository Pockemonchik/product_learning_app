import logging
from rest_framework.response import Response
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from product_learning.models import Teacher, Student


logger = logging.getLogger(__name__)


class AuthView(ObtainAuthToken):
    """Класс для авторизации пользователя"""

    @swagger_auto_schema(responses={200: UserSerializer}, request_body=UserSerializer)
    def post(self, request):
        """Авторизация пользователя"""
        # проверяем валидность данных
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        req_user = serializer.validated_data["username"]
        req_pass = serializer.validated_data["password"]
        # если пользователь есть в базе то проверяем пароль и выдаем токен
        user = User.objects.filter(username=req_user).first()
        if user:
            auth = authenticate(username=req_user, password=req_pass)
            if auth is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            else:
                return JsonResponse({"error": "Неверный пароль"}, status=400)


class RegistrationView(ObtainAuthToken):
    """Класс для регистрации пользователя"""

    @swagger_auto_schema(responses={200: UserSerializer}, request_body=CreateUserSerializer)
    def post(self, request):
        """Регистраци пользователя"""
        # проверяем валидность данных
        print("request.data", request.data)
        serializer = CreateUserSerializer(
            data=request.data, context={"request": request}
        )
        print("serializer", serializer.is_valid(raise_exception=True))
        serializer.is_valid(raise_exception=True)
        req_user = serializer.validated_data["username"]
        req_pass = serializer.validated_data["password"]
        # если пользователь есть в базе то проверяем пароль и выдаем токен
        user = User.objects.filter(username=req_user).first()
        if user:
            return JsonResponse(
                {"error": "Пользователь с таким логном уже зарегистрирован"}, status=400
            )
        # создание пользователя
        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        # создание студента
        print("serializer.validated_data",serializer.validated_data)
        if serializer.validated_data["role"] == "student":
            Student.objects.create(user=user)
        elif serializer.validated_data["role"] == "teacher":
            Teacher.objects.create(user=user)
        # создание преподавтеля
        auth = authenticate(username=req_user, password=req_pass)
        if auth is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return JsonResponse({"error": "Неверный пароль"}, status=400)
