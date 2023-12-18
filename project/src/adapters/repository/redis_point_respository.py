from src.domain.models.dto_point import Point, RedisPoint, PointInfo
from src.domain.models.configuration import Transaction
from src.domain.models.dto_rec import UserInfo, RecInfo
from src.domain.models.entities import User
from src.domain.ports.redis_port import RedisPort

from src.infrastructure.queue.task_queue import task_queue
from src.infrastructure.configuration.config import global_config

import redis
from typing import List

rate_limit = 2
point_remaining = 0

class RedisPointRepository(RedisPort):
    def __init__(self, redis_client=None, host=global_config.REDIS_HOST, port=global_config.REDIS_PORT, db=global_config.REDIS_DB):
        
        if redis_client is None:
            self.redis_conn = redis.Redis(host=host, port=port, db=db)
        else:
            self.redis_conn = redis_client

    def initialize_user(self, point: PointInfo) -> RedisPoint:
        pass

    def initialize_user_point(self, point: PointInfo) -> RedisPoint:
        user_key = f"user:{point.user_id}"
        recs_served_key = f"recs_served:{point.user_id}"
        # key_type = self.redis_conn.type(user_key)
        # updated_recs_served = self.redis_conn.lrange(f"recs_served:{point.user_id}", 0, -1)
        # print(updated_recs_served)
        if not self.redis_conn.exists(user_key):
            
            # update from MySQL DB
            self.redis_conn.hmset(f"user:{point.user_id}", {
                "rate_limit": rate_limit,
                "point_remaining": 0
            })
            if not self.redis_conn.exists(recs_served_key):
                self.redis_conn.delete(f"recs_served:{point.user_id}")
            print(f"User {point.user_id} initialized in Redis.")
        else:
            print(f"User {point.user_id} already exists in Redis.")

    def initialize_user_rec(self, user:User, recs: List[RecInfo]) -> RedisPoint:
        user_key = f"user:{user.user_id}"
        recs_served_key = f"recs_served:{user.user_id}"

        if not self.redis_conn.exists(user_key):
            
            # Create user if it doesn't exists
            self.redis_conn.hmset(f"user:{user.user_id}", {
                "rate_limit": rate_limit,
                "point_remaining": 0
            })
            print(f"User {user.user_id} initialized in Redis.")

        # reset recs served every event
        if self.redis_conn.exists(recs_served_key):
            self.redis_conn.delete(f"recs_served:{user.user_id}")

        # add Recs to redis 
        for rec in recs:
            self.redis_conn.rpush(recs_served_key, rec.id)
        
        # dipslay current user redis rec id
        # recs_served = self.redis_conn.lrange(f"recs_served:{user.user_id}", 0, -1)
        # recs_served = [int(rec.decode('utf-8')) for rec in recs_served]
        # print(recs_served)
        # user_data = self.redis_conn.hgetall(f"user:{user.user_id}")
        # print(user_data)
        # result = self.redis_conn.delete(f"user:{user.user_id}")

    def find_rec(self, point_info: PointInfo) -> Point:
        recs_served = self.redis_conn.lrange(f"recs_served:{point_info.user_id}", 0, -1)

        ## the data comes back as byte strings due to size.
        ## decode('utf-8') converts byte strings -> python strings.
        recs_served = [int(rec.decode('utf-8')) for rec in recs_served]

        # search with rec_reponse to get Point
        # query = (
        #     self.db.query(RecModel)
        #     .filter(RecModel.id == point_info.rec_id)
        # ).one_or_none()

        # if query:
        #     return Point(rec_id=query.id, amount =query.point)
        # return DOES_NOT_EXITS
        


    def update_point(self, transaction, point: PointInfo) -> bool:
        current_point = int(self.redis_conn.hget(f"user:{point.user_id}", "point_remaining"))
        
        remaining = current_point + point.point
        if transaction == Transaction.DEDUCT.value:
            remaining = current_point - point.point
        if remaining < 0 :
            return False
        self.redis_conn.hset(f"user:{point.user_id}", mapping={"rate_limit": rate_limit, "point_remaining": int(remaining)})

        # Below task should go into where right after the deposit usccess in side the service 
        # Insert Task to Queue
        # Update MySql History & User Status
        if transaction == Transaction.DEPOSIT.value:
            task_queue.enqueue(transaction, point)

        return True
    
    def deposit_rec(self, point: PointInfo) -> bool:
        self.redis_conn.lrem(f"recs_served:{point.user_id}", point.user_id, point.rec_id)
        return True


    def has_rec_been_served(self, point: PointInfo) -> bool:
        recs_served = self.redis_conn.lrange(f"recs_served:{point.user_id}", 0, -1)
        recs_served = [int(rec.decode('utf-8')) for rec in recs_served]
        # self.redis_conn.delete(f"recs_served:{point.user_id}")
        # print(recs_served)
        # print(point.rec_id in recs_served)
        return point.rec_id in recs_served

    def deposit_point(self, point: PointInfo) -> bool:
        if self.has_rec_been_served(point):
        # if True:
            self.deposit_rec(point)
            self.update_point(Transaction.DEPOSIT.value, point)
            return True
        else:
            #TODO: Check MySQL for cache miss
            # if mysql_rec_been-served
            # # deposit point
            pass
        return False

    def deduct_point(self, user: UserInfo, point: PointInfo) -> bool:
        # check mysql database balance()
        # read & write in mysql database
        return
    
    def point_remaining(self, user: UserInfo) -> RedisPoint:
        return self.redis_conn.hset(f"user:{user.user_id}", "point_remaining", point_remaining)

