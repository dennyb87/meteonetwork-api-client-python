# meteonetwork-api-client-python
Simple python client for [meteonetwork.it](https://www.meteonetwork.it/supporto/meteonetwork-api/) api (see [api documentation](https://api.meteonetwork.it/documentation.html)).  

### Bootstrap with credentials
```
client = MeteoNetworkClient.from_credentials(email="mylovely@email.com", password="my_lovely_password")
```

Access token will be accessible via `client.access_token` such that subesquent instantiations can be performed with:
```
client = MeteoNetworkClient(access_token=token)
client.real_time(station_code="tsc069")
```
