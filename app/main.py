from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api.main import api_router
from app.core.config import settings


from app.infrastructure.database import redis

app = FastAPI()


@app.on_event("startup")
async def startup():
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

app.include_router(api_router, prefix=settings.API_V1_STR)
