from govinfo.collections import CollectionsMixin
from govinfo.packages import PackagesMixin
from govinfo.config import BASE_URL, RequestArgs
from govinfo.exceptions import GovinfoException
from govinfo.models import Result

import httpx
from json import JSONDecodeError


class Govinfo(CollectionsMixin, PackagesMixin):
    def __init__(self, api_key: str = "DEMO_KEY"):
        self._url = f"{BASE_URL}"
        self._api_key = api_key

    def _get(self, args: RequestArgs) -> Result:
        headers = {"x-api-key": self._api_key}
        path, params = args
        with httpx.Client(base_url=self.url, headers=headers, params=params) as client:
            response = client.get(path)
            try:
                data = response.json()
            except (ValueError, JSONDecodeError) as e:
                raise GovinfoException("Bad JSON in response") from e
            is_success = 299 >= response.status_code >= 200
            if is_success:
                return Result(
                    response.status_code, message=response.reason_phrase, data=data
                )
            raise GovinfoException(f"{response.status_code}: {response.reason_phrase}")

    def __repr__(self) -> str:
        api_key = "user supplied" if self._is_api_key_set() else self._api_key
        return f"Govinfo(url={self.url!r}, api_key={api_key!r})"

    def _is_api_key_set(self) -> bool:
        return self._api_key != "DEMO_KEY"

    @property
    def url(self):
        return self._url
