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

    def granules(self, package_id: str, **kwargs) -> list[dict]:
        """Call the packages/{package_id}/granules endpoint of the GovInfo API."""
        args = self._build_granules_request(package_id, **kwargs)

        try:
            for item in self._get("granules", args):
                yield Granule(**item).model_dump()
        except GovInfoException as e:
            raise e
