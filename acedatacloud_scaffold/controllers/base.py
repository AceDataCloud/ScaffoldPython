from loguru import logger
from uuid import uuid4
import asyncio
import tornado
from acedatacloud_scaffold.handlers import HealthHandler
from acedatacloud_scaffold.settings import HTTP_PORT


class BaseController(object):

    def __init__(self):
        self.id = str(uuid4())
        self.application = tornado.web.Application([
            (r"/health", HealthHandler),
        ])

    def add_handler(self, path, handler):
        self.application.add_handlers(
            '.*', [(path, handler)])
        logger.debug(f'add handler {path}')

    async def main(self):
        self.application.listen(HTTP_PORT)
        await asyncio.Event().wait()

    def start(self):
        asyncio.run(self.main())
