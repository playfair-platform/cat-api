from pydantic import BaseModel, Field, ConfigDict, model_validator
from catd.utils import remove_html_tags, extract_links
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


class WikiPage(BaseModel):
    page_id: int
    title: str
    content: str
    extracted_links: list[str]  = []


    @model_validator(mode="after")
    def post_process_content(self):
        """Post process content, such as removing tags and creating sections."""
        if self.content:
            self.content = remove_html_tags(self.content)
            self.extracted_links = extract_links(self.content)
        return self
    