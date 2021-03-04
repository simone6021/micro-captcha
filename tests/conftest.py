import pytest
import aioredis
from async_asgi_testclient import TestClient

from pydantic import RedisDsn
from pydantic.tools import parse_obj_as

from main import app, get_settings
from settings import Settings


def get_settings_override() -> Settings:
    return Settings(redis_dsn=parse_obj_as(RedisDsn, 'redis://redis:6379/2'))


app.dependency_overrides[get_settings] = get_settings_override


@pytest.fixture
async def client() -> TestClient:
    # Cannot use fastapi/starlette test client because async is needed here.
    # Nor httpx test client until it support asgi application lifespan somehow,
    # see: https://github.com/tiangolo/fastapi/issues/1273
    # and here: https://github.com/encode/starlette/issues/652
    async with TestClient(app) as client:
        yield client


@pytest.fixture
async def redis_client() -> aioredis.Redis:
    redis = await aioredis.create_redis(get_settings_override().redis_dsn)
    yield redis
    # An error is logged when aioredis connection is not cleaned up properly.
    redis.close()
