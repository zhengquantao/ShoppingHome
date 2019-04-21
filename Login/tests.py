from django.test import TestCase
from django.core.cache import cache
# redisTest
import redis
# import uuid

# print(uuid.uuid4())

# 数据过大 会爆栈
pool = redis.ConnectionPool(host='localhost', port=6379, max_connections=1000)
conn = redis.Redis(connection_pool=pool)
ret = conn.hscan_iter('k2', count=100)
for item in ret:
    print(item)

try:
    r = redis.StrictRedis(host='localhost', port=6379)
    pipe = r.pipeline()
    pipe.set('py10', 'hello')
    pipe.set('py11', 'world')
    pipe.execute()
    temp = r.get('py10')
    print(temp)
except:
    print('连接失败')


# 封装方法
class redisHelper():
    # 初始化
    def __init__(self, host, port):
        self.__redis = redis.StrictRedis(host, port)

    # 写值
    def set(self, key, value):
        self.__redis.set(key, value)

    # 得值
    def get(self, key):
        return self.__redis.get(key)



