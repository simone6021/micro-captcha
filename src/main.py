import base64
import uuid
from functools import lru_cache

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from settings import Settings
from utils import generate_random_text, generate_captcha_image


@lru_cache()
def get_settings() -> Settings:
    return Settings()


app = FastAPI(
    title="Micro Captcha",
    description="A simple microservice which provides CAPTCHA verification trough http protocol",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def cache():
    return caches.get(CACHE_KEY)


@app.on_event('startup')
async def on_startup() -> None:
    # Necessary for testing, because dependency injection
    # works in path operations only, eg. functions.
    settings = app.dependency_overrides.get(get_settings, get_settings)()

    rc = RedisCacheBackend(settings.redis_dsn)
    # Testing can possibly trigger lifespan events multiple times,
    # and cache registry raise an error if an entry is already registered.
    if caches.get(CACHE_KEY):
        caches.remove(CACHE_KEY)
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


class CaptchaAnswer(BaseModel):
    id: str
    answer: str


@app.get('/captcha')
async def get_captcha(cache: RedisCacheBackend = Depends(cache),
                      settings: Settings = Depends(get_settings)):
    captcha_id = uuid.uuid4().hex
    answer = generate_random_text()
    await cache.set(captcha_id, answer, expire=settings.captcha_id_ttl)

    image = generate_captcha_image(answer)

    return {
        'id': captcha_id,
        'image': base64.b64encode(image.read()),
    }


@app.post('/captcha')
async def solve_captcha(data: CaptchaAnswer,
                        cache: RedisCacheBackend = Depends(cache)):
    captcha_id = data.id
    answer = data.answer

    solution = await cache.get(captcha_id)
    if solution is None:
        raise HTTPException(status_code=408, detail='Captcha is expired.')

    if answer != solution:
        raise HTTPException(status_code=400, detail='Captcha not solved.')

    # This is a friendly captcha and let the user retry
    # until the configured expiration period has passed.
    await cache.delete(captcha_id)

    return ''


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
