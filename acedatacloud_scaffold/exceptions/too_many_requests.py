from rest_framework import status
from .base import APIException


class TooManyRequestsException(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'too_many_requests'
