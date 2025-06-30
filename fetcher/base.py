import logging

logger = logging.getLogger(__name__)

class Fetcher:
    def __init__(self, *args, **kwargs):
        try:
            self._init(*args, **kwargs)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.__init__ failed: {e}")
            raise

    def fetch(self, *args, **kwargs):
        try:
            return self._fetch(*args, **kwargs)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.fetch failed: {e}")
            raise

    def _init(self, *args, **kwargs):
        raise NotImplementedError("子类必须实现 _init 方法")

    def _fetch(self, *args, **kwargs):
        raise NotImplementedError("子类必须实现 _fetch 方法")