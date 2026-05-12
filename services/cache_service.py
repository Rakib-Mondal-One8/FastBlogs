import redis.asyncio as aioredis
import json
from typing import Any

class RedisCache:
    def __init__(self,url = "redis://localhost:6379"):
        self._client = None
        self._url = url

    async def connect(self):
        self._client = await aioredis.from_url(
            self._url,
            encoding='UTF-8',
            decode_responses=True,
            max_connections=20
        )

    async def disconnect(self):
        if(self._client):
            await self._client.aclose()

    async def get(self,key:str):
        if(self._client is None):
            raise Exception("Redis is not connected.")
        raw = await self._client.get(key)
        if(raw is None):
            return None
        return json.loads(raw)
    
    async def set(self,key:str,value:Any,ttl:float):
        await self._client.setex(key,ttl,json.dumps(value))

    async def delete(self,key:str):
        await self._client.delete(key)

    async def delete_pattern(self,pattern:str):
        keys = await self._client.keys(pattern)
        if keys:
            await self._client.delete(*keys)
        return 0
    
    async def exists(self,key):
        return bool(await self._client.exists(key))
    
    async def ttl(self,key:str):
        return await self._client.ttl(key)
    

redis = RedisCache()
