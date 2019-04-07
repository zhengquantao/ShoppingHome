import redis
POOL = redis.ConnectionPool(host='localhost', port=6379, max_connections=1000)
# conn = redis.Redis(connection_pool=POOL)