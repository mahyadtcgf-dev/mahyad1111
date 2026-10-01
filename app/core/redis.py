import redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisManager, cls).__new__(cls)
            try:
                cls._instance.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
                logger.info("Connected to Redis successfully")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                cls._instance.client = None
        return cls._instance

    def set(self, key: str, value: str, ex: int = None):
        if not self.client: return False
        return self.client.set(key, value, ex=ex)

    def get(self, key: str):
        if not self.client: return None
        return self.client.get(key)

    def incr(self, key: str):
        if not self.client: return 0
        return self.client.incr(key)

    def expire(self, key: str, ex: int):
        if not self.client: return False
        return self.client.expire(key, ex)

redis_manager = RedisManager()
