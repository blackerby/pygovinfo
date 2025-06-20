from govinfo.config import RequestArgs
from govinfo.exceptions import GovinfoException


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
            result = self._get(args)
        except GovinfoException as e:
            raise e

        return result.data
