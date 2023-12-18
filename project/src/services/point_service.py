
from src.domain.models.dto_point import PointUser, Point, PointDepositBase, PointInfo, PointDeductBase
from src.domain.models.configuration import Transaction, UNUSED_REC_ID
from src.domain.models.entities import User

from src.adapters.repository.redis_point_respository import RedisPointRepository
from src.adapters.repository.sql_point_repository import SQLPointRepository

from datetime import datetime
from dataclasses import asdict



class PointService:
    def __init__(self, sql_interface: SQLPointRepository, redis_interface: RedisPointRepository):
        # self.point_interface = point_interface
        self.sql_interface = sql_interface
        self.redis_interface = redis_interface

    def create_point_deposit_info(self, point_base: PointDepositBase) -> PointInfo:
        # if deposit need to serach sql and get the depsoit amount
        # need to do this..!
        point_amount = self.sql_interface.get_rec_point_amount(point_base.rec_id)
        return PointInfo(
            **asdict(point_base),
            point = point_amount,
            transaction=Transaction.DEPOSIT.value,
            timestamp=datetime.now(),
        )

    def create_point_deduct_info(self, point_base: PointDeductBase) -> PointInfo:
        return PointInfo(
            rec_id = UNUSED_REC_ID,
            **asdict(point_base),
            transaction=Transaction.DEDUCT.value,
            timestamp=datetime.now(),
        )

    def modify_point(self, point: Point) -> bool:
        if self.sql_interface.modify_point(point):
            return self.sql_interface.modify_point(point)
        return False

    def deposit_point(self, point_info: PointInfo) -> bool:
        self.redis_interface.initialize_user_point(point_info)
        # point_amount = self.sql_interface.get_rec_point_amount(point_info.rec_id)
        return self.redis_interface.deposit_point(point_info)

    def deduct_point(self, point_info: PointInfo) ->bool:
        return self.sql_interface.deduct_point(point_info)

    def history_point(self, user_info: User) -> dict:
        return self.sql_interface.get_history(user_info)

    def balance_point(self, user_info: User) -> dict:
        return asdict(self.sql_interface.get_balance(user_info))
