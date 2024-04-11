from urllib.parse import urlencode

import requests

from src.meteonetwork_api.constants import HttpMethod


class MeteoNetworkClient:
    api_root = "https://api.meteonetwork.it/v3"

    class InvalidResponse(Exception):
        pass

    def __init__(self, access_token) -> None:
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
    def fetch_token(cls, email: str, password: str) -> str:
        endpoint = f"{cls.api_root}/login"
        data = {"email": email, "password": password}
        json_data = cls._request(url=endpoint, method=HttpMethod.POST, data=data)
        return json_data["access_token"]

    @classmethod
    def from_credentials(cls, email: str, password: str) -> "MeteoNetworkV3Client":
        access_token = cls.fetch_token(email=email, password=password)
        return cls(access_token=access_token)

    def real_time_data(self, station_code: str) -> dict:
        endpoint = f"{self.api_root}/data-realtime/{station_code}/"
        return self._request(url=endpoint, method=HttpMethod.GET, headers=self.headers)

    def daily_data(self, station_code: str, observation_date: str) -> dict:
        endpoint = f"{self.api_root}/data-daily/{station_code}/"
        return self._request(url=endpoint, method=HttpMethod.GET, headers=self.headers)

    def station(self, station_code: str) -> dict:
        endpoint = f"{self.api_root}/stations/{station_code}/"
        return self._request(url=endpoint, method=HttpMethod.GET, headers=self.headers)

    def interpolated_real_time_data(self, lat: str, lon: str) -> dict:
        query = urlencode(dict(lat=lat, lon=lon))
        endpoint = f"{self.api_root}/interpolated-realtime/?{query}"
        return self._request(url=endpoint, method=HttpMethod.GET, headers=self.headers)
