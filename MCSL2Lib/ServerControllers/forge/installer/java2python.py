import abc
import typing
from functools import partial

T = typing.TypeVar('T')


class Supplier(typing.Generic[T], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self) -> T:
        ...

    @classmethod
    def of(cls, supplier: typing.Callable[[], T]) -> 'Supplier[T]':
        return _SupplierInstance(supplier)


class _SupplierInstance(Supplier[T]):

    def __init__(self, supplier: typing.Callable[[], T]):
        self.__supplier = partial(supplier)

    def get(self) -> T:
        return self.__supplier()
