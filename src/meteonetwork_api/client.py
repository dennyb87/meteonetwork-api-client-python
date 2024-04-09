from enum import Enum

import requests


class HttpMethod(str, Enum):
    POST = "post"
    GET = "get"


class MeteoNetworkClient:
    api_root = "https://api.meteonetwork.it/v3"
    
    class InvalidResponse(Exception):
        pass

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    @classmethod
    def _request(cls, url: str, method: HttpMethod, **kwargs) -> dict:
        request_method = getattr(requests, method)
        response = request_method(url=url, **kwargs)
        if not response.ok:
            raise cls.InvalidResponse(f"{response.status_code}: {response.content}")
        return response.json()

    @classmethod
    def from_credentials(cls, email: str, password: str) -> "MeteoNetworkV3Client":
        login_endpoint = f"{cls.api_root}/login"
        data = {"email": email, "password": password}
        json_data = cls._request(url=login_endpoint, method=HttpMethod.POST, data=data)
        return cls(access_token=json_data["access_token"])

    def real_time(self, station_code: str) -> dict:
        real_time_endpoint = f"{self.api_root}/data-realtime/{station_code}/"
        return self._request(url=real_time_endpoint, method=HttpMethod.GET, headers=self.headers)