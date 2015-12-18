# jeapipy
Helper to connect to the JEVis REST-API

Provides wrappers for JEVis3 Webservice requests

## Dependencies
- Python2 or Python3
- requests

## Usage
A simple example is implemented in [example.py]( example.py )

First imort `JEVisConnector`
```
from jeapipy.jeapi import JEVisConnector
```

Configure the connection. The serverpath must be the full path to the REST-service.
```
server = "http://localhost:8080/JEWebService/v1"
user = "Sys Admin"
password = "jevis"

con = JEVisConnector(server, user, password)
```

Check if the credentials were correct and the connection was established successfully
```
if not con.isConnected():
  print("Error: could not connect to server")
  exit(1)
```
