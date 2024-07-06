from loguru import logger
from acedatacloud_scaffold.exceptions import APIException
import json
from acedatacloud_scaffold.settings import \
    ERROR_STATUS_API_ERROR, ERROR_CODE_API_ERROR, RECORD_SERVER_URL
from tornado.web import RequestHandler
from acedatacloud_scaffold.mixins import LogMixin
from uuid import uuid4
import requests


class BaseHandler(RequestHandler, LogMixin):

    def write_json(self, data, status=200, headers={}):
        self.clear()
        self.set_status(status)
        self.set_header('Content-Type', 'application/json')
        for key, value in headers.items():
            self.set_header(key, value)
        self.write(json.dumps(data, ensure_ascii=False))
        self.logger.debug(f'write json {data}')

    def write_success_sync(self, data, status=200, headers={}):
        self.write_json(data, status=status, headers=headers)
        self.finish()

    def write_success(self, data, status=200, headers={}):
        self.write_success_sync(data, status=status, headers=headers)

    def write_error(self, status_code, **kwargs):
        self.write_error_sync(status_code, **kwargs)

    def write_error_sync(self, status_code, **kwargs):
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
            'trace_id': self.trace_id,
            'error': {
                'code': (exception.code if hasattr(exception, 'code') else
                         exception.default_code) if isinstance(exception, APIException) else ERROR_CODE_API_ERROR,
                'message': exception.detail if isinstance(exception, APIException) else str(exception),
            }
        }
        self.write_json(data, status=status)
        self.logger.debug(f'write error {data}')
        self.finish()

    def get_record_application_id(self):
        return self.application_id

    def get_record_trace_id(self):
        return self.trace_id

    def get_record_api_id(self):
        return self.api_id

    def get_record_task_id(self):
        return self.task_id

    def get_record_user_id(self):
        return self.user_id

    def get_record_credential_id(self):
        return self.credential_id

    def get_record_request(self):
        return {
            'body': self.request.body.decode('utf-8'),
            'json': json.loads(self.request.body),
            'headers': dict(self.request.headers),
            'method': self.request.method,
        }

    def get_record_response(self):
        return {
            'status': self.get_status(),
        }

    @logger.catch
    def record(self, extra_data={}):
        record_server_url = RECORD_SERVER_URL
        self.logger.debug(f'record url {record_server_url}')
        data = {
            'trace_id': self.get_record_trace_id(),
            'application_id': self.get_record_application_id(),
            'api_id': self.get_record_api_id(),
            'task_id': self.get_record_task_id(),
            'user_id': self.get_record_user_id(),
            'credential_id': self.get_record_credential_id(),
            'request': self.get_record_request(),
            'response': self.get_record_response()
        }
        data.update(extra_data)
        logger.debug(f'{self.trace_id} record data {data}')
        response = requests.post(record_server_url, json=data)
        logger.debug(f'{self.trace_id} record response {response}')

    def initialize_trace_id(self):
        trace_id = self.request.query_arguments.get('trace_id')
        self.trace_id = trace_id[0].decode(
            'utf-8') if trace_id and len(trace_id) > 0 else str(uuid4())
        logger.debug(f'trace id {self.trace_id}')

    def initialize_credential_id(self):
        credential_id = self.request.query_arguments.get('credential_id')
        self.credential_id = credential_id[0].decode(
            'utf-8') if credential_id and len(credential_id) > 0 else None
        logger.debug(f'credential id {self.credential_id}')

    def initialize_user_id(self):
        user_id = self.request.query_arguments.get('user_id')
        self.user_id = user_id[0].decode(
            'utf-8') if user_id and len(user_id) > 0 else None
        logger.debug(f'user id {self.user_id}')

    def initialize_api_id(self):
        api_id = self.request.query_arguments.get('api_id')
        self.api_id = api_id[0].decode(
            'utf-8') if api_id and len(api_id) > 0 else None
        logger.debug(f'api id {self.api_id}')

    def initialize_application_id(self):
        application_id = self.request.query_arguments.get('application_id')
        self.application_id = application_id[0].decode(
            'utf-8') if application_id and len(application_id) > 0 else None
        logger.debug(f'application id {self.application_id}')

    def initialize_task_id(self):
        self.task_id = str(uuid4())
        logger.debug(f'task id {self.task_id}')

    def initialize(self):
        self.initialize_trace_id()
        self.initialize_task_id()
        self.initialize_application_id()
        self.initialize_api_id()
        self.initialize_user_id()
        self.initialize_credential_id()
