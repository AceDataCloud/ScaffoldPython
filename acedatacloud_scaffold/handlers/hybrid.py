from acedatacloud_scaffold.handlers.callback import CallbackHandler


class HybridHandler(CallbackHandler):

    def write_success(self, data, status=200, headers={}):
        if self.async_mode:
            self.write_error_async(data, status=status, headers=headers)
        else:
            self.write_error_sync(data, status=status, headers=headers)

    def write_error(self, status_code, **kwargs):
        if self.async_mode:
            self.write_error_async(status_code, **kwargs)
        else:
            self.write_error_sync(status_code, **kwargs)
