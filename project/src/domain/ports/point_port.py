from src.domain.models.dto_point import PointInfo, Point
from src.domain.models.entities import User

from abc import ABC, abstractmethod
from typing import List

class PointPort(ABC):
    @abstractmethod
    def modify_point(self, point: Point) -> bool:
        """Deposit point for a user."""
        pass

    @abstractmethod
    def deposit_point(self, user_info: User, point_info: List[Point]) -> bool:
        """Deposit point for a user."""
        pass

    @abstractmethod
    def deduct_point(self, user_info: User, task: PointInfo) -> bool:
        """Deduct an amount from the user's point balance."""
        pass
