from pymongo import MongoClient
from django.conf import settings

class MongoDB:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._db is None:
            config = settings.MONGO_DB
            cls._client = MongoClient(host=config['host'], port=config['port'])
            cls._db = cls._client[config['name']]
        return cls._db

    @classmethod
    def get_collection(cls, name):
        return cls.get_db()[name]
