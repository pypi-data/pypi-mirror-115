from typing import Any, NamedTuple
from ujenkins.exceptions import JenkinsError as JenkinsError

class Response(NamedTuple):
    status: Any
    headers: Any
    body: Any

class Jenkins:
    def __init__(self) -> None: ...
