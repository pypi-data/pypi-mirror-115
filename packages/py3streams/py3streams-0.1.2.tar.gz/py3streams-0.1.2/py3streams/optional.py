from typing import Generator, Any


def no_empty(value):
    """
    Check if value is not None and empty.
    """
    return (value is not None) and value


def is_empty(value):
    """
    Check if value is None or not empty in case if not None.
    """
    return (value is None) or (not value)


def get_or_else(value, default_value=None):
    """
    Return value if it is not empty. Otherwise default value (by default: None).
    """
    return value if no_empty(value) else default_value


class Optional:
    """
    Optional object holds data and allow control it with prepared functions.
    If stored value presents and its not None (is_present()) will return true. 'get()' will return stored value.
    get_or_else(default_value) will return stored value if exists, otherwise default_value.
    """

    _EMPTY = None

    def __init__(self, data: object):
        self._data = data

    @classmethod
    def empty(cls) -> object:
        if cls._EMPTY is None:
            cls._EMPTY = Optional(cls._EMPTY)
        return cls._EMPTY

    @classmethod
    def of(cls, data: object) -> object:
        """
        Get Optional object with provided data. If data is None, return Optional.empty object.

        :param data: an object,
        :return: Optional object.
        """
        return cls.empty() if is_empty(data) else Optional(data)

    def get(self) -> object:
        """
        :return: stored object.
        """
        return self._data

    def get_or_else(self, default_value: object) -> object:
        """
        :param default_value: default value.
        :return: return stored object if exists, otherwise default value.
        """
        return get_or_else(self._data, default_value)

    @property
    def present(self) -> bool:
        """
        :return: True if stored object is not empty, otherwise False.
        """
        return no_empty(self._data)

    def is_present(self) -> bool:
        """
        :return: True if stored object is not empty, otherwise False.
        """
        return self.present

    def if_present(self, func: Generator, default_value=None) -> Any:
        """
        Verify if stored object is present. If yes, that apply lambda function. If not ignore it.

        :param func: anonymous function (lambda) or regular function. Generator,
        :param default_value: object, default: None.
        :return: result from func if object is present, otherwise default value, None by default.
        """
        return func(self._data) if self.is_present() else default_value
