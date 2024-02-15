from django.utils.translation import gettext_lazy as _
from rest_framework import status
from .base import APIException


class NoApiException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('API does not exist, please make sure url is correct.')
    default_code = 'no_api'
