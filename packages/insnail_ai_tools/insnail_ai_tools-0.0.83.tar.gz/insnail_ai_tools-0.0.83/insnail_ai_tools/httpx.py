from typing import Dict, List, Union

import httpx
from httpx import Response


async def aio_get(url: str, **kwargs) -> Response:
    async with httpx.AsyncClient() as client:
        return await client.get(url, **kwargs)


async def aio_post(
    url: str, json: Union[Dict, List] = None, data: Union[Dict, List] = None, **kwargs
) -> Response:
    async with httpx.AsyncClient() as client:
        return await client.post(url, json=json, data=data, **kwargs)


async def aio_head(url: str, *args, **kwargs) -> Response:
    async with httpx.AsyncClient() as client:
        return await client.head(url, *args, **kwargs)
