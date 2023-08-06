import json


class SdkException(Exception):
    status_code = 500
    message = 'Internal Server Error'

    def __init__(self, code=None, message=None):
        self.code = code or self.status_code
        self.message = message or self.message
        self.error = '{}: {}'.format(self.code, self.message)

    def __str__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.error)


class StateInvalidException(SdkException):
    status_code = 4001
    message = 'invalid state'


class NonceInvalidException(SdkException):
    status_code = 4002
    message = 'invalid nonce'


class UnauthorizedException(SdkException):

    status_code = 4011


class NotFoundException(SdkException):

    status_code = 4041


class InternalServerErrorException(SdkException):

    status_code = 5001


class TimeoutException(SdkException):

    status_code = 5041
