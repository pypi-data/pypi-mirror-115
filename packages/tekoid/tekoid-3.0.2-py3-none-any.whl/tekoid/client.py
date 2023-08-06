import requests
from requests.exceptions import Timeout
from .errors import UnauthorizedException, NotFoundException, InternalServerErrorException, TimeoutException


class Client(requests.Session):
    def __init__(self, verify_ssl, request_timeout):
        super().__init__()
        self.verify_ssl = verify_ssl
        self.request_timeout = request_timeout

    def request(self, method, url, *args, **kwargs):
        try:
            res = super().request(method, url, verify=self.verify_ssl, timeout=self.request_timeout, *args, **kwargs)
        except Timeout:
            raise TimeoutException(message=f'Timeout when {method} data to {url}')

        if res.status_code == 401:
            raise UnauthorizedException(message=f'Unauthorized when {method} data to {url}')
        elif res.status_code == 404:
            raise NotFoundException(message=f'Not found when {method} data to {url}')
        elif res.status_code == 500:
            raise InternalServerErrorException()
        return res
