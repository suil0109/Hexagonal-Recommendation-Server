import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from src.domain.models.dto_rec import UserInfo, RecInfo, RecResponse
import datetime

class test_entities_models(unittest.TestCase):

    def test_userinfo_model_init_values_and_types(self):
        user = UserInfo(
            user_id=123,
            gender="F",
            country="US"
        )

        self.assertEqual(user.user_id, 123)
        self.assertEqual(user.gender, "F")
        self.assertEqual(user.country, "US")

        self.assertIsInstance(user.user_id, int)
        self.assertIsInstance(user.gender, str)
        self.assertIsInstance(user.country, str)

    def test_recinfo_model_init_values(self):
        rec = RecInfo(
            id=10,
            name="Test Rec",
            image_url="http://google_ad.com/image.jpg",
            landing_url="http://google_ad.com",
            weight=100,
            target_country="KR",
            target_gender="M",
            point=200,
            date=datetime.datetime(2023, 1, 1)
        )


        self.assertEqual(rec.id, 10)
        self.assertEqual(rec.name, "Test Rec")
        self.assertEqual(rec.image_url, "http://google_ad.com/image.jpg")
        self.assertEqual(rec.landing_url, "http://google_ad.com")
        self.assertEqual(rec.weight, 100)
        self.assertEqual(rec.target_country, "KR")
        self.assertEqual(rec.target_gender, "M")
        self.assertEqual(rec.point, 200)
        self.assertEqual(rec.date, datetime.datetime(2023, 1, 1))

        self.assertIsInstance(rec.id, int)
        self.assertIsInstance(rec.name, str)
        self.assertIsInstance(rec.image_url, str)
        self.assertIsInstance(rec.landing_url, str)
        self.assertIsInstance(rec.weight, int)
        self.assertIsInstance(rec.target_country, str)
        self.assertIsInstance(rec.target_gender, str)
        self.assertIsInstance(rec.point, int)
        self.assertIsInstance(rec.date, datetime.datetime)


    def test_recresponse_model_init_values(self):

        rec = RecResponse(
            id=10,
            name="Test Rec",
            image_url="http://google_ad.com/image.jpg",
            landing_url="http://google_ad.com",
        )

        assert rec.id == 10
        assert rec.name == "Test Rec"
        assert rec.image_url == "http://google_ad.com/image.jpg"
        assert rec.landing_url == "http://google_ad.com"

        self.assertIsInstance(rec.id, int)
        self.assertIsInstance(rec.name, str)
        self.assertIsInstance(rec.image_url, str)
        self.assertIsInstance(rec.landing_url, str)  


    # def test_recresponse_model_init_types(self):

    #     rec = RecResponse(
    #         id=10,
    #         name="Test Rec",
    #         image_url="http://google_ad.com/image.jpg",
    #         landing_url="http://google_ad.com",
    #     )

    #     self.assertIsInstance(rec.id, int)
    #     self.assertIsInstance(rec.name, str)
    #     self.assertIsInstance(rec.image_url, str)
    #     self.assertIsInstance(rec.landing_url, str)  

if __name__ == '__main__':
    unittest.main()
