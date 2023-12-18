import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.domain.models.dto_rec import RecInfo
from src.domain.models.dto_rec import UserInfo, RecInfo
from src.services.rec_service import RecService

from unittest.mock import Mock
import unittest



class TestRecService(unittest.TestCase):


    def setUp(self):

        self.rec1 = RecInfo(
            id=1, 
            name="campaign name 1", 
            image_url="https://image.google.com/image_1.jpg", 
            landing_url="https://landing.google.com/landing_1", 
            weight=2300, 
            target_country="HK", 
            target_gender="F", 
            point=2
        )
        self.rec2 = RecInfo(
            id=2, 
            name="campaign name 2", 
            image_url="https://image.google.com/image_2.jpg", 
            landing_url="https://landing.google.com/landing_2", 
            weight=5500, 
            target_country="US", 
            target_gender=None, 
            point=7
        )

        self.rec_allocation_mock = Mock()
        self.ctr_prediction_mock = Mock()
        self.redis_point_mock = Mock()
        self.recs = [self.rec1, self.rec2]
        self.rec_service = RecService(rec_allocation=self.rec_allocation_mock, redis_interface=self.redis_point_mock)
        self.rec_service.ctr_prediction = self.ctr_prediction_mock

    def test_get_recs_for_user(self):
        self.rec_allocation_mock.allocate_recs.return_value = self.recs
        userInfo = UserInfo(1, "M", "KR")
        result = self.rec_service.get_recs_for_user(userInfo)
        self.rec_allocation_mock.allocate_recs.assert_called_with(userInfo)
        # self.assertEqual(result, [rec.id for rec in self.recs])

    def test_get_recs_for_user_with_ctr_prediction(self):
        self.rec_allocation_mock.allocate_recs.return_value = self.recs
        self.ctr_prediction_mock.predict_ctr.return_value = [0.2, 0.8]

        userInfo = UserInfo(1,"M", "KR")
        result = self.rec_service.get_recs_for_user_with_ctr_prediction(userInfo)

        self.rec_allocation_mock.allocate_recs.assert_called_with(userInfo)
        # self.ctr_prediction_mock.predict_ctr.assert_called_with(1, [rec.id for rec in self.recs])
        # self.assertEqual(result, [rec for rec in self.recs[::-1]])

if __name__ == '__main__':
    unittest.main()
