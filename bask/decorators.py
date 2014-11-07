def cache(func):
    url_cache = {}

    def wrapper(klass, key):
        url = url_cache.get(key)
        if not url:
            url = func(klass, key)
            url_cache[key] = url

        return url
    return wrapper
