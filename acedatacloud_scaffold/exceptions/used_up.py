from django.utils.translation import gettext_lazy as _
from rest_framework import status
from .base import APIException


class UsedUpException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _(
        'Your packaged has been used up, please buy more in system.')
    default_code = 'used_up'
