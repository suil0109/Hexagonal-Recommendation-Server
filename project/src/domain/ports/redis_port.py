from src.domain.models.dto_rec import UserInfo, RecResponse
from src.domain.models.dto_point import  RedisPoint, PointInfo

from abc import ABC, abstractmethod

class RedisPort(ABC):
    @abstractmethod
    def initialize_user(self, point: PointInfo) -> RedisPoint:
        pass

    @abstractmethod
    def update_point(self, sign, point: PointInfo) -> bool:
        pass

    @abstractmethod
    def has_rec_been_served(self, point: PointInfo) -> bool:
        pass
    
    @abstractmethod
    def deposit_point(self, point: PointInfo) -> bool:
        pass
    
    @abstractmethod
    def deduct_point(self, user: UserInfo, point: RecResponse) -> bool:
        pass

    @abstractmethod
    def point_remaining(self, user: UserInfo) -> RedisPoint:
        pass
