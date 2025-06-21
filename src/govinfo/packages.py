from govinfo.config import RequestArgs
from govinfo.exceptions import GovInfoException
from govinfo.models import Granule


class PackagesMixin:
    def _build_granules_request(
        self,
        package_id: str,
        **kwargs,
    ) -> RequestArgs:
        path = f"packages/{package_id}/granules"
        params = self._set_params(**kwargs)
        return (path, params)

    def granules(self, package_id: str, **kwargs):
        """Call the packages/{package_id}/granules endpoint of the GovInfo API."""
        args = self._build_granules_request(package_id, **kwargs)

        try:
            for item in self._get("granules", args):
                yield Granule(**item).model_dump()
        except GovInfoException as e:
            raise e

    def summary(self, package_id: str, granule_id: str | None = None, **kwargs):
        path = (
            f"packages/{package_id}/granules/{granule_id}/summary"
            if granule_id
            else f"packages/{package_id}/summary"
        )
        params = self._set_params(**kwargs)
        try:
            for item in self._get(
                endpoint=None,
                args=(
                    path,
                    params,
                ),
            ):
                return item
        except GovInfoException as e:
            raise e
