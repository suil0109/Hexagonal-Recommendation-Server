import unittest

class MockRedis:
    def __init__(self, cache=None):
        if cache is None:
            cache = {}
        self.cache = cache

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value, *args, **kwargs):
        if key in self.cache:
            return 0
        else:
            self.cache[key] = value
            return 1
    def exists(self, key):
        return 1 if key in self.cache else 0

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            return 1
        return 0

    def hmset(self, hash, values):
        if not isinstance(values, dict):
            raise ValueError("Values must be a dictionary")
        self.cache.setdefault(hash, {}).update(values)
        return "OK"

    def hget(self, hash, key):
        return self.cache.get(hash, {}).get(key)


    #### V1.0.1 hset
    # def hset(self, hash, key, value):
    #     self.cache.setdefault(hash, {})[key] = value
    #     return 1

    #### V1.0.2 hset
    def hset(self, hash_key, key=None, value=None, mapping=None):

        ## mapping 업데이트
        if mapping is not None:
            if not isinstance(mapping, dict):
                raise ValueError("Mapping must be a dictionary")
            self.cache.setdefault(hash_key, {}).update(mapping)
            return len(mapping)
        else:
            ## key value 업데이트
            if key is None or value is None:
                raise ValueError("Key and value must be provided if mapping is not used")
            self.cache.setdefault(hash_key, {})[key] = value
            return 1

    def rpush(self, key, *values):
        self.cache.setdefault(key, []).extend(values)
        return len(self.cache[key])

    def lrange(self, key, start, end):
        if end == -1:
            end = None
            ## redis returns utf-8 byte strings.. so.. you need to convert each elemetns to utf-8
            return [str(item).encode('utf-8')for item in self.cache.get(key, [])[start:end]]
        return [str(item).encode('utf-8')for item in self.cache.get(key, [])[start:end+1]]
    def lrem(self, key, count, value):
        if key not in self.cache or not isinstance(self.cache[key], list):
            return 0
        original_length = len(self.cache[key])
        if count >= 0:
            self.cache[key] = [v for v in self.cache[key] if v != value or count == 0]
        else:
            self.cache[key].reverse()
            self.cache[key] = [v for v in self.cache[key] if v != value or count == 0]
            self.cache[key].reverse()
        return original_length - len(self.cache[key])
    


class TestMockRedis(unittest.TestCase):

    def setUp(self):
        self.redis = MockRedis()

    def test_set_and_get(self):
        self.redis.set('user1', 'rec1')
        self.assertEqual(self.redis.get('user1'), 'rec1')

    def test_exists(self):
        self.redis.set('user2', 'rec2')
        self.assertTrue(self.redis.exists('user2'))
        self.assertFalse(self.redis.exists('user999'))

    def test_delete(self):
        self.redis.set('user3', 'rec')
        self.assertTrue(self.redis.exists('user3'))
        self.redis.delete('user3')
        self.assertFalse(self.redis.exists('user3'))

    # hash map set, hash get
    def test_hmset_and_hget(self):
        self.redis.hmset('user1', {'age': 1, 'point': 10})
        self.assertEqual(self.redis.hget('user1', 'age'), 1)
        self.assertEqual(self.redis.hget('user1', 'point'), 10)
        self.assertIsNone(self.redis.hget('user1', 'country'))

    # hash set
    def test_hset(self):
        self.redis.hset('user2', 'age', 1)
        self.assertEqual(self.redis.hget('user2', 'age'), 1)

    # right push (list), list range
    def test_rpush_and_lrange(self):
        self.redis.rpush('list1', 'item1', 'item2')
        ## b'item' => byte string
        self.assertEqual(self.redis.lrange('list1', 0, -1), [b'item1', b'item2'])

    # list remove
    def test_lrem(self):
        self.redis.rpush('list2', 'item1', 'item2', 'item1')
        self.redis.lrem('list2', 2, 'item1')
        self.assertEqual(self.redis.lrange('list2', 0, -1), [b'item2'])

if __name__ == '__main__':
    unittest.main()
