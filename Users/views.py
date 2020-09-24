from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.decorators import api_view
from . import redis_setup
import jwt
import datetime
import redis
from .redis_setup import get_redis_instance
from .tasks import send_notification
from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import exceptions


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
