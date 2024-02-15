from rest_framework import status
from .base import APIException


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_request'
