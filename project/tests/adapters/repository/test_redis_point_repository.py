import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from unittest.mock import patch, Mock
from src.domain.models.dto_point import PointInfo
from src.adapters.repository.redis_point_respository import RedisPointRepository
from src.domain.models.entities import User, Rec 
from tests.infrastructure.redis.test_model import MockRedis
from src.domain.models.configuration import Transaction

class TestRedisPointRepository(unittest.TestCase):
    def setUp(self):
        self.redis_repo = RedisPointRepository(MockRedis())
        self.user = User(user_id=123, gender="M", country='KR', balance=None, rate_limit=None)
        self.recs = [Rec(id=23, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=2.0), Rec(id=44, name='campaign name 2', image_url='https://image.google.com/image_2.jpg', landing_url='https://landing.google.com/landing_2', weight=5500, target_country='KR', target_gender='M', point=7.0), Rec(id=53, name='campaign name 3', image_url='https://image.google.com/image_3.jpg', landing_url='https://landing.google.com/landing_3', weight=6400, target_country='KR', target_gender='M', point=5.0)]
        self.pointInfo = PointInfo(rec_id = 23, user_id=123, transaction='deposit', point=10)

    @patch('tests.infrastructure.redis.test_model.MockRedis')
    def test_init(self, mock_redis):
        redis = RedisPointRepository(MockRedis())

    # @patch('tests.infrastructure.redis.test_model.MockRedis')
    def test_initialize_user_rec(self):
        # redis = RedisPointRepository(MockRedis())
        # mock_redis = Mock()
        # mock_redis.initialize_user_rec.return_value = 1
        self.redis_repo.initialize_user_rec(self.user, self.recs)
        
        user_id_in_redis = 'user:'+str(self.user.user_id)
        key_in_redis = {'rate_limit': 2, 'point_remaining': 0}

        self.assertEqual(self.redis_repo.redis_conn.exists(user_id_in_redis), 1)
        self.assertEqual(self.redis_repo.redis_conn.get(user_id_in_redis), key_in_redis)

    def test_find_rec(self):

        # mock_redis = Mock()
        # mock_redis.initialize_user_rec.return_value = 1
        self.redis_repo.initialize_user_rec(self.user, self.recs)
        self.assertEqual(self.redis_repo.find_rec(self.pointInfo), None)

    def test_update_point_deposit(self):

        user_id_in_redis = 'user:'+str(self.user.user_id)
        user_remaining_point = 'point_remaining'
        remaining_balance = 10

        self.redis_repo.initialize_user_rec(self.user, self.recs)
        self.redis_repo.update_point(Transaction.DEPOSIT.value, self.pointInfo)
        self.assertEqual(self.redis_repo.redis_conn.hget(user_id_in_redis, user_remaining_point), remaining_balance)

    def test_update_point_deduct(self):

        user_id_in_redis = 'user:'+str(self.user.user_id)
        user_remaining_point = 'point_remaining'
        remaining_balance = 0

        self.redis_repo.initialize_user_rec(self.user, self.recs)
        self.redis_repo.update_point(Transaction.DEDUCT.value, self.pointInfo)
        self.assertEqual(self.redis_repo.redis_conn.hget(user_id_in_redis, user_remaining_point), remaining_balance)

    def test_update_point_deposit_then_deduct(self):

        user_id_in_redis = 'user:'+str(self.user.user_id)
        user_remaining_point = 'point_remaining'
        remaining_balance = 5

        deductInfo = self.pointInfo
        deductInfo.point = 5

        self.redis_repo.initialize_user_rec(self.user, self.recs)
        ## Deposit 10
        self.redis_repo.update_point(Transaction.DEDUCT.value, self.pointInfo)

        ## Deduct 5
        self.redis_repo.update_point(Transaction.DEPOSIT.value, self.pointInfo)
        
        # Remaining 5
        self.assertEqual(self.redis_repo.redis_conn.hget(user_id_in_redis, user_remaining_point), remaining_balance)

    def test_has_rec_been_served(self):

        self.redis_repo.initialize_user_rec(self.user, self.recs)

        ## check if the rec exists. it should exists
        self.assertEqual(self.redis_repo.has_rec_been_served(self.pointInfo), True)

        newPointInfo = self.pointInfo
        self.pointInfo.rec_id = 9999

        ## check if the rec exists. it shouln't exists
        self.assertEqual(self.redis_repo.has_rec_been_served(newPointInfo), False)


    def test_point_remaining(self):
        self.redis_repo.initialize_user_rec(self.user, self.recs)
        self.redis_repo.point_remaining(self.user)

        #TODO
        # self.assertEqual(self.redis_repo.point_remaining(self.user), 0)


if __name__ == '__main__':
    unittest.main()
