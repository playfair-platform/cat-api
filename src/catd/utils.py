import aiohttp
import asyncio
import re

from typing import Any


async def arequest(url: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=payload) as response:
            data = await response.json()
            return data


def request(url: str, payload: dict) -> Any:
    return async_run(arequest(url, payload))


def async_run(coro: Any) -> Any:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def remove_html_tags(text: str) -> str:
    clean = re.sub(r"<.*?>", "", text)
    return clean
