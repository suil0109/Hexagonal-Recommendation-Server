from src.main import app  

from src.domain.models.configuration import Status, StatusCode

from fastapi.testclient import TestClient
from unittest import TestCase
import unittest



client = TestClient(app)


class TestRecRouter(TestCase):
    def test_init(self):

        # @dataclass
        # class Point:
        #     rec_id: int
        #     amount: int
        #     date: Optional[datetime] = field(default=datetime.now())

        test_point = {"rec_id": 1, "amount":10}
        
        response = client.post("point/test", json=test_point)
        
        self.assertEqual(response.status_code, StatusCode.OK.value)

    def test_valid_intput_output(self):
        """
        Test if the apis have valid input and outputs!
        """
        
        test_point = {"rec_id": 1, "amount":10}
        response = client.post("point/modify", json=test_point)
        self.assertEqual(response.status_code, StatusCode.OK.value)
        self.assertEqual(response.json(), Status.SUCCESS.value)

        
        # for rec_data in rec_response:
        #     self.assertTrue(isinstance(rec_data, dict), "Should be a dict")
        #     for field in fields(RecResponse):
        #         self.assertIn(field.name, rec_data, f"{field.name} missing response")
        #         self.assertIsInstance(rec_data[field.name], field.type, f"{field.name} should be of type {field.type}")
    

if __name__ == '__main__':
    unittest.main()