from acedatacloud_scaffold.handlers.callback import CallbackHandler
import json
from acedatacloud_scaffold.exceptions import BadRequestException


class HybridHandler(CallbackHandler):

    def initialize_async_context(self):
        try:
            request_body = self.request.body.decode('utf-8')
            post_json = json.loads(request_body)
            callback_url = post_json.get('callback_url')
            if callback_url:
                self.async_mode = True
                self.callback_url = callback_url
                self.index_written = False
            else:
                self.async_mode = False
                self.callback_url = None
        except Exception:
            self.logger.error('error initializing async context')
            raise BadRequestException(
                'error when parsing request body for callback url')

    def write_success(self, data, status=200, headers={}):
        if self.async_mode:
            self.write_success_async(data, status=status, headers=headers)
        else:
            self.write_success_sync(data, status=status, headers=headers)

    def write_error(self, status_code, **kwargs):
        if self.async_mode:
            self.write_error_async(status_code, **kwargs)
            if not self.index_written:
                self.write_error_sync(status_code, **kwargs)
        else:
            self.write_error_sync(status_code, **kwargs)
