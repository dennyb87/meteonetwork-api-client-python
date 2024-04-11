from enum import Enum, unique


@unique
class HttpMethod(str, Enum):
    POST = "post"
    GET = "get"
