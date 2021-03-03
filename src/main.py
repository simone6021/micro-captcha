import base64
import uuid

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.memory import CACHE_KEY, InMemoryCacheBackend
from pydantic import BaseModel

from utils import generate_random_text, generate_captcha_image


app = FastAPI()


def cache():
    return caches.get(CACHE_KEY)


@app.on_event('startup')
async def on_startup() -> None:
    rc = InMemoryCacheBackend()
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


class CaptchaAnswer(BaseModel):
    id: str
    answer: str


@app.get('/captcha')
async def get_captcha(cache: InMemoryCacheBackend = Depends(cache)):
    captcha_id = uuid.uuid4().hex
    answer = generate_random_text()
    await cache.set(captcha_id, answer, ttl=360)

    image = generate_captcha_image(answer)

    return {
        'captcha_id': captcha_id,
        'image': base64.b64encode(image.read()),
    }


@app.post('/captcha')
async def solve_captcha(data: CaptchaAnswer, cache: InMemoryCacheBackend = Depends(cache)):
    captcha_id = data.id
    answer = data.answer

    solution = await cache.get(captcha_id)
    if solution is None:
        raise HTTPException(status_code=404, detail='Captcha is expired.')

    await cache.delete(captcha_id)

    if answer != solution:
        raise HTTPException(status_code=400, detail='Captcha not solved.')

    return {}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
