import uuid

from typing import Dict
from dataclasses import dataclass, field
from models.model import Model


@dataclass(eq=False)
class Asset(Model):
    collection: str = field(init=False, default='assets')

    type: str
    model: str
    name: str
    ip: str
    subnet: str
    floor: int
    room: str
    price: [int, float]
    status: str
    _id: int = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            'type': self.type,
            'model': self.model,
            'name': self.name,
            'ip': self.ip,
            'subnet': self.subnet,
            'floor': self.floor,
            'room': self.room,
            'price': self.price,
            'status': self.status,
            '_id': self._id
        }

    # for future use (filter)
    @classmethod
    def get_by_name(cls, device_name: str):
        return cls.find_one_by('name', device_name)

    @classmethod
    def get_by_ip(cls, device_ip: str):
        return cls.find_one_by('ip', device_ip)
