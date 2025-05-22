from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Result:
    def __init__(self, status_code: int, message: str = "", data: dict = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else {}


class GovinfoModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
