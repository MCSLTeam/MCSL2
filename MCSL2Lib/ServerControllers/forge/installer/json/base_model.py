import abc
import functools
import inspect
import typing
from dataclasses import dataclass, fields, MISSING, Field


class InjectError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class TypeFactory(metaclass=abc.ABCMeta):
    def __call__(self, *args, **kwargs):
        """
        however, this method doesn't work

        """
        print("__call__")
        factory = kwargs.get("factory", None)
        if factory is not None:
            return factory(self, *args, **kwargs)
        elif len(args) > 0:
            if callable(factory := args[0]):
                return self.default(factory)
        return super.__call__(*args, **kwargs)

    @abc.abstractmethod
    def get(self, data: typing.Any):
        ...

    @classmethod
    def from_supplier(cls, supplier: typing.Callable[[typing.Any], typing.Any]) -> 'TypeFactory':
        return type("TypeFactoryInstance", (TypeFactory,), {
            "get": lambda self, data: supplier(data)
        })()

    @classmethod
    def default(cls, factory: typing.Callable) -> 'TypeFactory':
        """
        invoke factory with data
        """
        return cls.from_supplier(factory)

    @classmethod
    def base_model(cls, type_hint: type) -> 'TypeFactory':
        """
        invoke <? impl BaseModel>.from_dict with data
        """
        return cls.from_supplier(lambda data: type_hint.from_dict(data))

    @classmethod
    def inject(cls, factory: typing.Callable) -> 'TypeFactory':
        """
        directly invoke factory
        """
        return cls.from_supplier(lambda _: factory())

    @classmethod
    def pass_through(cls) -> 'TypeFactory':
        """
        directly pass through data
        """
        return cls.from_supplier(lambda data: data)


USER_DEFINED_GENERIC_FACTORIES = {}  # Does not support user defined generic!!! only typing provided are valid


def add_generic_factory(type_hint: typing.Type, supplier: typing.Callable[[typing.Any], typing.Any]):
    """
    *** Does not support user defined generic ***
    *** only typing provided are valid ***
    """
    USER_DEFINED_GENERIC_FACTORIES[type_hint] = TypeFactory.from_supplier(supplier)


