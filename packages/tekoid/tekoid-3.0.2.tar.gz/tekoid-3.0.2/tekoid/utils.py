import urllib
from urllib.parse import urlparse, parse_qs
import base64
from hashlib import sha256
import random
import string

pattern = ''.join((string.ascii_uppercase, string.ascii_lowercase, string.digits))


def get_url_encode_from_dict(query):
    return urllib.parse.urlencode(query)


def get_dict_from_url(url):
    return parse_qs(urlparse(url).query)


def create_sha256_code_challenge(code_verifier):
    code_challenge = base64.urlsafe_b64encode(sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')

    code_challenge = code_challenge.replace('=', '')
    code_challenge = code_challenge.replace('+', '-')
    code_challenge = code_challenge.replace('/', '_')
    return code_challenge


def get_random_string(len=50):
    return ''.join(random.choice(pattern) for _ in range(len))
