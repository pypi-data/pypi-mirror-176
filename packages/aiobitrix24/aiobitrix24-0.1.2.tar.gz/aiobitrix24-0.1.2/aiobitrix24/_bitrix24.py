"""Main bitrix24 module."""
import asyncio
import time

import httpx

from aiobitrix24 import _builders
from aiobitrix24.methods import BATCH

BITRIX_REQUEST_TIMEOUT = 20


class Bitrix24:
    """Class for making bitrix24 requests."""

    def __init__(self, url: str, sleep_sec: int = 5) -> None:
        """Init class.

        :param url: base url for bitrix24 rest api
        :param sleep_sec: sleep seconds between queries
        """
        self.url = url
        self.sleep_sec = sleep_sec
        self.last_request_time = time.time() - sleep_sec

    async def request(
        self,
        method: str,
        query_params: dict,
        is_query_complex: bool = False,
    ) -> httpx.Response:
        """Request to bitrix24.

        :param method: call method
        :param query_params: query params
        :param is_query_complex: build custom param string, defaults to False
        :return: http response
        """
        await self._sleep()
        async with httpx.AsyncClient() as client:
            if is_query_complex:
                complex_query = _builders.build_query(query_params)
                return await client.post(
                    f"{self.url}{method}?{complex_query}",
                    timeout=BITRIX_REQUEST_TIMEOUT,
                )
            return await client.post(
                f"{self.url}{method}",
                json=query_params,
                timeout=BITRIX_REQUEST_TIMEOUT,
            )

    async def batch_request(
        self, queries: list[_builders.BatchQuery],
    ) -> httpx.Response:
        """Batch request to bitrix24.

        :param queries: batch of queries
        :return: http response
        """
        await self._sleep()
        batch_query = _builders.build_batch(queries)
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{self.url}{BATCH}",
                json=batch_query,
                timeout=BITRIX_REQUEST_TIMEOUT,
            )

    async def _sleep(self) -> None:
        current_time = time.time()
        if current_time - self.last_request_time < self.sleep_sec:
            self.last_request_time = current_time + self.sleep_sec
            await asyncio.sleep(self.sleep_sec)
        else:
            self.last_request_time = current_time
