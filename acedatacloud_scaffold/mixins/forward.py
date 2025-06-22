import httpx
from acedatacloud_scaffold.settings import DEFAULT_TIMEOUT_FORWARD


class ForwardMixin(object):

    async def get_forward_request_timeout(self):
        return httpx.Timeout(DEFAULT_TIMEOUT_FORWARD, read=None)

    async def get_forward_request_proxy(self):
        return None

    async def get_forward_request_method(self):
        return self.request.method if self.request else None

    async def get_forward_request_url(self):
        return self.request.uri if self.request else None

    async def get_forward_request_headers(self):
        return self.request.headers if self.request else None

    async def get_forward_request_body(self):
        return self.request.body if self.request else None

    async def get_forward_response_status(self):
        return self.forward_response.status_code \
            if hasattr(self, 'forward_response') else None

    async def get_forward_request_params(self):
        return None

    async def get_forward_response_headers(self):
        return self.forward_response.headers \
            if hasattr(self, 'forward_response') else None

    async def get_forward_response_body(self):
        if not hasattr(self, 'forward_response'):
            return
        async for data in self.forward_response.aiter_raw():
            yield data

    async def write_response_body(self):
        async for data in self.get_forward_response_body():
            self.logger.debug(
                f'write data {data}')
            self.write(data)
        self.logger.debug('finish write data')
        self.finish()

    async def write_response_status(self):
        forward_response_status = await self.get_forward_response_status()
        self.set_status(forward_response_status)

    async def write_response_headers(self):
        # set response headers
        forward_response_headers = await self.get_forward_response_headers()
        for header, value in forward_response_headers.items():
            self.logger.debug(
                f'set header {header} {value}')
            self.set_header(header, value)

    async def forward(self):
        self.logger.debug('start to forward request')
        # forward info for building forward request
        forward_timeout = await self.get_forward_request_timeout()
        forward_url = await self.get_forward_request_url()
        forward_headers = await self.get_forward_request_headers()
        forward_body = await self.get_forward_request_body()
        forward_method = await self.get_forward_request_method()
        forward_params = await self.get_forward_request_params()

        async with httpx.AsyncClient(
                **{
                    'timeout': forward_timeout,
                    'proxy': await self.get_forward_request_proxy()
                }) as client:
            self.logger.debug(
                f'forward_url {forward_url} forward_headers {forward_headers} forward_body {forward_body} forward_params {forward_params}')
            async with client.stream(
                forward_method,
                forward_url,
                params=forward_params,
                headers=forward_headers,
                data=forward_body,
            ) as response:
                self.forward_response = response
                self.logger.debug(
                    f'forward response {self.forward_response}')
                await self.write_response_status()
                await self.write_response_headers()
                await self.write_response_body()
