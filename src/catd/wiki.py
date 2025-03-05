from catd.models.wiki import QueryResult
from functools import partial
from .utils import request


class Wiki:
    BASE_URL = "https://wiki.rossmanngroup.com/api.php"

    @staticmethod
    def _query(search: str) -> list[QueryResult]:
        """Searches Wiki

        Args:
            search: the search string"""
        params = {
            "action": "query",
            "list": "search",
            "srsearch": search,
            "format": "json",
        }
        res = request(url=Wiki.BASE_URL, payload=params)
        pages = res.get("query")
        if not pages:
            return []
        items = pages.get("search")
        if not items:
            return []

        data = [
            QueryResult.model_validate(
                {**item, "get": partial(Wiki._get_page_by_id, item["pageid"])}
            )
            for item in items
        ]
        return data

    def _get_page_by_id(id: int):
        """Gets Wiki page by ID"""
        uri = Wiki.BASE_URL + f"?curid={id}"
        res = request(uri, {})

    def get_page(*, page_id: int):
        """Gets a Wiki page by different identifiers such as ID

        Keyword Args:
            page_id: the page ID. Can be found by _query method."""

        if page_id:
            params = 1
