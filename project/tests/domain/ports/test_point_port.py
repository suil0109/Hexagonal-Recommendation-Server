import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from typing import List
from src.domain.models.entities import User
from src.domain.models.dto_point import PointInfo, Point

from src.domain.ports.point_port import PointPort
import unittest
from unittest.mock import Mock

class MockPointPort(PointPort):
    def modify_point(self, point: Point) -> bool:
        return True

    def deposit_point(self, user_info: User, point_info: List[Point]) -> bool:
        return True

    def deduct_point(self, user_info: User, task: PointInfo) -> bool:
        return True


class TestPointPort(unittest.TestCase):

    def setUp(self):
        self.point_port = MockPointPort()
        self.user_info = Mock(spec=User)
        self.point = Mock(spec=Point)
        self.point_info = Mock(spec=PointInfo)
        self.point_list = [self.point]

    def test_modify_point(self):
        result = self.point_port.modify_point(self.point)
        self.assertTrue(result)

    def test_deposit_point(self):
        result = self.point_port.deposit_point(self.user_info, self.point_list)
        self.assertTrue(result)

    def test_deduct_point(self):
        result = self.point_port.deduct_point(self.user_info, self.point_info)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
