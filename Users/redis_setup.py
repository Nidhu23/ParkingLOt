import redis
from ParkingLotSystem import settings


def get_redis_instance():
    return redis.Redis(host=settings.REDIS_HOST,
                       port=settings.REDIS_PORT,
                       db=0)