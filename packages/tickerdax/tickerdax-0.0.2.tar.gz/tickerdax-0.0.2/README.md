# TickerDax Python Client
A python package that interfaces with the tickerdax.com REST and websockets API. It handles common data operations
like batch downloading data, streaming real-time data, and caching data locally to minimize network requests.

## Installation
You can install this package with pip by running the command below.
```shell
pip install tickerdax
```

## Docker Dependency
This client interfaces with a redis docker container. In order for the package to work, you must first install
docker. Here are instructions per platform.
### Mac
[Instructions](https://docs.docker.com/desktop/install/mac-install/)
### Linux
[Instructions](https://docs.docker.com/desktop/install/linux-install/)
### Windows
Note on windows you must first install [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) then you can install docker.
[Instructions](https://docs.docker.com/desktop/install/windows-install/)

## Python Example
Here is a basic example of getting data using the python SDK.
```python
from pprint import pprint
from datetime import datetime, timezone
from tickerdax.client import TickerDax

client = TickerDax()
pprint(client.get_route(
    route='/order-book/binance',
    symbols=["BTC"],
    start=datetime.now(tz=timezone.utc),
    end=datetime.now(tz=timezone.utc)
))
```
Note that if this data doesn't exist in your cache, the data will be fetched from the REST API. All 
subsequent calls to the same data will only be from the cache and not the REST API.
This is designed give you lighting fast responses and ultimately deliver data to you a cheaper cost.

## CLI
The package also has a command line interface.
```text
Usage: tickerdax [OPTIONS] COMMAND [ARGS]...                                
                                                                            
  TickerDax version 0.0.1. A CLI tool that interfaces with the tickerdax.com
  REST and websockets API. It handles common data operations like batch     
  downloading, streaming, and caching data locally to minimize network      
  requests.                                                                 
                                                                            
Options:                                                                    
  --help  Show this message and exit.

Commands:
  create-config
  download
  list-routes
  stream
```