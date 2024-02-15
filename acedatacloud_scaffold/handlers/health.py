from .base import BaseHandler


class HealthHandler(BaseHandler):

    def get(self):
        self.write("ok")
