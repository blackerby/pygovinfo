from govinfo.config import PAGE_DEFAULT, OFFSET_DEFAULT
from govinfo.exceptions import GovinfoException
from govinfo.models import GranuleContainer


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
