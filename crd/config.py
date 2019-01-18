import json


class ConfigurationManager(object):
    """
    Configuration manager
    In charge of persisting user configuration via local cache
    """

    CACHE_FILE_DEFAULT = "config.json"

    def __init__(self, cache_file: str = CACHE_FILE_DEFAULT):
        self._cache_file = cache_file
        self.cache = {}

    def __enter__(self):
        try:
            with open(self._cache_file, 'r') as fp:
                self.cache = json.load(fp)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            with open(self._cache_file, 'w') as fp:
                json.dump(self.cache, fp)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            raise

