from acedatacloud_scaffold.handlers.base import BaseHandler
import json
from loguru import logger
import requests
from acedatacloud_scaffold.settings import \
    ERROR_STATUS_API_ERROR, ERROR_CODE_API_ERROR
from acedatacloud_scaffold.exceptions import APIException, BadRequestException


class CallbackHandler(BaseHandler):

    def initialize(self):
        super().initialize()
        self.initialize_async_context()

    @logger.catch
    def send_callback(self, data):
        self.logger.debug(f'{self.trace_id} callback url {self.callback_url}')
        self.logger.debug(f'{self.trace_id} callback data {data}')
        response = requests.post(self.callback_url, json=data)
        self.logger.debug(f'{self.trace_id} callback response {response}')

    def write_success_async(self, data, status=200, headers={}):
        # append task id
        data['task_id'] = self.task_id
        # append trace id
        data['trace_id'] = self.trace_id
        data['success'] = True
        self.send_callback(data)

    def write_index(self):
        self.write_json({
            'task_id': self.task_id,
        })
        self.finish()
        self._finished = False
        # this flag used for checking if headers has been written,
        # if headers not written, we can continue return error sync
        self._headers_written = False
        # this flag used for checking if index has been written,
        # if index not written, we can return error sync
        self.index_written = True

    def write_success(self, data, status=200, headers={}):
        self.write_success_async(data, status=status, headers=headers)

    def write_error(self, status_code, **kwargs):
        self.write_error_async(status_code, **kwargs)
        if not self.index_written:
            self.write_error_sync(status_code, **kwargs)

    def write_error_async(self, status_code, **kwargs):
        self.logger.error(f'error happened {kwargs}')
        exception = None
        if "exc_info" in kwargs:
            exception = kwargs["exc_info"][1]
        self.logger.exception(f'error {exception}')
        data = {}
        status = exception.status_code if hasattr(
            exception, 'status_code') else (status_code or
                                            ERROR_STATUS_API_ERROR)
        self.logger.debug(f'{self.trace_id} error status {status}')
        # construct error
        data = {
            'task_id': self.task_id,
            'trace_id': self.trace_id,
            'success': False,
            'error': {
                'code': (exception.code if hasattr(exception, 'code') else
                         exception.default_code) if isinstance(exception, APIException) else ERROR_CODE_API_ERROR,
                'message': exception.detail if isinstance(exception, APIException) else str(exception),
            }
        }
        self.send_callback(data)
        self.logger.debug(f'write error {data}')

    def initialize_async_context(self):
        try:
            request_body = self.request.body.decode('utf-8')
            post_json = json.loads(request_body)
            callback_url = post_json.get('callback_url')
            if not callback_url:
                raise BadRequestException('callback_url is required')
            self.index_written = False
        except Exception:
            pass
