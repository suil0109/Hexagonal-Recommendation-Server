# import os, sys
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# sys.path.insert(0, parent_dir)


# from fastapi.testclient import TestClient
# from unittest import TestCase
# from src.main import app  
# from src.domain.models.entities import User
# from src.domain.models.dto_rec import UserInfo, RecInfo, RecResponse
# from src.domain.models.configuration import StatusCode 
# import unittest
# from dataclasses import dataclass, asdict, fields

# client = TestClient(app)


# # @dataclase
# # class User:
# #     user_id: int
# #     gender: str
# #     country: str

# class TestRecRouter(TestCase):
#     def test_init(self):

#         test_user = UserInfo(user_id=1, gender="M", country="KR")
        
#         response = client.post("recs/", json=asdict(test_user))
        
#         self.assertEqual(response.status_code, StatusCode.OK.value)
#         self.assertEqual(response.json()[0], StatusCode.OK.value)

#     def test_valid_intput_output(self):
#         """
#         Test if the apis have valid input and outputs!
#         """

#         test_user = UserInfo(user_id=1, gender="M", country="KR")
#         apis = ['recs/base/', 'recs/ctr']
#         for api_call in apis:
#             response = client.post(api_call, json=asdict(test_user))
#             rec_response = response.json()

#             self.assertTrue(isinstance(rec_response, list), "Needs to be a List")

#             for rec_data in rec_response:
#                 self.assertTrue(isinstance(rec_data, dict), "Should be a dict")
#                 for field in fields(RecResponse):
#                     self.assertIn(field.name, rec_data, f"{field.name} missing response")
#                     self.assertIsInstance(rec_data[field.name], field.type, f"{field.name} should be of type {field.type}")
    

# if __name__ == '__main__':
#     unittest.main()