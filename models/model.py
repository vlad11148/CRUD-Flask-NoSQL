from abc import ABCMeta, abstractmethod
from typing import List, Dict

from common.database import Database


class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_by_id(cls, _id: str):
        return cls.find_one_by('_id', _id)

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def all(cls) -> List:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls, attribute: str, value):
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls, attribute: str, value: str):
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]

    def save_to_mongo(self):
        Database.update(self.collection, {'_id': self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {'_id': self._id})
