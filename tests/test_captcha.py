import asyncio
import base64

import aioredis
from PIL import Image
import pytest
from io import BytesIO

from async_asgi_testclient import TestClient


pytestmark = pytest.mark.asyncio


async def test_get_captcha(client: TestClient):
    response = await client.get("/captcha")
    assert response.status_code == 200

    data = response.json()
    assert data['id']

    image_bytes = base64.b64decode(data['image'])
    assert Image.open(BytesIO(image_bytes)).format == 'PNG'


async def test_solve_captcha(client: TestClient, redis_client: aioredis.Redis):
    key = 'testing_solution'
    solution = 'ok'
    await redis_client.set(key, solution, expire=6)

    response = await client.post("/captcha", json={
        'id': key,
        'answer': solution,
    })
    assert response.status_code == 200


async def test_expired_captcha(client: TestClient, redis_client: aioredis.Redis):
    key = 'testing_expired_solution'
    await redis_client.set(key, 'ok', expire=1)

    await asyncio.sleep(1)

    response = await client.post("/captcha", json={
        'id': key,
        'answer': 'not ok',
    })
    assert response.status_code == 408


async def test_wrong_solve_captcha(client, redis_client):
    key = 'testing_wrong_solution'
    await redis_client.set(key, 'ok', expire=6)

    response = await client.post("/captcha", json={
        'id': key,
        'answer': 'not ok',
    })
    assert response.status_code == 400
