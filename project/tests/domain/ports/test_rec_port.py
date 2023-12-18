import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from typing import List
from src.domain.models.entities import Rec, User
from src.domain.models.dto_rec import UserInfo, RecInfo, RecResponse
from src.domain.ports.rec_port import RecManagementPort


class MockRecManagement(RecManagementPort):
    def allocate_recs(self, user_id: int, gender: str, country: str) -> List[RecInfo]:
        return [Rec(id=1, name='Mock Rec', image_url='http://example.com/rec.png',
                   landing_url='http://example.com', weight=10, target_country=country,
                   target_gender=gender, point=0.5)]

    def response_recs(self, recs: List[RecInfo]) -> List[RecResponse]:
        return [RecResponse(id=rec.id, name=rec.name, image_url=rec.image_url,
                           landing_url=rec.landing_url) for rec in recs]

    def predict_ctr(self, user: UserInfo, recs: List[RecInfo]) -> List[RecInfo]:
        return recs

class TestRecManagement(unittest.TestCase):

    def setUp(self):
        self.rec_manager = MockRecManagement()
        self.user = UserInfo(user_id=1, gender='Male', country='US')
        self.recs = [
            Rec(id=1, name='Rec 1', image_url='http://example.com/ad1.png',
               landing_url='http://example.com/landing1', weight=10,
               target_country='US', target_gender='Any', point=0.1),
            Rec(id=2, name='Rec 2', image_url='http://example.com/ad2.png',
               landing_url='http://example.com/landing2', weight=20,
               target_country='US', target_gender='Male', point=0.2)
        ]

    def test_allocate_recs(self):
        recs = self.rec_manager.allocate_recs(user_id=123, gender='Female', country='US')
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0].target_country, 'US')
        self.assertEqual(recs[0].target_gender, 'Female')

    def test_response_recs(self):
        # self.mock_recs = [Rec(id=1, name='Mock Rec', image_url='http://example.com/rec.png',
        #             landing_url='http://example.com', weight=10, target_country='US',
        #             target_gender='Male', point=0.5, date=None)]

        rec_manager = self.rec_manager.response_recs(self.recs)
        self.assertEqual(len(rec_manager), 2)
        self.assertEqual(rec_manager[0].id, self.recs[0].id)
        self.assertEqual(rec_manager[0].name, 'Rec 1')

        self.assertEqual(rec_manager[1].id, self.recs[1].id)
        self.assertEqual(rec_manager[1].name, 'Rec 2')

    def test_predict_ctr(self):
        predicted_recs = self.rec_manager.predict_ctr(self.user, self.recs)
        self.assertEqual(len(predicted_recs), len(self.recs))
        self.assertListEqual(predicted_recs, self.recs)

if __name__ == '__main__':
    unittest.main()
