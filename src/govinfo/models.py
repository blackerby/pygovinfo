from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_snake


class Result:
    def __init__(self, status_code: int, message: str = "", data: dict = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else {}


class GovinfoModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_snake)


class SummaryItem(GovinfoModel):
    collectionCode: str
    collectionName: str
    packageCount: int
    granuleCount: int | None


class CollectionSummary(GovinfoModel):
    collections: list[SummaryItem]


class PackageInfo(GovinfoModel):
    package_id: str
    last_modified: str
    package_link: str
    doc_class: str
    title: str
    congress: str
    date_issued: str


class CollectionContainer(GovinfoModel):
    count: int
    message: str | None
    next_page: str | None
    previous_page: str | None
    packages: list[PackageInfo]
