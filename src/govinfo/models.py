from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Result:
    def __init__(self, status_code: int, message: str = "", data: dict = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else {}


class GovinfoModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class SummaryItem(GovinfoModel):
    collection_code: str
    collection_name: str
    package_count: int
    granule_count: int | None


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


class GranuleMetadata(GovinfoModel):
    title: str
    granule_id: str
    granule_link: str
    granule_class: str
    md5: str = Field(default=None)


class GranuleContainer(GovinfoModel):
    count: int
    offset: int | None
    page_size: int
    next_page: str | None
    previous_page: str | None
    granules: list[GranuleMetadata]
    message: str = Field(default=None)


class PackageSummary(GovinfoModel):
    # "allow" since there are so many variations on what is returned
    model_config = ConfigDict(extra="allow")
    category: str
    date_issued: str
    collection_code: str
    collection_name: str
    doc_class: str
    publisher: str
    last_modfied: str
    branch: str
    # TODO: specify download model
    download: dict
    # TODO: specify other_identifier model
    other_identifier: dict


# TODO: create models that inherit from PackageSummary for specific packages types
# start with BILLS, PLAW, CREC, CRPT, CPRT
