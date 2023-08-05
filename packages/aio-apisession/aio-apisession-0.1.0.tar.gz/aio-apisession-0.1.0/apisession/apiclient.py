# APIO is a asynchronous aiohttp-based general purpose client
# with features for common API integration scenarios
from typing import Optional, Union
import logging

import aiohttp
from aiohttp.client_exceptions import ClientPayloadError
from yarl import URL

logger = logging.getLogger(__name__)


class APISession:
    def __init__(
        self,
        name: str = 'default',
        url: Optional[Union[str, URL]] = None,
        middlewares: list = None,
        **kwargs
    ):
        self._name = name
        self._url = None if url is None else URL(url)
        self._session = aiohttp.ClientSession(**kwargs)
        self._request_handlers = [
            m.handle_request
            for m in middlewares
            if hasattr(m, 'handle_request')
        ]
        self._response_handlers = [
            m.handle_response
            for m in middlewares
            if hasattr(m, 'handle_response')
        ]

    async def get(self, url: Union[str, URL], **kwargs):
        return await self.request('GET', url, **kwargs)

    async def post(self, url: Union[str, URL], **kwargs):
        return await self.request('POST', url, **kwargs)

    async def request(self, method: str, url: Union[str, URL], **kwargs):
        '''Alias for ClientSession request:
            - Performs request on integration's client
            - Supports URLs relative to the integration's base URL
            - URL passed as first and only positional argument
            - Throttles requests according to `max_requests_per_minute`
        '''
        kwargs['method'] = kwargs.get('method', 'GET')

        request_url = (
            URL(url)
            if self._url is None
            else self._url.join(URL(url))
        )

        request = {
            'url': request_url,
            **kwargs,
        }

        for handler in self._request_handlers:
            request = await handler(request)

        response = await self._session.request(**request)

        logger.info(f'[{self._name}] Response: {response.status} {url}')
        logger.debug(f'[{self._name}] Sent: {kwargs}')
        logger.debug(f'[{self._name}] Headers received:', response.headers)

        for handler in self._response_handlers:
            response = await handler(response)
            if response is None:
                return

        try:
            logger.debug(
                '[{}] Body received: {}'
                .format(self._name, await response.text())
            )
        except UnicodeDecodeError:
            logger.info(
                '[{}] Body received: {} bytes, non-utf8 data'.format(
                    self._name, len(await response.read())
                )
            )
        except ClientPayloadError:
            logger.info(f'[{self._name}] Client Payload Error')

        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        return await self._session.close()
