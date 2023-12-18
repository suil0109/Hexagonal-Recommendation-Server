from src.adapters.repository.redis_point_respository import RedisPointRepository
from src.adapters.repository.sql_point_repository import SQLPointRepository
from src.adapters.repository.sql_rec_repository import SQLRecRepository

from src.services.point_service import PointService
from src.services.rec_service import RecService


# Rec service
def get_rec_service():
    rec_repository = SQLRecRepository()
    redis_repository = RedisPointRepository()
    rec_service = RecService(rec_repository, redis_repository)
    return rec_service


# Point service
def get_point_service():
    sql_repository = SQLPointRepository()
    redis_repository = RedisPointRepository()
    point_service = PointService(sql_repository, redis_repository)
    return point_service
