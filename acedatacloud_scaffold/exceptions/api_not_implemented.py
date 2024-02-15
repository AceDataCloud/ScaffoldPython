from .base import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class ApiNotImplementedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('The API is not implemented.')
    default_code = 'api_not_implemented'
