# meteonetwork-api-client-python

[![Coverage Status](https://coveralls.io/repos/github/dennyb87/meteonetwork-api-client-python/badge.svg)](https://coveralls.io/github/dennyb87/meteonetwork-api-client-python)

Simple python client for [meteonetwork.it](https://www.meteonetwork.it/supporto/meteonetwork-api/) api (see [api documentation](https://api.meteonetwork.it/documentation.html)).  

### Basic usage  

```
token = MeteoNetworkClient.fetch_token(
    email="mylovely@email.com",
    password="my_lovely_password",
)

client = MeteoNetworkClient(access_token=token)
client.real_time_data(station_code="tsc069")
```
