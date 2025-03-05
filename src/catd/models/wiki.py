from pydantic import BaseModel, Field, ConfigDict, model_validator
from catd.utils import remove_html_tags
from typing import Callable

class QueryResult(BaseModel):
    title: str
    page_id: int = Field(alias="pageid")
    size: int
    wordcount: int
    snippet: str
    timestamp: str
    get_page: Callable = None

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="after")
    def remove_tags(self):
        """Remove HTML tags after parsing."""
        if self.snippet:
            self.snippet = remove_html_tags(self.snippet)
        return self
