from .config import BASE_URL
from .exceptions import GovinfoException
from .models import Result, CollectionContainer, CollectionSummary
import httpx
from json import JSONDecodeError


class Govinfo:
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

    def collections(
        self,
        collection: str = None,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ):
        endpoint_parts = ["collections", collection, start_date, end_date]
        endpoint = "/".join(part for part in endpoint_parts if part is not None)
        page_size = kwargs.get("pageSize", 20)
        offset_mark = kwargs.get("offsetMark", "*")
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

    @property
    def url(self):
        return self._url
