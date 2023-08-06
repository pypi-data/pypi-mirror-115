from datetime import timedelta
from typing import Callable

from loguru import logger

from rapdevpy.file_cache import FileCache

log_message = "what={object}, why={reason}, how={action}"


class ApiFileCache:
    def __init__(self, cache_path):
        self.cache = FileCache(cache_path)

    def get_data(self, api_function: Callable, expire_timedelta: timedelta, *args, **kwargs):
        """
        get_data(example_function, timedelta(minutes=30), example_id, page=1)
        """
        return self.get_response(api_function, expire_timedelta, *args, **kwargs)["data"]

    def get_response(self, api_function: Callable, expire_timedelta: timedelta, *args, **kwargs):
        key = self.form_key(api_function, *args, **kwargs)
        if self.cache.is_exists(key):
            response = self.get_from_etag(api_function, expire_timedelta, *args, **kwargs)
        else:
            response = self.get_from_cache(api_function, expire_timedelta, *args, **kwargs)
        logger.info(log_message, object=str(response["status"]) + ", " + str(self.extract_etag(response)),
                    reason="Inspection", action="Get response")

        return response

    def get_from_etag(self, api_function: Callable, expire_timedelta: timedelta, *args, **kwargs):
        key = self.form_key(api_function, *args, **kwargs)
        logger.info(log_message, object=key, reason="Cache hit", action="Access cache")
        response = self.cache.get(key)
        etag = self.extract_etag(response)
        try:
            response = api_function(*args, if_none_match=etag, **kwargs)
            self.cache.set(key, response, expire_timedelta)
            logger.info(log_message, object=str(key) + ", " + etag, reason="ETag expired", action="Etag check")
        except Exception as e:
            logger.error(log_message, object=str(e) + ", " + str(api_function) + ", " + str(args) + ", " + str(kwargs), reason="Exception while executing api, args and kwargs", action="Invoked API function")

        return response

    def extract_etag(self, response: dict):
        try:
            return response["headers"]["ETag"].split('"')[1]
        except KeyError as e:
            logger.error(log_message, object=str(response), reason="Cached response has no ETag", action="Extract ETag")
            return "neutral-etag"

    def get_from_cache(self, api_function: Callable, expire_timedelta: timedelta, *args, **kwargs):
        key = self.form_key(api_function, *args, **kwargs)
        logger.info(log_message, object=key, reason="Cache miss", action="Access cache")
        response = api_function(*args, **kwargs)
        self.cache.set(key, response, expire_timedelta)
        return response

    def form_key(self, api_function: Callable, *args, **kwargs):
        return api_function.__name__, args, kwargs
