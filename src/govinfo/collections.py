from govinfo.config import PAGE_DEFAULT, OFFSET_DEFAULT
from govinfo.exceptions import GovinfoException
from govinfo.models import CollectionContainer, CollectionSummary


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
