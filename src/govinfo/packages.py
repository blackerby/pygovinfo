from datetime import date, datetime

from govinfo.config import PAGE_DEFAULT, OFFSET_DEFAULT
from govinfo.exceptions import GovinfoException
from govinfo.models import Branch, GovinfoModel

from pydantic import ConfigDict, Field
from pydantic.networks import HttpUrl


class PackageInfo(GovinfoModel):
    package_id: str
    last_modified: datetime
    package_link: HttpUrl
    doc_class: str
    title: str
    congress: int
    date_issued: date


class GranuleMetadata(GovinfoModel):
    title: str
    granule_id: str
    granule_link: HttpUrl
    granule_class: str
    md5: str = Field(default=None)


class GranuleContainer(GovinfoModel):
    count: int
    offset: int | None
    page_size: int
    next_page: HttpUrl | None
    previous_page: HttpUrl | None
    granules: list[GranuleMetadata]
    message: str = Field(default=None)


class PackageSummary(GovinfoModel):
    # "allow" since there are so many variations on what is returned
    model_config = ConfigDict(extra="allow")
    category: str
    date_issued: date
    collection_code: str
    collection_name: str
    doc_class: str
    publisher: str
    last_modfied: datetime
    branch: Branch
    # TODO: specify download model
    download: dict
    # TODO: specify other_identifier model
    other_identifier: dict


# TODO: create models that inherit from PackageSummary for specific packages types
# start with BILLS, PLAW, CREC, CRPT, CPRT


class PackagesMixin:
    def granules(
        self,
        package_id: str,
        offset: int = None,
        page_size: int = PAGE_DEFAULT,
        md5: str = None,
        granule_class: str = None,
        offset_mark: str = OFFSET_DEFAULT,
    ):
        endpoint = f"packages/{package_id}/granules"
        params = self._set_query_params(
            offset, page_size, md5, granule_class, offset_mark
        )

        try:
            result = self._get(endpoint, params=params)
        except GovinfoException as e:
            raise e

        validated = GranuleContainer(**result.data)
        return validated.model_dump()

    def _set_query_params(
        self, offset, page_size, md5, granule_class, offset_mark
    ) -> dict[str]:
        params = {"pageSize": page_size, "offsetMark": offset_mark}

        if offset:
            params["offset"] = offset
        if md5:
            params["md5"] = md5
        if granule_class:
            params["granuleClass"] = granule_class

        return params
