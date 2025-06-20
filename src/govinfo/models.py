from dataclasses import dataclass, field


@dataclass
class Result:
    status_code: int
    message: str = ""
    data: dict = field(default_factory=dict)


# NOTE: response objects from `related` endpoints and `packages` summary endpoints are similarly vague
