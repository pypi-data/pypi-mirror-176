from constants import KeyTypes
from tickerdax.config_base import ConfigBase


class Streamer(ConfigBase):
    """
    Streams data from the https://tickerdax.com websocket api to the cache using a provided config.
    """
    def __init__(self, config, client_kwargs=None):
        super(Streamer, self).__init__(config, client_kwargs)
        self.stream()

    def _validate(self):
        super(Streamer, self)._validate()
        self.client.validate_api_key(KeyTypes.WEBSOCKET)

    def stream(self):
        """
        Downloads data from the algo trading REST API base on the bot config files.
        """
        routes = self._config.get('routes', {})
        back_fill = self._config.get('back_fill', True)
        if routes:
            # unless told not to, first backwards fill the history from the start date in the config
            if back_fill:
                for route, symbols in routes.items():
                    self._logger.info(f'Back filling {route} history from "{self._start}" to "{self._now}"...')
                    self.client.get_route(
                        route=route,
                        symbols=symbols,
                        start=self._start,
                        end=self._now,
                    )

            # stream updates to the cache indefinitely
            self._logger.info(f'Starting streams...')
            self.client.stream(routes=routes)


if __name__ == '__main__':
    import os
    import logging
    logging.basicConfig(level=logging.INFO)
    Streamer(config=os.path.join(os.path.dirname(__file__), 'example_configs', 'config.yaml'))
