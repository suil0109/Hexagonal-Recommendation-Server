################
# Redis Client #
################

import redis

redis_client = redis.Redis(host='hostname-redis', port=6379, db=0)