import jwt
from ParkingLotSystem import settings


def get_user(user_token):
    payload = jwt.decode(user_token, settings.SECRET_KEY)
    username = payload.get('username')
    return username