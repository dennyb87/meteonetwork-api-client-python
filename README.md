# meteonetwork-api-client-python
Simple python client for meteonetwork api.  

### Bootstrap with credentials
```
client = MeteoNetworkClient.from_login(email="mylovely@email.com", password="my_levely_password")
```

Access token will be accessible via `client.access_token` such that subesquent instantiations can be performed with:
```
client = MeteoNetworkClient(access_token=token)
client.real_time(station_code="tsc069")
```
