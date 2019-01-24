import json
from os.path import realpath, join, dirname

import logging
logger = logging.getLogger("crd")


class ConfigurationManager(object):
    """
    Configuration manager
    In charge of persisting user configuration via local cache
    """

    CACHE_FILE_DEFAULT = join(dirname(dirname(realpath(__file__))), "config.json")

    def __init__(self, cache_file: str = CACHE_FILE_DEFAULT):
        logger.info("Using the following path for config cache: %s" % cache_file)
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

