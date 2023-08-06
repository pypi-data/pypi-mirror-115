
from .stream_base import StreamBase
from .stream import Stream

from typing import Any, Iterator, Generator, List, Dict


class DictStream(StreamBase):
    """
    DictStream object which can evalulate dictionary. Usage of this class is rare, it is usable during fmap() process.
    In case when dictionaries are stored in list, recommended process is to use Stream class.
    """

    def __init__(self, value: dict):
        super().__init__(value)

    def _get_inner_items(self) -> Any:
        """
        Method returns items from iterable_object which is type of Dict.
        """
        return self.iterable_object.items()

    def filter(self, func: Generator) -> Any:
        self.add(((k, v) for k, v in self.get_last_gen() if func(k, v)))
        return self

    def map(self, func: Generator) -> Any:
        self.add((func(k, v) for k, v in self.get_last_gen()))
        return self

    def to_list(self) -> List:
        return list(self.get_last_gen())

    def to_dict(self) -> Dict:
        return {k:v for k,v in self.get_last_gen()}

    def items(self) -> Iterator:
        """
        Wrapper for DictStream based on dict.items().

        :return: Iterator of stored elements.
        """
        return self.__iter__()

    def values(self) -> Stream:
        """
        :return: Stream object of values from DictStream.
        """
        return Stream((v for _, v in self.get_last_gen()))

    def keys(self) -> Stream:
        """
        :return: Stream object of keys from DictStream.
        """
        return Stream((k for k, _ in self.get_last_gen()))

    def reverse(self):
        raise NotImplementedError("Method is not implemented in DictStream.")
