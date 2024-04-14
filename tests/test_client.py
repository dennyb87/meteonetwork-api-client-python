import json
import unittest
from copy import deepcopy
from unittest import mock

import responses
from requests.exceptions import HTTPError

from src.meteonetwork_api.client import MeteoNetworkClient
from tests.sample_responses import (
    DAILY_DATA,
    INTERPOLATED_REAL_TIME_DATA,
    REAL_TIME_DATA,
    STATION_DATA,
)


class MeteoNetworkClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_station = "dummy_station"
        self.token = "32166|e211RHqWVAWc6CudMlf6dQuyyGTWf1S6tUYyOLyb"
        self.token_body = json.dumps(
            {
                "status_code": 200,
                "access_token": self.token,
                "token_type": "Bearer",
                "message": "The token will never expires. Save it because you can generate a new one in 1 hour.",
            }
        )
        self.real_time_data = deepcopy(REAL_TIME_DATA)
        self.daily_data = deepcopy(DAILY_DATA)
        self.station_data = deepcopy(STATION_DATA)
        self.interpolated_real_time_data = deepcopy(INTERPOLATED_REAL_TIME_DATA)
        self.real_time_data_body = json.dumps(self.real_time_data)
        self.daily_data_body = json.dumps(self.daily_data)
        self.station_body = json.dumps(self.station_data)
        self.interpolated_real_time_data_body = json.dumps(
            self.interpolated_real_time_data
        )

    def test_fetch_token(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.POST,
                f"{MeteoNetworkClient.api_root}/login",
                body=self.token_body,
                status=200,
            )
            token = MeteoNetworkClient.fetch_token(
                email="dummy@email.com", password="dummy_password"
            )

        self.assertEqual(token, self.token)

    @mock.patch.object(MeteoNetworkClient, "fetch_token")
    def test_from_credentials_factory(self, fetch_token_mock):
        fetch_token_mock.return_value = self.token
        client = MeteoNetworkClient.from_credentials(
            email="dummy@email.com", password="dummy_password"
        )
        self.assertIsInstance(client, MeteoNetworkClient)
        self.assertEqual(client.access_token, self.token)

    def test_real_time_data(self):
        client = MeteoNetworkClient(access_token=self.token)
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                f"{MeteoNetworkClient.api_root}/data-realtime/{self.dummy_station}/",
                body=self.real_time_data_body,
                status=200,
            )
            data = client.real_time_data(station_code=self.dummy_station)

        self.assertEqual(data, self.real_time_data)

    def test_response_not_okay(self):
        client = MeteoNetworkClient(access_token=self.token)
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                f"{MeteoNetworkClient.api_root}/data-realtime/{self.dummy_station}/",
                status=500,
            )
            with self.assertRaises(HTTPError):
                client.real_time_data(station_code=self.dummy_station)

    def test_daily_data(self):
        client = MeteoNetworkClient(access_token=self.token)
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                f"{MeteoNetworkClient.api_root}/data-daily/{self.dummy_station}/",
                body=self.daily_data_body,
                status=200,
            )
            data = client.daily_data(
                station_code=self.dummy_station, observation_date="2024-04-10"
            )

        self.assertEqual(data, self.daily_data)

    def test_station(self):
        client = MeteoNetworkClient(access_token=self.token)
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                f"{MeteoNetworkClient.api_root}/stations/{self.dummy_station}/",
                body=self.station_body,
                status=200,
            )
            data = client.station(station_code=self.dummy_station)

        self.assertEqual(data, self.station_data)

    def test_interpolated_real_time_data(self):
        client = MeteoNetworkClient(access_token=self.token)
        lat, lon = "45.5", "9.3"
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                f"{MeteoNetworkClient.api_root}/interpolated-realtime/?lat={lat}&lon={lon}",
                body=self.interpolated_real_time_data_body,
                status=200,
            )
            data = client.interpolated_real_time_data(lat=lat, lon=lon)

        self.assertEqual(data, self.interpolated_real_time_data)
