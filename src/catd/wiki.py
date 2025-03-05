from catd.models.wiki import QueryResult, WikiPage
from functools import partial
from .utils import request


class Wiki:
    BASE_URL = "https://wiki.rossmanngroup.com/api.php"

    def default_param() -> dict[str, str]:
        return {
            "action": "query",
            "format": "json",
        }

    @staticmethod
    def search(search: str) -> list[QueryResult]:
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
                {**item, "get_page": partial(Wiki._get_page_by_id, item["pageid"])}
            )
            for item in items
        ]
        return data

    def _get_page_content(revision: dict):
        try:
            return revision[0]['slots']['main']['*']
        except KeyError:
            return ""
        
    @staticmethod
    def _get_page_by_id(id: int):
        """Gets Wiki page by ID
        
        Args:
            id: the ID of the page."""
        res = request(
            Wiki.BASE_URL,
            {
                "pageids": id,
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "main",
                **Wiki.default_param(),
            },
        )
        query = res.get("query")
        if query:
            try:
                page_content = query['pages'][str(id)]
                title = page_content['title']
                page_meta = page_content['revisions']
                content = Wiki._get_page_content(page_meta)
                return WikiPage(page_id=id, title=title, content=content)
            except Exception as ex:
                raise WikiPageError("Could not find page by ID.", ex)
            
    @staticmethod
    def _get_page_by_title(title: str):
        """Gets Wiki page by title
        
        Args:
            id: the exact title of the page."""
        res = request(
            Wiki.BASE_URL,
            {
                "titles": title,
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "main",
                **Wiki.default_param(),
            },
        )
        query = res.get("query")
        if query:
            try:
                page_id = list(query['pages'].keys())[0]
                if page_id == -1:
                    raise KeyError("ss")

                page_content = query['pages'][str(page_id)]
                title = page_content['title']
                page_meta = page_content['revisions']
                content = Wiki._get_page_content(page_meta)
                return WikiPage(page_id=page_id, title=title, content=content)
            except Exception as ex:
                raise WikiPageError("Could not find page by title.", ex)

    
    def get_page(*, page_id: int):
        """Gets a Wiki page by different identifiers such as ID

        Keyword Args:
            page_id: the page ID. Can be found by _query method."""

        if page_id:
            return Wiki._get_page_by_id(page_id)


class WikiPageError(Exception):
    def __init__(self, message: str, response_data: dict = None):
        super().__init__(message + f"\n{response_data}")
        self.response_data = response_data