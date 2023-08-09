from pydantic import BaseModel
from typing import List


class SearchResult(BaseModel):
    id: str
    title: str
    url: str
    score: int
    tags: List[str]
    report_generated: int
