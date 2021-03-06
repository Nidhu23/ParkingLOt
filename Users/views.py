from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from .models import User
from ParkingLotSystem import settings
from rest_framework.decorators import api_view
from . import redis_setup
from .utils import get_user
import jwt
from jwt import DecodeError
import datetime
import redis
from .redis_setup import get_redis_instance
from .tasks import send_notification
from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import exceptions
import logging
logger = logging.getLogger('django')


# Create your views here.
@api_view(['POST'])
def register(request):
    ''' 
    API that registers users to parkinglot and sends a email notification on successfull registration

    Parameters:
    argument(1):request paramter: having username,role,email,password

    Returns:
    registers user and returns status code and message
    '''
    try:
        user_email = request.data['email']
        user_name = request.data['username']
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_notification.delay(user_email, user_name)
            return Response(data={"SUCCESSFULLY REGISTERED"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(exception=True,
                        data={"status": status.HTTP_400_BAD_REQUEST})


@api_view(['POST'])
def login(request):
    ''' 
    API for user to login to the parking lot system

    Parameters:
    argument(1):request paramter: having username,password

    Returns:
    create access token and returns status code and message
    '''
    try:
        redis_instance = redis_setup.get_redis_instance()
        username = request.data.get('username')
        password = request.data.get('password')
        if (username is None) or (password is None):
            return Response("username and password required",
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=username)
        if (user is None):
            return Response("username required",
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response("wrong password entered",
                            status=status.HTTP_400_BAD_REQUEST)
        access_token_payload = {'username': 'login_' + user.username}
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY)
        redis_instance.set('login_' + username, access_token)
        return Response("LOGIN SUCCESSFULL",
                        headers={'token': access_token},
                        status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response("user not registered,please register",
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return Response("Login Error",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def logout(request):
    ''' 
    Logout function

    Parameters:
    argument(1):request paramter: token in request header

    Returns:
    deletes the user from redis 
    '''
    try:
        redis_instance = get_redis_instance()
        user = get_user(request.headers.get('token'))
        if redis_instance.delete(user) > 0:
            return Response("logged out successfully", status=status.HTTP_200_OK)
        return Response("Please login first",status=status.HTTP_404_NOT_FOUND)
    except DecodeError:
        return Response("You are not logged in",
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as exception:
        logger.error(exception)
        return Response("Could not log you out",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
