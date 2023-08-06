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
docker.
### Mac
[Instructions](https://docs.docker.com/desktop/install/mac-install/)
### Linux
[Instructions](https://docs.docker.com/desktop/install/linux-install/)
### Windows
Note on windows you must first install [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) then you can install docker.
[Instructions](https://docs.docker.com/desktop/install/windows-install/)

## Usage
Here is a basic example of getting data from the REST API.
```python
import pytz
from pprint import pprint
from datetime import datetime
from tickerdax import TickerDax

client = TickerDax()
pprint(client.get_into_the_block_predictions(
    symbols=["BTC"],
    start=datetime.now(tz=pytz.UTC),
    end=datetime.now(tz=pytz.UTC)
))
```