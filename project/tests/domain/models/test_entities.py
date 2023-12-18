import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)


from src.domain.models.exceptions import SuccessResponse, ErrorResponse
from src.domain.models.entities import Rec, User

import unittest
import datetime

class test_entities_models(unittest.TestCase):
    def test_rec_model_init(self):

        rec = Rec(
            id=10,
            name="Test Rec",
            image_url="http://google_ad.com/image.jpg",
            landing_url="http://google_ad.com",
            weight=5,
            target_country="US",
            target_gender="M",
            point=100,
            date=None
        )
        
        assert rec.id == 10
        assert rec.name == "Test Rec"
        assert rec.image_url == "http://example.com/image.jpg"
        assert rec.landing_url == "http://example.com"
        assert rec.weight == 5
        assert rec.target_country == "US"
        assert rec.target_gender == "Any"


    def test_rec_model_init(self):

        rec = Rec(
            id=10,
            name="Test Rec",
            image_url="http://google_ad.com/image.jpg",
            landing_url="http://google_ad.com",
            weight=5,
            target_country="US",
            target_gender="M",
            point=100,
            date=datetime.datetime.now() 
        )

        self.assertIsInstance(rec.id, int)
        self.assertIsInstance(rec.name, str)
        self.assertIsInstance(rec.image_url, str)
        self.assertIsInstance(rec.landing_url, str)  
        self.assertIsInstance(rec.weight, int) 
        self.assertIsInstance(rec.target_country, str) 
        self.assertIsInstance(rec.target_gender, str) 
        self.assertIsInstance(rec.point, int) 
        self.assertIsInstance(rec.date, datetime.datetime) 

    def test_user_model_init(self):
        user = User(user_id=1, gender="Female", country="USA", balance=100, rate_limit=10)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.gender, "Female")
        self.assertEqual(user.country, "USA")
        self.assertEqual(user.balance, 100)
        self.assertEqual(user.rate_limit, 10)

    def test_user_model_type(self):
        user = User(user_id=1, gender="Female", country="USA", balance=100, rate_limit=10)
        self.assertIsInstance(user.user_id, int)
        self.assertIsInstance(user.gender, str)
        self.assertIsInstance(user.country, str)
        self.assertIsInstance(user.balance, int)  
        self.assertIsInstance(user.rate_limit, int) 

    def test_success_response_init(self):
        response = SuccessResponse(status="OK")
        self.assertEqual(response.status, "OK")

    def test_error_response_init(self):
        response = ErrorResponse(status="Error", message="An error occurred")
        self.assertEqual(response.status, "Error")
        self.assertEqual(response.message, "An error occurred")


if __name__ == '__main__':
    unittest.main()

