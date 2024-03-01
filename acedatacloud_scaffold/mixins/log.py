from loguru import logger


class LogMixin(object):

    def log(self, level, message, *args, **kwargs):
        """
        Custom log method that includes the trace ID.
        """
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        trace_message = f"[{self.trace_id}] {message}"
        getattr(logger, level)(trace_message, *args, **kwargs)

    @property
    def logger(self):
        """
        Expose a logger-like interface that automatically includes the trace ID.
        """
        class LoggerAdapter:
            def __init__(self, outer):
                self.outer = outer

            def debug(self, message, *args, **kwargs):
                self.outer.log('debug', message, *args, **kwargs)

            def info(self, message, *args, **kwargs):
                self.outer.log('info', message, *args, **kwargs)

            def warning(self, message, *args, **kwargs):
                self.outer.log('warning', message, *args, **kwargs)

            def error(self, message, *args, **kwargs):
                self.outer.log('error', message, *args, **kwargs)

            def critical(self, message, *args, **kwargs):
                self.outer.log('critical', message, *args, **kwargs)

            def exception(self, message, *args, **kwargs):
                self.outer.log('exception', message, *args, **kwargs)

        return LoggerAdapter(self)
