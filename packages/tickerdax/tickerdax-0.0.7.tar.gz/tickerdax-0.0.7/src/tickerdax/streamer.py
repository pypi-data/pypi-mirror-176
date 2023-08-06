from tickerdax.constants import KeyTypes
from tickerdax.config_base import ConfigBase
from tickerdax.client import TickerDax
from tickerdax.downloader import Downloader


class Streamer(ConfigBase):
    """
    Streams data from the https://tickerdax.com websocket api to the cache using a provided config.
    """
    def __init__(self, config, client_kwargs=None):
        # this avoids connecting to the client initially incase the Downloader needs to connect as well
        client_kwargs['connect'] = False
        super(Streamer, self).__init__(config, client_kwargs)

        # unless told not to, first backwards fill the history from the start date in the config
        self._back_fill = self._config.get('back_fill', True)

        # if were are not going to use the Downloader, then we need to set the connection
        if not self._back_fill:
            client_kwargs['connect'] = True
            self.client = TickerDax(client_kwargs)

        self.stream()

    def _validate(self):
        super(Streamer, self)._validate()
        self.client.validate_api_key(KeyTypes.WEBSOCKET)

    def stream(self):
        """
        Downloads data from the algo trading REST API base on the bot config files.
        """
        routes = self._config.get('routes', {})

        if routes:
            if self._back_fill:
                Downloader(config=self._config_file_path, till_now=True)

            # stream updates to the cache indefinitely
            self._logger.info(f'Starting streams...')
            self.client.stream(routes=routes)


if __name__ == '__main__':
    import os
    import logging
    logging.basicConfig(level=logging.INFO)
    Streamer(config=os.path.join(os.path.dirname(__file__), 'example_configs', 'config.yaml'))
