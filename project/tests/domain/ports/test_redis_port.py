import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from unittest.mock import Mock
from src.domain.models.entities import User
from src.domain.models.dto_rec import UserInfo, RecInfo, RecResponse
from src.domain.models.dto_point import  RedisPoint, PointInfo
from src.domain.ports.redis_port import RedisPort

class MockRedisPort(RedisPort):
    def initialize_user(self, point: PointInfo) -> RedisPoint:
        return Mock(spec=RedisPoint)

    def update_point(self, sign, point: PointInfo) -> bool:
        return True

    def has_rec_been_served(self, point: PointInfo) -> bool:
        return False
    
    def deposit_point(self, point: PointInfo) -> bool:
        return True
    
    def deduct_point(self, user: UserInfo, point: RecResponse) -> bool:
        return True

    def point_remaining(self, user: UserInfo) -> RedisPoint:
        return Mock(spec=RedisPoint)

class TestRedisPort(unittest.TestCase):

    def setUp(self):
        self.redis_port = MockRedisPort()
        self.point_info = Mock(spec=PointInfo)
        self.user = Mock(spec=User)
        self.rec_response = Mock(spec=RecResponse)

    def test_initialize_user(self):
        result = self.redis_port.initialize_user(self.point_info)
        self.assertIsInstance(result, RedisPoint)

    def test_update_point(self):
        result = self.redis_port.update_point('+', self.point_info)
        self.assertTrue(result)

    def test_has_rec_been_served(self):
        result = self.redis_port.has_rec_been_served(self.point_info)
        self.assertFalse(result)

    def test_deposit_point(self):
        result = self.redis_port.deposit_point(self.point_info)
        self.assertTrue(result)

    def test_deduct_point(self):
        result = self.redis_port.deduct_point(self.user, self.rec_response)
        self.assertTrue(result)

    def test_point_remaining(self):
        result = self.redis_port.point_remaining(self.user)
        self.assertIsInstance(result, RedisPoint)

if __name__ == '__main__':
    unittest.main()
