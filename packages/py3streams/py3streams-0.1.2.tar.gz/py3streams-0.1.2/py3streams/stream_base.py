from abc import ABC, abstractmethod
from .optional import Optional

from typing import Iterable, Generator, Any, List


class StreamBase(ABC):
    """
    Abstract Stream class. Base of other Stream classes.
    """

    def __init__(self, iterable_object: Iterable):
        self.iterable_object = iterable_object
        self._generators = []

    def get_last_gen(self) -> Any:
        """
        Get last saved generator from generators chain. If there is no registered generators, return stored collection.
        """
        return self._generators[-1] if len(self._generators) > 0 else (self.iterable_object.items() if isinstance(self.iterable_object, dict) else self.iterable_object)

    def add(self, generator: Generator) -> None:
        """
        Add new generator to the Stream generator container for future lazy evaluation.
        """
        self._generators.append(generator)

    def get_first(self) -> Optional:
        """
        Evaluate stored _generators and try find first existing element. After evaluation Stream is empty, and cannot be reused.
        Stored _generators may produce result, but if not it will return None. Result from generator is stored in Optional container object.

        :return: Optional container object with result. Result is an defined object which is found from _generators.
        """
        return Optional.of(next(self.__iter__(), None))

    def __iter__(self):
        yield from self.get_last_gen()

    def operations(self) -> List:
        """
        Method for debugging for check stored _generators.

        :return: list of stored _generators.
        """
        return self._generators

    def fmap(self, func: Any) -> object:
        """
        This specific method allow iterate over nested lists and dicts(!) inside collection.
        It works only with 1 nested-level. In case of sub-sub list, repeat fmap.

        In case of many dicts in collection, fmap allow iterate over key-value from dicts. Stream is not a dict,
        it does not care if more than 1 dict may have same key-value pairs. It will just iterate.
        Example: [{id:1, value: "John"}, {id:2, value: "John"}].
        Fmap with DictStream will iterate over key-value from first dict, and then continue with next.

        fmap method uses abstract method _get_inner_items().
        It's important because different iterator is executed in case of Stream or DictStream.
        """
        # noinspection PyProtectedMember
        def _wrap(streams):
            for s in streams:
                yield from s._get_inner_items()

        self.add(_wrap((func(i) for i in self.get_last_gen())))
        return self

    def limit(self, limit: int) -> object:
        """
        Method with limit for generators. During evaluation Stream will try find only limited amount of results.

        :param limit: int, the limit for Stream.
        :return: Stream object.
        """
        def _wrap(iterator):
            for i, e in enumerate(iterator):
                if i < limit:
                    yield e
                else:
                    break
        self.add(_wrap(self.get_last_gen()))
        return self

    @abstractmethod
    def _get_inner_items(self) -> Any:
        """
        Abstract method usable in fmap() evaluation. Method have to be implemented in DictStream or Stream with their logic.
        """

    @abstractmethod
    def filter(self, func: Any):
        """
        Add func as a filter-generator to the stored generators and connect it to already stored generators.

        :param func: anonymous function (lambda) or regular function.
        :return: Stream object.
        """

    @abstractmethod
    def map(self, func):
        """
        Add func as a map-generator to the stored generators and connect it to already stored generators.

        :param func: anonymous function (lambda) or regular function.
        :return: Stream object.
        """

    @abstractmethod
    def to_list(self):
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :return: List of items after Stream evaluation.
        """

    @abstractmethod
    def to_dict(self):
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :return: Dict of items after Stream evaluation.
        """

    @abstractmethod
    def reverse(self):
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :return: List of elements with reversed order.
        """
