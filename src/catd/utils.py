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


def extract_links(text):
    """Regex expression to match URLs (HTTP, HTTPS, www)

    Args:
        text: the content/article to search for
    """
    pattern = r'https?://[^\s)>\]\'",]+|www\.[^\s)>\]\'",]+'
    skip_list = ["archive.org"]
    links = re.findall(pattern, text)

    cleaned_links = []

    for link in links:
        should_skip = 0
        for skip in skip_list:
            if link.find(skip) >= 0:
                should_skip = 1
        if should_skip:
            cleaned_links.append(link)
            continue
        link_fwd = link[8:]
        # checking beyond first http protocol
        if "http" in link_fwd:
            # resplit at new appearances
            parts = re.split(r"(?=https?://.)", link)
            cleaned_links.extend(parts)
        else:
            cleaned_links.append(link)
    cleaned_links = [re.sub(r"[\.,'}]+$", "", link) for link in cleaned_links]

    return cleaned_links
