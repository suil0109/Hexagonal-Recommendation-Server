import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from datetime import datetime

from src.domain.models.dto_point import Point, RedisPoint, PointUser, \
     PointDeductBase, PointDepositBase ,PointInfo


class TestPointEntities(unittest.TestCase):

    def test_point_model_init(self):
        point = Point(rec_id=1, amount=100)
        self.assertIsInstance(point.rec_id, int)
        self.assertIsInstance(point.amount, int)
        self.assertIsInstance(point.date, datetime)

    def test_redis_point_model_init(self):
        redis_point = RedisPoint(user_id='user123', rate_limit=10, point_remaining=500)
        self.assertIsInstance(redis_point.user_id, str)
        self.assertIsInstance(redis_point.rate_limit, int)
        self.assertIsInstance(redis_point.point_remaining, int)
        self.assertIsInstance(redis_point.recs_served, list)

    def test_point_user_model_init(self):
        point_user = PointUser(user_id=1, point=150)
        self.assertIsInstance(point_user.user_id, int)
        self.assertIsInstance(point_user.point, int)
        self.assertIsInstance(point_user.date, datetime)

    def test_point_deposit_base_model_init(self):
        point_deposit = PointDepositBase(rec_id=1, user_id=2)
        self.assertIsInstance(point_deposit.rec_id, int)
        self.assertIsInstance(point_deposit.user_id, int)

    def test_point_deduct_base_model_init(self):
        point_deduct = PointDeductBase(user_id=2, point=50)
        self.assertIsInstance(point_deduct.user_id, int)
        self.assertIsInstance(point_deduct.point, int)

    def test_point_info_model_init(self):
        point_info = PointInfo(rec_id=1, user_id=2, transaction='deposit', point=100)
        self.assertIsInstance(point_info.rec_id, int)
        self.assertIsInstance(point_info.user_id, int)
        self.assertIsInstance(point_info.transaction, str)
        self.assertIsInstance(point_info.point, int)
        self.assertIsInstance(point_info.timestamp, datetime)

if __name__ == '__main__':
    unittest.main()
