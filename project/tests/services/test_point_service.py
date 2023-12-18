import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from unittest.mock import Mock, patch
from src.domain.models.entities import Rec, User
from src.domain.models.dto_point import PointInfo
from src.services.rec_service import RecService
from src.services.point_service import PointService

class TestPointService(unittest.TestCase):

    def setUp(self):
        self.sql_interface_mock = Mock()
        self.redis_interface_mock = Mock()
        self.point_service = PointService(sql_interface=self.sql_interface_mock, redis_interface=self.redis_interface_mock)

    def test_deposit_point(self):
        pointInfo = PointInfo(rec_id=1, user_id=1,transaction='deposit', point=100)
        self.point_service.deposit_point(pointInfo)
        # self.point_interface_mock.deposit_point.assert_called_with(pointInfo)

    def test_deduct_point(self):
        pointInfo = PointInfo(rec_id=1, user_id=1,transaction='deduct', point=100)
        self.point_service.deduct_point(pointInfo)
        # self.point_interface_mock.deduct_point.assert_called_with(1, 50.0)

