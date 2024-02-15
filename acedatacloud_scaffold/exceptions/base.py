from rest_framework.exceptions import APIException as BaseAPIException


class APIException(BaseAPIException):

    def __init__(self, detail=None, code=None):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code
