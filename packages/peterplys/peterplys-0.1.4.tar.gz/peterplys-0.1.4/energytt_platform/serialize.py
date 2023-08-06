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
    @property
    def type_name(self) -> str:
        return self.__class__.__name__


class SerializeError(Exception):
    pass


class DeserializeError(Exception):
    pass


TSerializable = TypeVar('TSerializable', bound=Serializable)
TSerialized = TypeVar('TSerialized')


class Serializer(Generic[TSerialized]):
    """
    An interface for serializing and deserializing dataclasses.
    """

    @abstractmethod
    def serialize(self, obj: TSerializable) -> TSerialized:
        """
        Serialize an object to bytes.

        :param Serializable obj: Object to serialize
        :raise SerializeError: Raised when serialization fails
        :rtype: bytes
        :return: Byte-representation of object
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, data: TSerialized, cls: Type[TSerializable]) -> TSerializable:
        """
        Deserialize bytes to an object.

        :param bytes data: Byte-representation of object
        :param Type[Serializable] cls: Class to deserialize into
        :raise DeserializeError: Raised when deserialization fails
        :rtype: Serializable
        :return: Deserialized object
        """
        raise NotImplementedError


class SimpleSerializer(Serializer[Dict[str, Any]]):
    """
    Serialize and deserialize to and from simple Python types (dictionary).
    """
    def serialize(self, obj: TSerializable) -> Dict[str, Any]:
        """
        Serializes object to Python.
        """
        return self.get_serializer(obj.__class__).dump(obj)

    def deserialize(self, data: Dict[str, Any], cls: Type[TSerializable]) -> TSerializable:
        """
        Deserialize JSON data to instance of type "cls".
        """
        return self.get_serializer(cls).load(data)

    # -- Serializers ---------------------------------------------------------

    @lru_cache
    def get_serializer(self, cls: Type[TSerializable]) -> serpyco.Serializer:
        return self.build_serializer(cls)

    def build_serializer(self, cls: Type[TSerializable]) -> serpyco.Serializer:
        return serpyco.Serializer(cls)


class JsonSerializer(Serializer[bytes]):
    """
    Serialize and deserialize to and from JSON.
    """
    def serialize(self, obj: TSerializable) -> bytes:
        """
        Serializes object to JSON.
        """
        return self \
            .get_serializer(obj.__class__) \
            .dump_json(obj) \
            .encode()

    def deserialize(self, data: bytes, cls: Type[TSerializable]) -> TSerializable:
        """
        Deserialize JSON data to instance of type "cls".
        """
        return self \
            .get_serializer(cls) \
            .load_json(data.decode('utf8'))

    # -- Serializers ---------------------------------------------------------

    @lru_cache
    def get_serializer(self, cls: Type[TSerializable]) -> serpyco.Serializer:
        return self.build_serializer(cls)

    def build_serializer(self, cls: Type[TSerializable]) -> serpyco.Serializer:
        return serpyco.Serializer(cls)


# -- Singletons --------------------------------------------------------------

json_serializer = JsonSerializer()
simple_serializer = SimpleSerializer()
