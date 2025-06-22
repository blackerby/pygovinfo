from json import JSONDecodeError

import httpx

from govinfo.config import BASE_URL, KEYS, OFFSET_DEFAULT, PAGE_DEFAULT
from govinfo.exceptions import GovInfoException
from govinfo.models import Collection, Granule, Package


class GovInfo:
    """Wrapper class for the GovInfo API.

    Users can supply an API key or use the default value, DEMO_KEY"""

    def __init__(self, api_key: str = "DEMO_KEY"):
        self._url = f"{BASE_URL}"
        self._api_key = api_key
        self._params = {
            "offsetMark": OFFSET_DEFAULT,
            "pageSize": PAGE_DEFAULT,
        }

    def collections(
        self,
        collection: str = None,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ):
        """Call the collections endpoint of the GovInfo API."""

        try:
            return self._call_endpoint(
                endpoint="collections",
                collection=collection,
                start_date=start_date,
                end_date=end_date,
                **kwargs,
            )
        except GovInfoException as e:
            raise e

    def granules(self, package_id: str, **kwargs):
        """Call the packages/{package_id}/granules endpoint of the GovInfo API."""

        try:
            return self._call_endpoint(
                endpoint="packages", package_id=package_id, **kwargs
            )
        except GovInfoException as e:
            raise e

    def summary(self, package_id: str, granule_id: str | None = None, **kwargs):
        self._path = (
            f"packages/{package_id}/granules/{granule_id}/summary"
            if granule_id
            else f"packages/{package_id}/summary"
        )
        self._set_params(**kwargs)
        try:
            for item in self._get(endpoint=None):
                return item
        except GovInfoException as e:
            raise e

    def published(
        self,
        collection: str,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ):
        """Call the published endpoint of the GovInfo API."""

        try:
            return self._call_endpoint(
                endpoint="published",
                collection=collection,
                start_date=start_date,
                end_date=end_date,
                **kwargs,
            )
        except GovInfoException as e:
            raise e

    def _get(self, endpoint: str):
        headers = {"x-api-key": self._api_key}
        with httpx.Client(headers=headers) as client:
            response = client.get(
                "/".join([self._url, self._path]), params=self._params
            )
            try:
                payload = response.json()
            except (ValueError, JSONDecodeError) as e:
                raise GovInfoException("Bad JSON in response") from e
            is_success = 299 >= response.status_code >= 200
            if is_success:
                if endpoint is None:
                    yield payload
                else:
                    payload_key = self._set_payload_key(endpoint, self._path)
                    for item in payload[payload_key]:
                        yield item
                    while next_page := payload.get("nextPage"):
                        response = client.get(next_page)
                        payload = response.json()
                        for item in payload[payload_key]:
                            yield item
            else:
                raise GovInfoException(
                    f"{response.status_code}: {response.reason_phrase}"
                )

    def __repr__(self) -> str:
        api_key = "user supplied" if self._is_api_key_set() else self._api_key
        return f"GovInfo(url={self._url!r}, api_key={api_key!r})"

    def _is_api_key_set(self) -> bool:
        return self._api_key != "DEMO_KEY"

    def _set_path_and_params(self, **kwargs):
        match kwargs:
            case {
                "endpoint": endpoint,
                "collection": collection,
                "start_date": start_date,
                **params,
            }:
                if endpoint == "collections":
                    endpoint_parts = [endpoint, collection, start_date]
                    params = params
                elif endpoint == "published":
                    endpoint_parts = [endpoint, start_date]
                    params = params
                    params["collection"] = collection
            case {
                "endpoint": endpoint,
                "collection": collection,
                "start_date": start_date,
                "end_date": end_date,
                **params,
            }:
                if endpoint == "collections":
                    endpoint_parts = [endpoint, collection, start_date, end_date]
                    params = params
                elif endpoint == "published":
                    endpoint_parts = [endpoint, start_date, end_date]
                    params = params
                    params["collection"] = collection
            case {"endpoint": endpoint, "package_id": package_id, **params}:
                endpoint_parts = [endpoint, package_id, "granules"]
                params = params
            case {"endpoint": endpoint, **params}:
                endpoint_parts = [endpoint]
                params = params
            case _:
                raise GovInfoException

        self._path = "/".join(part for part in endpoint_parts if part is not None)
        self._set_params(**params)

    def _call_endpoint(self, **kwargs):
        self._set_path_and_params(**kwargs)

        endpoint = kwargs.get("endpoint")
        collection = kwargs.get("collection")
        match (endpoint, collection):
            case ("collections", None):
                model = Collection
            case ("collections" | "published", _):
                model = Package
            case ("packages", None):
                model = Granule

        try:
            for item in self._get(endpoint):
                yield model(**item).model_dump()
        except GovInfoException as e:
            raise e

    def _set_params(self, **params):
        self._params |= {
            key.split("_")[0]
            + "".join(word.capitalize() for word in key.split("_")[1:]): value
            for key, value in params.items()
        }

    def _set_payload_key(self, endpoint: str, path: str) -> str:
        if endpoint == "collections" and path == "collections":
            return "collections"
        return KEYS[endpoint]
