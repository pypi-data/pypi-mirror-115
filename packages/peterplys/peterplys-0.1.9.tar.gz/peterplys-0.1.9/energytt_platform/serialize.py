import serpyco
from abc import abstractmethod
from functools import lru_cache
from dataclasses import dataclass
from typing import Dict, Type, TypeVar, Generic, Any


@dataclass
class Serializable:
    """
    Base class for dataclasses that can be serialized and deserialized.
    Subclasses must be defined as dataclasses.
    """
    pass


# -- Interfaces --------------------------------------------------------------


TSerializable = TypeVar('TSerializable', bound=Serializable)
TSerialized = TypeVar('TSerialized')


class Serializer(Generic[TSerialized]):
    """
    An interface for serializing and deserializing dataclasses.
    """

    @abstractmethod
    def serialize(self, obj: TSerializable) -> TSerialized:
        """
        Serialize an object.
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, data: TSerialized, cls: Type[TSerializable]) -> TSerializable:
        """
        Deserialize an object.
        """
        raise NotImplementedError


# -- Serializers -------------------------------------------------------------


class SimpleSerializer(Serializer[Dict[str, Any]]):
    """
    Serialize and deserialize to and from simple Python types (dictionary).
    """
    def serialize(self, obj: TSerializable) -> Dict[str, Any]:
        """
        Serializes object to Python.
        """
        return get_serializer(obj.__class__).dump(obj)

    def deserialize(self, data: Dict[str, Any], cls: Type[TSerializable]) -> TSerializable:
        """
        Deserialize JSON data to instance of type "cls".
        """
        return get_serializer(cls).load(data)


class JsonSerializer(Serializer[bytes]):
    """
    Serialize and deserialize to and from JSON (encoded bytes).
    """
    def serialize(self, obj: TSerializable) -> bytes:
        """
        Serializes object to JSON.
        """
        return get_serializer(obj.__class__).dump_json(obj).encode()

    def deserialize(self, data: bytes, cls: Type[TSerializable]) -> TSerializable:
        """
        Deserialize JSON data to instance of type "cls".
        """
        return get_serializer(cls).load_json(data.decode('utf8'))


# -- Misc --------------------------------------------------------------------


@lru_cache
def get_serializer(cls: Type[TSerializable]) -> serpyco.Serializer:
    """
    TODO
    """
    return serpyco.Serializer(cls)


# -- Singletons --------------------------------------------------------------


json_serializer = JsonSerializer()
simple_serializer = SimpleSerializer()
