from .config import BASE_URL
from .exceptions import GovinfoException
from .models import Result
import httpx
from json import JSONDecodeError
import logging


class Govinfo:
    def __init__(self, api_key: str = "DEMO_KEY", logger: logging.Logger = None):
        self._url = f"{BASE_URL}"
        self._api_key = api_key
        self._logger = logger or logging.getLogger(__name__)

    def get(self, endpoint: str, params: dict = None) -> Result:
        url = f"{self.url}/{endpoint}"
        headers = {"x-api-key": self._api_key}
        log_line_pre = f"url={url}, params={params}"
        log_line_post = ", ".join(
            (log_line_pre, "success={}, status_code={}, message={}")
        )
        try:
            self._logger.debug(msg=log_line_pre)
            response = httpx.get(url=url, headers=headers, params=params)
        except httpx.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise GovinfoException("Request failed") from e
        try:
            data = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise GovinfoException("Bad JSON in response") from e
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason_phrase
        )
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(
                response.status_code, message=response.reason_phrase, data=data
            )
        self._logger.error(msg=log_line)
        raise GovinfoException(f"{response.status_code}: {response.reason_phrase}")

    @property
    def url(self):
        return self._url