@dataclass
class BaseModel:
    BASE_VAR_TYPES = (int, float, str, bool, list, dict, tuple, complex, None)
    INJECT_WHITELIST = {}
    GenericAlias = getattr(typing, "_GenericAlias")

    @classmethod
    def of(cls, data: dict):
        # cls_fields = {field.name for field in fields(cls)}
        # return cls(**{k:data.get(k, None)  for k in cls_fields})
        cls_fields: typing.Dict[str, Field] = {field.name: field for field in fields(cls)}
        filtered_dict = {}
        for k, field in cls_fields.items():
            if k in data:
                filtered_dict[k] = data[k]
            elif field.default is not MISSING:
                filtered_dict[k] = field.default
            elif field.default_factory is not MISSING:
                filtered_dict[k] = field.default_factory()
            else:
                filtered_dict[k] = None

        all_fields_types = typing.get_type_hints(cls)

        custom_factories: typing.Dict[str, TypeFactory] = cls._get_factories({
            k: all_fields_types[k] for k in all_fields_types if k in cls_fields
        })  # scan custom factories

        default_factories_field = set(cls_fields.keys()) - set(custom_factories.keys())
        custom_factories.update({
            field: cls._init_inject(filtered_dict[field], all_fields_types[field])
            for field in default_factories_field
            if not cls._is_base_type(all_fields_types[field])  # apply injection if no custom factory
        })

        for field in custom_factories:
            if filtered_dict[field] is None: continue
            filtered_dict[field] = custom_factories[field].get(filtered_dict[field])

        return cls(**filtered_dict)

    @classmethod
    def _is_base_type(cls, type_hint: typing.Type) -> bool:
        return cls._get_type(type_hint) in cls.BASE_VAR_TYPES

    @classmethod
    def _get_type(cls, type_hint: typing.Type):
        if hasattr(type_hint, "__origin__"):
            return type_hint.__origin__
        if hasattr(type_hint,"__forward_arg__"):
            raise RuntimeError(f"{type_hint.__forward_arg__} Out of context.")
        return type_hint

    @classmethod
    def _get_factories(cls, fields_with_factory: typing.Dict[str, typing.Type]) -> typing.Dict[str, TypeFactory]:
        factories = {}
        for field, field_hint_type in fields_with_factory.items():
            factory = getattr(cls, field + "_factory", None)
            if factory is not None:
                factories[field] = TypeFactory.from_supplier(factory)
            elif hasattr(field_hint_type, "__origin__"):  # assumed to be generic
                try:
                    factories[field] = cls._get_generic_type_factory(
                        field_hint_type,
                        *getattr(field_hint_type, "__args__")
                    )
                except AttributeError:
                    print("type:", field_hint_type, ",is not a generic type")
                    continue
            else:
                if cls._is_base_model(field_hint_type):
                    factories[field] = TypeFactory.base_model(field_hint_type)

        return factories

    @classmethod
    def _list_factory(cls, element_type: typing.Type) -> TypeFactory:
        """
        type_hint:获取注解

        *** AUTOMATICALLY REGISTERED *** (use getattr in cls._get_generic_type_factory)
        """
        # TODO: 递归的扫描泛型
        return TypeFactory.from_supplier(lambda data: [
            cls._get_type_supplier(
                type_hint=element_type
            )(e) for e in data
        ])

    @classmethod
    def _dict_factory(cls, KT: typing.Type, VT: typing.Type) -> TypeFactory:
        """
        type_hint:获取注解
        KT:BaseModel,BaseVarType,SomeClass implements __eq__,__hash__
        VT:BaseModel,BaseVarType,object

        *** AUTOMATICALLY REGISTERED *** (use getattr in cls._get_generic_type_factory)
        """
        # TODO: 递归的扫描泛型
        KT_supplier = cls._get_type_supplier(type_hint=KT)
        VT_supplier = cls._get_type_supplier(type_hint=VT)

        return TypeFactory.from_supplier(lambda data: {
            KT_supplier(k): VT_supplier(v) for k, v in data.items()
        })

    @classmethod
    def _get_generic_type_factory(cls, type_hint: typing._GenericAlias, *args) -> TypeFactory:
        """
        *** AUTOMATICALLY GET GENERIC TYPE FACTORY *** (use getattr)

        args: types

        register factory:
            @classmethod
            def _{type_hint._name.lower()}factory(cls,*args) -> TypeFactory:
                ...

            > if some arg has particular usage:

            @classmethod
            def _{type_hint._name.lower()}factory(cls,KT,VT,*args) -> TypeFactory:
                ...

            > OR
            @classmethod
            def _{type_hint._name.lower()}factory(cls,KT,VT) -> TypeFactory:
                ...

        """
        # TODO: 递归的扫描泛型
        if type_hint not in USER_DEFINED_GENERIC_FACTORIES:
            f_name = f"_{type_hint._name.lower()}_factory"
            if hasattr(cls, f_name):
                return getattr(cls, f_name)(*args)
            else:
                return TypeFactory.pass_through()
        else:
            return USER_DEFINED_GENERIC_FACTORIES[type_hint]

    @classmethod
    def _get_type_supplier(
            cls,
            type_hint: typing.Type,
            base_model_supplier: typing.Callable = None,
            base_var_type_supplier: typing.Callable = None,
            default_supplier: typing.Callable = None,
    ) -> typing.Callable:
        if cls._is_base_model(type_hint):
            return base_model_supplier or type_hint.from_dict
        elif cls._is_base_type(type_hint):
            return base_var_type_supplier or (lambda _: _)
        else:
            return default_supplier or functools.partial(cls._init_inject, type_hint=type_hint)

    @classmethod
    def _is_base_model(cls, type_hint: typing.Type) -> bool:
        return issubclass(cls._get_type(type_hint), BaseModel)

    @classmethod
    def _init_inject(cls, data: typing.Dict, type_hint: typing.Type, strict_mode: bool = False) -> TypeFactory:
        """
        return a class factory
        """
        # inspect type_hint`s constructor
        # TODO support generic type

        if type_hint not in BaseModel.INJECT_WHITELIST: # pass through if not in inject whitelist
            return TypeFactory.pass_through()

        signature = inspect.signature(type_hint.__init__)
        params_to_bind = {}
        for sig, param in signature.parameters.items():
            if sig == "self":
                continue

            if sig not in data and param.default is inspect.Parameter.empty:
                raise InjectError(f"{type_hint.__name__} missing argument {sig}")

            value = data[sig]
            if (
                    strict_mode
                    and param.annotation is not inspect.Parameter.empty
                    and not isinstance(value, param.annotation)
            ):  # TODO: support generic type and typing._SpecialForm
                raise InjectError(f"{type_hint.__name__} argument {sig} type error")
            params_to_bind[sig] = value

        bound_args = signature.bind_partial(**params_to_bind)
        return TypeFactory.inject(functools.partial(type_hint, **bound_args.arguments))