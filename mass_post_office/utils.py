# coding: utf-8
import zlib
import pickle
import hashlib
import urllib
import base64

import settings


def encode_data(data):
    """Turn `data` into a hash and an encoded string, suitable for use with
    `decode_data`.

    """
    text = base64.b64encode(zlib.compress(
        pickle.dumps(data, 0)
    )).replace('+', '.').replace('/', '-')
    m = hashlib.md5(settings.SECRET_KEY + text).hexdigest()[:12]
    return m, text


def decode_data(hashed, enc):
    """The inverse of `encode_data`.

    """
    text = urllib.unquote(enc)
    m = hashlib.md5(settings.SECRET_KEY + text).hexdigest()[:12]
    if m != hashed:
        raise ValueError("Bad hash!")
    text = text.replace('-', '/').replace('.', '+')
    data = pickle.loads(zlib.decompress(text.decode('base64')))
    return data
