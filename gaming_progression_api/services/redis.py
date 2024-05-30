from redis.asyncio import Redis
from gaming_progression_api.settings import get_settings

settings = get_settings()


class RedisTools:
    def __init__(self):
        self.redis = Redis(host='redis', port=6379)

    async def set_pair(self, key: str, value: str, exp: int):
        await self.redis.set(key, value, ex=exp)

    async def get_pair(self, key: str):
        return await self.redis.get(key)
