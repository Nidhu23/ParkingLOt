from rest_framework.response import Response
from rest_framework import status
import rest_framework
from Users.models import User
from Users.redis_setup import get_redis_instance
from ParkingLotSystem import settings
import jwt
import logging
from rest_framework import request
logger = logging.getLogger('django')


def jwt_decode(view_func):
    def wrap(request, *args, **kwargs):
        try:
            print(request.headers.get('token'))
            print(settings.SECRET_KEY)
            payload = jwt.decode(request.headers.get('token'),
                                 settings.SECRET_KEY)
            username = payload.get('username')
            redis_instance = get_redis_instance()
            if redis_instance.exists(username) > 0:
                return view_func(request, *args, **kwargs)
            else:
                return Response("You are not logged in, Please login",
                                status=status.HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError:
            return Response("Please login again",
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            logger.error("Invalid token passed")
            return Response("Login failed", status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            logger.error("Login Exception", exception)
            return Response(exception=True,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrap


def role_required(roles_allowed=[]):
    def check_permission(view_func):
        def wrap(request, *args, **kwargs):
            try:
                user = jwt.decode(request.headers.get('token'),
                                  settings.SECRET_KEY)
                username = user.get('username').split("_", 1)
                print(username[1])
                user_details = User.objects.get(username=username[1]).role
                print(user_details)
                role = user_details.role
                print(role)
                if role in roles_allowed:
                    return view_func(request, *args, **kwargs)
                else:
                    return Response("Forbidden access",
                                    status=status.HTTP_403_FORBIDDEN)
            except Exception:
                return Response("Authorization could not be completed",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrap

    return check_permission