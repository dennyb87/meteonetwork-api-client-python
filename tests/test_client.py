import json
import unittest
from copy import deepcopy

import responses

from src.meteonetwork_api.client import MeteoNetworkClient
from tests.sample_responses import DATA_REALTIME


class MeteoNetworkClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_station = "dummy_station"
        self.token = "32166|e211RHqWVAWc6CudMlf6dQuyyGTWf1S6tUYyOLyb"
        self.successful_token_response = json.dumps(
            {
                "status_code": 200,
                "access_token": self.token,
                "token_type": "Bearer",
                "message": "The token will never expires. Save it because you can generate a new one in 1 hour.",
            }
        )
        self.data_realtime = deepcopy(DATA_REALTIME)
        self.successful_data_realtime_response = json.dumps(self.data_realtime)

    def test_from_credentials_factory(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.POST,
                f"{MeteoNetworkClient.api_root}/login",
                body=self.successful_token_response,
                status=200,
            )
            client = MeteoNetworkClient.from_credentials(
                email="dummy@email.com", password="dummy_password"
            )

        self.assertIsInstance(client, MeteoNetworkClient)
        self.assertEqual(client.access_token, self.token)

    def test_real_time(self):
        client = MeteoNetworkClient(access_token=self.token)
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                f"{MeteoNetworkClient.api_root}/data-realtime/{self.dummy_station}/",
                body=self.successful_data_realtime_response,
                status=200,
            )
            data = client.real_time(station_code=self.dummy_station)

        self.assertEqual(data, self.data_realtime)

    def test_response_not_okay(self):
        client = MeteoNetworkClient(access_token=self.token)
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                f"{MeteoNetworkClient.api_root}/data-realtime/{self.dummy_station}/",
                status=500,
            )
            with self.assertRaises(MeteoNetworkClient.InvalidResponse):
                client.real_time(station_code=self.dummy_station)
