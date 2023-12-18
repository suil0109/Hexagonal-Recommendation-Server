import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)


from src.adapters.repository.ctr_prediction_repository import RandomPrediction, WeightPrediction, \
    PCTRPrediction, MixedPrediction, request_ctr_prediction_server

from src.infrastructure.configuration.config import global_config
from src.domain.models.entities import Rec, Rec
from src.domain.models.dto_rec import UserInfo

from unittest.mock import Mock, patch
import unittest


mock_request_ctr_prediction_server = Mock()
mock_PCTRPrediction = Mock()
mock_WeightPrediction = Mock()

# Mock configurations
global_config.MAX_RECS = 5


class TestRandomPrediction(unittest.TestCase):

    def setUp(self):
        self.random_prediction = RandomPrediction()
        self.user_info = Mock(spec=UserInfo)
        self.recs_list = [Mock(spec=Rec) for _ in range(10)]

    def test_predict_ctr_output(self):
        result = self.random_prediction.predict_ctr(self.user_info, self.recs_list)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(rec, Rec) for rec in result))
        self.assertLessEqual(len(result), global_config.MAX_RECS)


    # make sure the list is shuffled
    def test_predict_ctr_shuffle(self):
        original_recs_list = self.recs_list.copy()
        self.random_prediction.predict_ctr(self.user_info, self.recs_list)
        self.assertNotEqual(self.recs_list, original_recs_list)


class TestWeightPrediction(unittest.TestCase):

    def setUp(self):
        self.weight_prediction = WeightPrediction()
        self.user_info = Mock(spec=UserInfo)
        self.recs_list = [Mock(spec=Rec, id=i, weight=i) for i in range(1, 100, 10)]

    def test_predict_ctr_output(self):
        result = self.weight_prediction.predict_ctr(self.user_info, self.recs_list)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(rec, Rec) for rec in result))
        self.assertLessEqual(len(result), global_config.MAX_RECS)

    def test_random_probability_prediction_distribution(self):


        total_weight = sum(rec.weight for rec in self.recs_list)
        probabilities = [rec.weight / total_weight for rec in self.recs_list]

        zipped = sorted(zip(self.recs_list, probabilities), key= lambda x: x[1], reverse=True)
        expected_recs = [rec for rec, weight in zipped]
        actual_recs = self.weight_prediction.random_probability_prediction(self.user_info, self.recs_list)

        count = 0

        # check if half of the probability is in the list!
        for i in range(len(actual_recs)):
            if actual_recs[i].id == expected_recs[i].id:
                count +=1

        assert count < (global_config.MAX_RECS //  2)

# class TestWeightPrediction(unittest.TestCase):

#     def setUp(self):
#         self.weight_prediction = WeightPrediction()
#         self.user_info = Mock(spec=UserInfo)
#         self.recs_list = [Mock(spec=Rec, id=i, weight=i) for i in range(1, 100, 10)]

#     def test_predict_ctr_output(self):
#         result = self.weight_prediction.predict_ctr(self.user_info, self.recs_list)
#         self.assertIsInstance(result, list)
#         self.assertTrue(all(isinstance(rec, Rec) for rec in result))
#         self.assertLessEqual(len(result), global_config.MAX_RECS)

class TestPCTRPrediction(unittest.TestCase):

    def setUp(self):
        self.pctr_prediction = PCTRPrediction()
        self.user_info = Mock(spec=UserInfo, user_id=1)
        self.recs_list = [Rec(id=23, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=2.0), Rec(id=44, name='campaign name 2', image_url='https://image.google.com/image_2.jpg', landing_url='https://landing.google.com/landing_2', weight=5500, target_country='KR', target_gender='M', point=7.0), Rec(id=53, name='campaign name 3', image_url='https://image.google.com/image_3.jpg', landing_url='https://landing.google.com/landing_3', weight=6400, target_country='KR', target_gender='M', point=5.0)]

    def test_predict_ctr_output(self):
        result = self.pctr_prediction.predict_ctr(self.user_info, self.recs_list)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(rec, Rec) for rec in result))
        self.assertLessEqual(len(result), global_config.MAX_RECS)


class TestMixedPrediction(unittest.TestCase):
    def setUp(self):
        self.mixed_prediction = MixedPrediction()
        self.user = UserInfo(user_id=1, gender="M", country="KR")
        self.recs = [Rec(id=23, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=2.0), Rec(id=44, name='campaign name 2', image_url='https://image.google.com/image_2.jpg', landing_url='https://landing.google.com/landing_2', weight=5500, target_country='KR', target_gender='M', point=7.0), Rec(id=53, name='campaign name 3', image_url='https://image.google.com/image_3.jpg', landing_url='https://landing.google.com/landing_3', weight=6400, target_country='KR', target_gender='M', point=5.0)]
        self.user_info = Mock(spec=UserInfo, user_id=1)

            # self.recs = [Rec() for _ in range(3)]
    def test_predict_ctr_output(self):
        result = self.mixed_prediction.predict_ctr(self.user_info, self.recs)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(rec, Rec) for rec in result))
        self.assertLessEqual(len(result), global_config.MAX_RECS)

    @patch('src.adapters.repository.ctr_prediction_repository.request_ctr_prediction_server', mock_request_ctr_prediction_server)
    @patch('src.adapters.repository.ctr_prediction_repository.PCTRPrediction.sort_by_pctr', mock_PCTRPrediction.sort_by_pctr)
    @patch('src.adapters.repository.ctr_prediction_repository.WeightPrediction.random_probability_prediction', mock_WeightPrediction.random_probability_prediction)
    def test_predict_ctr(self):

        # Test the algorithm to make sure that length of rec is always less than equal to global variable 3
        for ctr_count in range(5):
            for pctr_count in range(5):
                for weight_count in range(5):
                    mock_request_ctr_prediction_server.return_value = [f'rec{i}' for i in range(ctr_count)]
                    mock_PCTRPrediction.sort_by_pctr.return_value = [f'rec{i}' for i in range(pctr_count)]
                    mock_WeightPrediction.random_probability_prediction.return_value = [f'rec{i}' for i in range(weight_count)]

                    mixed_prediction = MixedPrediction()

                    sorted_recs = mixed_prediction.predict_ctr(self.user, self.recs)

                    # Make sure the length of the requirements is <=3
                    assert len(sorted_recs) <= min(global_config.MAX_RECS, len(self.recs))



class TestRequestCTRPredictionServer(unittest.TestCase):

    def test_request_ctr_prediction_server(self):

        # expected_url = "https://predict-ctr-pmj4td4sjq-du.a.run.app/?user_id=11324&rec_campaign_ids=23,44,58"

        # Test data setup
        user = UserInfo(user_id=11324, gender="M", country="KR")
        recs = [
            Rec(id=23, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=2.0),
            Rec(id=44, name='campaign name 2', image_url='https://image.google.com/image_2.jpg', landing_url='https://landing.google.com/landing_2', weight=5500, target_country='KR', target_gender='M', point=7.0),
            Rec(id=53, name='campaign name 3', image_url='https://image.google.com/image_3.jpg', landing_url='https://landing.google.com/landing_3', weight=6400, target_country='KR', target_gender='M', point=5.0)
        ]

        result = request_ctr_prediction_server(user, recs)

        self.assertIsInstance(result, dict)        
        self.assertIsInstance(result, dict)
        self.assertIn('pctr', result)
        self.assertIsInstance(result['pctr'], list)
        self.assertTrue(all(isinstance(val, float) for val in result['pctr']))

if __name__ == '__main__':
    unittest.main()


