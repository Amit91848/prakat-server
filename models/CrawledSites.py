from beanie import Document
from typing import List


class crawled_sites(Document):
    url: str
    title: str
    body: str
    ner_done: bool
    tags: List[str]
    report_generated: bool
    reportId: str | None
