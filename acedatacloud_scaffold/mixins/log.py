from loguru import logger


class LogMixin(object):

    def log(self, level, message):
        """
        Custom log method that includes the trace ID.
        """
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        trace_message = f"[{self.trace_id}] {message}"
        getattr(logger, level)(trace_message)

    @property
    def logger(self):
        """
        Expose a logger-like interface that automatically includes the trace ID.
        """
        class LoggerAdapter:
            def __init__(self, outer):
                self.outer = outer

            def debug(self, message):
                self.outer.log('debug', message)

            def info(self, message):
                self.outer.log('info', message)

            def warning(self, message):
                self.outer.log('warning', message)

            def error(self, message):
                self.outer.log('error', message)

            def critical(self, message):
                self.outer.log('critical', message)

            def exception(self, message):
                self.outer.log('exception', message)

        return LoggerAdapter(self)
