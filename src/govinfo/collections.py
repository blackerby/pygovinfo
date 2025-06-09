from govinfo.config import PAGE_DEFAULT, OFFSET_DEFAULT
from govinfo.exceptions import GovinfoException
from govinfo.models import GovinfoModel
from govinfo.packages import PackageInfo
from pydantic.networks import HttpUrl


class SummaryItem(GovinfoModel):
    collection_code: str
    collection_name: str
    package_count: int
    granule_count: int | None


class CollectionSummary(GovinfoModel):
    collections: list[SummaryItem]


class CollectionContainer(GovinfoModel):
    count: int
    message: str | None
    next_page: HttpUrl | None
    previous_page: HttpUrl | None
    packages: list[PackageInfo]


class CollectionsMixin:
    def collections(
        self,
        collection: str = None,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ):
        endpoint_parts = ["collections", collection, start_date, end_date]
        endpoint = "/".join(part for part in endpoint_parts if part is not None)
        page_size = kwargs.get("pageSize", PAGE_DEFAULT)
        offset_mark = kwargs.get("offsetMark", OFFSET_DEFAULT)
        params = {"pageSize": page_size, "offsetMark": offset_mark}

        try:
            result = self._get(endpoint, params=params)
        except GovinfoException as e:
            raise e

        if collection is None:
            validated = CollectionSummary(**result.data)
        else:
            validated = CollectionContainer(**result.data)
        # TODO: dump with(out) alias?
        return validated.model_dump()
