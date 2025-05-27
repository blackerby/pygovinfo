from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


@dataclass
class Result:
    status_code: int
    message: str = ""
    data: dict = {}


class GovinfoModel(BaseModel):
    # TODO: move shared attributes into this model,
    # e.g., dateIssued, packageId, collectionCode, collectionName, docClass, category?
    # download?, last_modified, title?
    model_config = ConfigDict(alias_generator=to_camel)


# NOTE: response objects from `related` endpoints and `packages` summary endpoints are similarly vague
