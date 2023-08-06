
from .stream_base import StreamBase
import re

from typing import Generator, Iterable


class Stream(StreamBase):
    """
    Stream is sa class which help manipulate the collection and lazily evaluate results with defined generators as filters, maps and fmaps.
    """

    """Regex for detect int and float string-type numbers."""
    REGEX_DIGITS = re.compile(r'^\d+\.{0,1}\d*$')
    REGEX_DIGITS_BYTES = re.compile(rb'^\d+\.{0,1}\d*$')

    def __init__(self, value):
        super().__init__(value)

    def _get_inner_items(self) -> Iterable:
        """
        Get items from iterable_object which is type of list.
        """
        return self.iterable_object

    def filter(self, func: Generator) -> object:
        self.add((i for i in self.get_last_gen() if func(i)))
        return self

    def map(self, func: Generator) -> object:
        self.add((func(i) for i in self.get_last_gen()))
        return self

    def to_dict(self) -> dict:
        raise NotImplementedError("Method is not implemented for Stream. Use Dictstream instead.")

    def to_list(self) -> list:
        return [e for e in self.get_last_gen()]

    def reverse(self) -> list:
        return reversed(self.to_list())

    def joining(self, delimiter: str) -> str:
        """
        Return sting from the Stream. Connect all data with delimiter.

        :param delimiter: string, delimiter.
        :return: String
        """
        return delimiter.join(self.get_last_gen())

    def count(self) -> int:
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :return: int, amount of elements.
        """
        return sum(1 for _ in self.get_last_gen())

    def any_match(self, func: Generator) -> bool:
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :param func: anonymous function (lambda) or regular. Generator.
        :return: True if any found, otherwise False.
        """
        return any(func(i) for i in self.get_last_gen())

    def all_match(self, func: Generator) -> bool:
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :param func: anonymous function (lambda) or regular. Generator.
        :return: True if all found, otherwise False.
        """
        return all(func(i) for i in self.get_last_gen())

    def sum(self) -> int:
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :return: int, sum of elements. If elements are not only int/float type, exception will occur.
        """
        return sum(self.get_last_gen())

    def max(self) -> int:
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :return: int, max value from elements.
        """
        return max(self.get_last_gen())

    def min(self) -> int:
        """
        Method evaluates generators. Stream cannot be reused after this method.

        :return: int, min value from elements.
        """
        return min(self.get_last_gen())

    def map_to_str(self) -> object:
        """
        Helper method, include map-generator to change elements types to String.
        """
        return self.map(lambda x: str(x))

    def map_to_int(self) -> object:
        """
        Helper method, include map-generator to change elements types to int.
        """
        return self.map(lambda x: int(x))

    def map_to_float(self) -> object:
        """
        Helper method, include map-generator to change elements types to float.
        """
        return self.map(lambda x: float(x))

    def only_dict(self) -> object:
        """
        Helper method, include filter-generator for elements which are dicts.
        """
        return self.filter(lambda x: isinstance(x, dict))

    def only_list(self) -> object:
        """
        Helper method, include filter-generator for elements which are lists, tuples or sets.
        """
        return self.filter(lambda x: isinstance(x, (list, set, tuple)))

    def only_digits(self) -> object:
        """
        Helper method, include filter-generator for elements which are digits.
        """
        return self.filter(
            lambda x: isinstance(x, (int, float)) or
                      (isinstance(x, str) and self.REGEX_DIGITS.match(x)) or
                      (isinstance(x, bytes) and self.REGEX_DIGITS_BYTES.match(x))
        )

    def no_none(self) -> object:
        """
        Helper method, include filter-generator for not None elements.
        """
        return self.filter(lambda x: x is not None)

    def no_list(self) -> object:
        """
        Helper method, include filter-generator for elements which are not list, tuple or set type.
        """
        return self.filter(lambda x: not isinstance(x, (list, set, tuple)))

    def exists(self) -> object:
        """
        Helper method, include filter-generator and check if element exists (are not empty, like empty list, None or empty String).
        """
        return self.filter(lambda x: x)

    def even(self) -> object:
        """
        Helper method, include filter-generator for even elements.
        """
        return self.filter(lambda x: x%2 == 0)

    def odd(self) -> object:
        """
        Helper method, include filter-generator for odd elements.
        """
        return self.filter(lambda x: (x%2 - 1) == 0)

    def gt(self, value: int) -> object:
        """
        Helper method, include filter-generator for number-type elements which are greater than value.
        """
        return self.filter(lambda x: x > value)

    def lt(self, value: int) -> object:
        """
        Helper method, include filter-generator for number-type elements which are lower than value.
        """
        return self.filter(lambda x: x < value)

    def ge(self, value: int) -> object:
        """
        Helper method, include filter-generator for number-type elements which are greater and equal value.
        """
        return self.filter(lambda x: x >= value)

    def le(self, value: int) -> object:
        """
        Helper method, include filter-generator for number-type elements which are less and equal value.
        """
        return self.filter(lambda x: x <= value)

    def eq(self, value: object) -> object:
        """
        Helper method, include filter-generator for number-type elements which are equal value.
        """
        return self.filter(lambda x: x == value)
