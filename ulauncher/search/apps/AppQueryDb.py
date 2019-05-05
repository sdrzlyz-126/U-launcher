import os
from ulauncher.config import CACHE_DIR
from ulauncher.utils.db.KeyValueDb import KeyValueDb
from ulauncher.utils.decorator.singleton import singleton


class AppQueryDb(KeyValueDb):

    @classmethod
    @singleton
    def get_instance(cls):
        db = cls(os.path.join(CACHE_DIR, 'app_queries_v3.db'))
        db.open()
        return db
