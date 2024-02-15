import httpx
from acedatacloud_scaffold.settings import DEFAULT_TIMEOUT_FORWARD


class ForwardMixin(object):

    async def get_forward_request_timeout(self):
        return httpx.Timeout(DEFAULT_TIMEOUT_FORWARD, read=None)

    async def get_forward_request_url(self):
        return self.request.uri

    async def get_forward_request_headers(self):
        return self.request.headers

    async def get_forward_request_body(self):
        return self.request.body

    async def get_forward_response_status(self):
        return self.forward_response.status_code

    async def get_forward_response_headers(self):
        return self.forward_response.headers

    async def get_forward_response_body(self):
        async for data in self.forward_response.aiter_raw():
            yield data

    async def forward(self):
        # forward info for building forward request
        forward_timeout = await self.get_forward_request_timeout()
        forward_url = await self.get_forward_request_url()
        forward_headers = await self.get_forward_request_headers()
        forward_body = await self.get_forward_request_body()
        forward_method = await self.get_forward_request_method()

        async with httpx.AsyncClient(timeout=forward_timeout) as client:
            self.logger.debug(
                f'forward_url {forward_url} forward_headers {forward_headers} forward_body {forward_body}')
            async with client.stream(
                forward_method,
                forward_url,
                headers=forward_headers,
                data=forward_body,
            ) as response:
                self.forward_response = response
                self.logger.debug(
                    f'forward response {self.forward_response}')
                # set response status
                forward_response_status = await self.get_forward_response_status()
                self.set_status(forward_response_status)
                # set response headers
                forward_response_headers = self.get_forward_response_headers()
                for header, value in forward_response_headers.items():
                    self.logger.debug(
                        f'set header {header} {value}')
                    self.set_header(header, value)
                # set response body
                async for data in self.get_forward_response_body():
                    self.logger.debug(
                        f'write data {data}')
                    self.write(data)
                self.logger.debug('finish write data')
                self.finish()