from db.base import Cache, Storage


class Service:
    def __init__(self, cache: Cache, storage: Storage):
        self.cache = cache
        self.storage = storage
