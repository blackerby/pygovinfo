from govinfo.config import RequestArgs
from govinfo.exceptions import GovInfoException
from govinfo.models import Package


class PublishedMixin:
    def _build_published_request(
        self,
        collection: str,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ) -> RequestArgs:
        endpoint_parts = ["published", start_date, end_date]
        path = "/".join(part for part in endpoint_parts if part is not None)
        params = self._set_params(**kwargs)
        params["collection"] = collection
        return (path, params)

    def published(
        self,
        collection: str,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ):
        """Call the published endpoint of the GovInfo API."""
        args = self._build_published_request(collection, start_date, end_date, **kwargs)

        try:
            for item in self._get("published", args):
                yield Package(**item).model_dump()
        except GovInfoException as e:
            raise e
