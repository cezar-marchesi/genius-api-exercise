import redis
import json
from config import Configuration
from datetime import timedelta

class RedisConnection:
    def __init__(self) -> None:
        self.redis_host = Configuration.redis_host
        self.redis_port = Configuration.redis_port
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)
    
    def get_cache(self, key: str) -> str:
        result = self.redis_client.get(key)
        if result:
            return json.loads(result)
        return None

    def set_cache(self, key: str, data: dict) -> None:
        self.redis_client.set(key, json.dumps(data))

    def set_expiration(self, key: str) -> None:
        self.redis_client.expire(key, timedelta(days=7))

    def delete_cache(self, key: str) -> None:
        self.redis_client.delete(key)