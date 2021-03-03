from typing import Optional, IO
from io import BytesIO
import random
import string

from captcha.image import ImageCaptcha


def generate_random_text(length: int = 5,
                         chars: str = string.digits + string.ascii_lowercase) -> str:
    return "".join(random.sample(chars, length))


def generate_captcha_image(text: str,
                           fp: Optional[IO] = None,
                           rewind: bool = True) -> IO:
    if fp is None:
        fp = BytesIO()

    image = ImageCaptcha()
    image.write(text, fp)

    if rewind:
        fp.seek(0)
    return fp
