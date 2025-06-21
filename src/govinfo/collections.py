from govinfo.config import RequestArgs
from govinfo.exceptions import GovInfoException


class CollectionsMixin:
    def _build_collections_request(
        self,
        collection: str = None,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ) -> RequestArgs:
        endpoint_parts = ["collections", collection, start_date, end_date]
        path = "/".join(part for part in endpoint_parts if part is not None)
        params = self._set_params(**kwargs)
        return (path, params)

    def collections(
        self,
        collection: str = None,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ) -> list[dict]:
        """Call the collections endpoint of the GovInfo API."""
        args = self._build_collections_request(
            collection, start_date, end_date, **kwargs
        )

        try:
            result = self._get("collections", args)
        except GovInfoException as e:
            raise e

        return result.data
