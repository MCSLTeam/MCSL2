import abc
import typing
from functools import partial

T = typing.TypeVar('T')


def FunctionalInterface(cls):
    if cls.__class__ is not abc.ABCMeta:
        raise TypeError("@FunctionalInterface can only be applied to abstract classes")

    abstract_methods = {name for name, val in cls.__dict__.items() if getattr(val, "__isabstractmethod__", False)}
    if len(abstract_methods) != 1:
        raise TypeError("@FunctionalInterface can only be applied to classes with exactly one abstract method")

    abstract_method_name = abstract_methods.pop()

    def of(func: typing.Callable[..., T]) -> cls:
        if not callable(func):
            raise TypeError("@FunctionalInterface: of method must be callable")

        new_cls_dict = cls.__dict__.copy()
        new_cls_dict[abstract_method_name] = func
        return type(cls.__name__, (cls,), new_cls_dict)()

    setattr(cls, 'of', of)

    return cls


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
