from govinfo.collections import CollectionsMixin
from govinfo.packages import PackagesMixin
from govinfo.config import BASE_URL
from govinfo.exceptions import GovinfoException
from govinfo.models import Result

import httpx
from json import JSONDecodeError


class Govinfo(CollectionsMixin, PackagesMixin):
    def __init__(self, api_key: str = "DEMO_KEY"):
        self._url = f"{BASE_URL}"
        self._api_key = api_key

    def _get(self, endpoint: str, params: dict = None) -> Result:
        url = f"{self.url}/{endpoint}"
        headers = {"x-api-key": self._api_key}
        try:
            response = httpx.get(url=url, headers=headers, params=params)
        except httpx.exceptions.RequestException as e:
            raise GovinfoException("Request failed") from e
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

    @property
    def url(self):
        return self._url
