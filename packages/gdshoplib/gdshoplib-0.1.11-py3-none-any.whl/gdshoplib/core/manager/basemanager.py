import datetime
import functools
import requests as r


class BaseManager:
    CACHE = {}
    DESCRIPTION_TEMPLATE = "basic.txt"

    def __init__(self, cache=False, cache_period=20) -> None:
        self.cache = cache
        self.cache_period = cache_period
        self.settings = self.SETTINGS()

    @classmethod
    def get_manager_by_key(cls, key):
        for manager in cls.__subclasses__():
            if manager.KEY == key.upper():
                return manager
        assert False, f"Менеджер по ключу {key} не найден"

    def get_cache_key(self, path, **kwargs):
        return f"{path}"

    def check_cacheble(self, *args, **kwargs):
        return kwargs.get("method").upper() == "GET"

    def auth(self):
        raise NotImplementedError

    def pagination(self, url, *, params=None, **kwargs):
        raise NotImplementedError

    def pagination_next(self, response):
        raise NotImplementedError

    def cache_response(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if self.cache and self.check_cacheble(*args, **kwargs):
                cache_key = self.get_cache_key(*args, **kwargs)
                cached = self.CACHE.get(cache_key)

                if cached and cached["time"] > datetime.datetime.now():
                    cached["time"] += datetime.timedelta(seconds=self.cache_period)
                    return cached["data"]

                self.CACHE[cache_key] = {
                    "data": func(self, *args, **kwargs),
                    "time": datetime.datetime.now()
                    + datetime.timedelta(seconds=self.cache_period),
                }

                return self.CACHE[cache_key]["data"]
            return func(self, *args, **kwargs)

        return wrap

    @cache_response
    def make_request(self, path, *, method, params=None):
        _path = f"{self.BASE_URL}{path}"
        _r = r.request(
            method,
            _path,
            headers=self.get_headers(),
            **dict(
                (dict(params=params) or {})
                if method == "GET"
                else (dict(json=params) or {})
            ),
        )
        assert (
            _r.ok
        ), f"Запрос {method.upper()} {_path} прошел с ошибкой {_r.status_code}"
        return _r
