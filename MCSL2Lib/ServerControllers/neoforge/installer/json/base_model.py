import builtins
import dataclasses
import functools
import inspect
import json
import sys
import traceback
import typing
import warnings

InjectError = Exception


class GenericFactory:
    custom_factories = {}

    @staticmethod
    def list(type_hint: typing.Any, data: typing.List[typing.Any]):
        (i_type,) = typing.get_args(type_hint)

        i_type_supplier = Utils.get_type_eval_supplier(i_type)
        return [i_type_supplier(i) for i in data]

    @staticmethod
    def dict(type_hint: typing.Any, data: typing.Dict[typing.Any, typing.Any]):
        (
            k_type,
            v_type,
        ) = typing.get_args(type_hint)

        k_type_supplier = Utils.get_type_eval_supplier(k_type)
        v_type_supplier = Utils.get_type_eval_supplier(v_type)

        return {k_type_supplier(k): v_type_supplier(v) for k, v in data.items()}

    @staticmethod
    def get(type_hint: typing.Any) -> typing.Callable[[typing.Any], typing.Any]:
        return functools.partial(
            {
                list: GenericFactory.list,
                dict: GenericFactory.dict,
                **GenericFactory.custom_factories,
            }.get(Utils.get_type(type_hint), lambda t, d: d),
            type_hint,
        )


class Utils:
    BASE_VAR_TYPES: typing.Tuple[typing.Type] = (
        int,
        float,
        str,
        bool,
        complex,
        type(None),
    )

    @staticmethod
    def get_type(type_hint: typing.Any):
        t_type = typing.get_origin(type_hint)
        if t_type is not None:
            return t_type
        if Utils.is_forward_ref(type_hint):
            return typing._eval_type(type_hint, globals(), locals())
        return type_hint

    @staticmethod
    def is_base_type(type_hint: typing.Any) -> bool:
        return Utils.get_type(type_hint) in Utils.BASE_VAR_TYPES

    @staticmethod
    def is_base_model(type_hint: typing.Any) -> bool:
        return issubclass(Utils.get_type(type_hint), BaseModel)

    @staticmethod
    def is_generic_type(type_hint: typing.Type) -> bool:
        return hasattr(type_hint, "__origin__")

    @staticmethod
    def is_special_type(type_hint: typing.Type) -> bool:
        return type_hint.__module__ == "typing" and hasattr(type_hint, "_name")

    @staticmethod
    def is_forward_ref(type_hint: typing.Type) -> bool:
        return hasattr(type_hint, "__forward_arg__")

    @staticmethod
    def constructor_inject(data: typing.Dict, type_hint: typing.Type, strict: bool = True):
        # TODO
        """
        return a class factory
        """
        # inspect type_hint`s constructor
        if Utils.is_generic_type(type_hint):
            raise ValueError("Generic type's constructor injection is not supported")

        signature = inspect.signature(type_hint.__init__)
        params = signature.parameters
        params_to_bind = {}
        for sig, param in params.items():
            if sig == "self":
                continue

            if sig not in data and param.default is inspect.Parameter.empty:
                raise InjectError(f"{type_hint.__name__} missing argument {sig}")

            if sig not in data and param.default is not inspect.Parameter.empty:
                continue  # not value provided but default value existing, just skip it

            if param.annotation is not inspect.Parameter.empty:
                # try:
                supplier = Utils.get_type_eval_supplier(eval(param.annotation))  # parse type
                value = supplier(data[sig])
                # except Exception:
                #     raise InjectError(
                #         f"cannot transform data:\n{json.dumps(data, indent=2, sort_keys=True)}\n to type: {param.annotation}"
                #     )
            elif param.annotation is inspect.Parameter.empty and strict:
                raise InjectError(
                    f'in class {type_hint.__name__}: <"{param}"> in  <"__init__{signature}"> do not have a annotation.'
                )
            else:
                value = data[sig]
            params_to_bind[sig] = value

        bound_args = signature.bind_partial(**params_to_bind)
        return type_hint(**bound_args.arguments)

    @staticmethod
    def get_type_eval_supplier(
        type_hint: typing.Any,
        base_model_supplier: typing.Callable = None,
        base_var_type_supplier: typing.Callable = None,
        generic_type_supplier: typing.Callable = None,
        default_supplier: typing.Callable = None,
    ) -> typing.Callable[[typing.Any], typing.Any]:
        """
        get 'type_hint' init method (the way to init a 'type_hint' instance use data provided)
        """

        if Utils.is_base_type(type_hint):
            # base var type (int,float, ...), pass through
            return base_var_type_supplier or (lambda _: _)

        elif Utils.is_generic_type(type_hint):
            # generic type, recursively scan
            return generic_type_supplier or (lambda data: Utils.scan_generic_type(type_hint, data))

        elif Utils.is_special_type(type_hint):
            name = getattr(type_hint, "_name")
            if name == "Optional":
                # prevent Optional[None]
                args = typing.get_args(type_hint)
                if not args:
                    return lambda _: None

                (
                    some_type,
                    none,
                ) = typing.get_args(type_hint)
                return lambda data: Utils.get_type_eval_supplier(some_type)(data) if data else None

            elif name == "Literal":
                literals = typing.get_args(type_hint)
                if not literals:
                    raise ValueError(f"not support raw typing.Literal.")

                def ret(data):
                    if data in literals:
                        return data
                    else:
                        raise ValueError(f"{data} is not in {literals}")

                return ret

            elif name == "Union":
                union_types = typing.get_args(type_hint)

                # is optional
                if len(union_types) == 2 and union_types[1] == type(None):
                    (
                        some_type,
                        none,
                    ) = typing.get_args(type_hint)
                    return (
                        lambda data: Utils.get_type_eval_supplier(some_type)(data) if data else None
                    )

            else:
                ValueError(f"{type_hint} is not supported.")

        elif Utils.is_forward_ref(type_hint):
            ValueError(f"{type_hint} is not supported.")

        elif Utils.is_base_model(type_hint):
            # base model, use 'of' method
            return base_model_supplier or type_hint.of
        else:
            # raise ValueError(f"{type_hint} is not supported.")
            # common class, use '__init__' method
            return default_supplier or functools.partial(
                Utils.constructor_inject, type_hint=type_hint
            )

    @staticmethod
    def scan_generic_type(type_hint: typing.Any, data: typing.Any) -> typing.Any:
        """
        construct generic type from its type and data
        """
        return GenericFactory.get(type_hint)(data)

    @staticmethod
    def get_type_string(t_type: typing.Any):
        if t_type in (None, ...):
            return t_type
        if t_type.__module__ == "typing":
            return str(t_type)
        else:
            try:
                return t_type.__name__
            except AttributeError:
                raise Exception("Could not get type string:", t_type)

    @staticmethod
    def gen_fn(f_name, args, body, *, globals_=None, locals_=None, t_return=None):
        if locals_ is None:
            locals_ = {}
        if "BUILTINS" not in locals_:
            locals_["BUILTINS"] = builtins

        locals_["_t_return"] = Utils.get_type_string(t_return)
        t_return = "_t_return"

        f_args = ", ".join(args)
        f_body = "".join(f"\n  {b}" for b in body)

        f_code = f" def {f_name}({f_args}) -> {t_return}:{f_body}"

        local_vars = ", ".join(locals_.keys())
        txt = f"def _gen_fn({local_vars}):\n{f_code}\n return {f_name}"

        rv = {}
        exec(txt, globals_, rv)
        return rv["_gen_fn"](**locals_)

    @staticmethod
    def is_init_overridden(cls):
        base_init = cls.__base__.__init__
        current_init = cls.__init__
        return not (
            current_init is base_init or inspect.unwrap(current_init) is inspect.unwrap(base_init)
        )

    @staticmethod
    def get_builtins_type_factory(t_type: typing.Any) -> typing.Optional[typing.Callable]:
        """
        get default type factory for cls
        """
        r_type = Utils.get_type(t_type)
        if r_type in (
            int,
            float,
            str,
            bool,
            list,
            dict,
            set,
            tuple,
            bytes,
            bytearray,
        ):
            return r_type
        return None


class BaseModelMeta(type):
    """
    自动注册根据__annotations__注册__init__，类似dataclass,
    若__init__被重写，则不会自动注册

    提供__base_model_fields__
    """

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if name == "BaseModel":
            return

        cls_annotations = typing.get_type_hints(cls)  # recursively scan to solve inheritance
        cls.__base_model_fields__ = tuple(cls_annotations.keys())

        if cls.__module__ in sys.modules:
            globals_ = sys.modules[cls.__module__].__dict__
        else:
            globals_ = {}

        locals_ = {}
        init_args = []
        arg_counter = 0
        for arg_name, anno in cls_annotations.items():
            new_anno = f"_t_arg{arg_counter}"
            locals_[new_anno] = anno
            init_args.append(f"{arg_name}: {new_anno}")
            arg_counter += 1

        locals_.update({"BUILTINS": builtins})
        dataclasses.dataclass()
        init_body = "".join(f"\n    self.{p} = {p}" for p in cls_annotations.keys()) or "\n    pass"

        __init__ = Utils.gen_fn(
            f"__init__", ["self"] + init_args, [init_body], globals_=globals_, locals_=locals_
        )
        # check init if is user defined
        if not Utils.is_init_overridden(cls):
            cls.__init__ = __init__


class BaseModelJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            fields = o.__base_model_fields__
            return {k: getattr(o, k) for k in fields}
        return json.JSONEncoder.default(self, o)


class BaseModel(metaclass=BaseModelMeta):
    """
    dataclass pro版，
    解决无法递归的反序列化类的问题，

    反序列化类: cls.of
    """

    @classmethod
    def of(cls, provided: typing.Dict[str, typing.Any]):
        """
        从json中构造一个类, (如果有__from_raw__(cls,data:Any) -> Self存在，则使用__from_raw__)
        """
        if provided is None:
            return None

        if hasattr(cls, "__from_raw__"):  # get raw supplier
            return getattr(cls, "__from_raw__")(provided)

        annotations = typing.get_type_hints(cls)

        data = {}
        for k, v in annotations.items():
            if k in provided:
                supplier = Utils.get_type_eval_supplier(
                    v
                )  # use provided value, and recursively parse it
                data[k] = supplier(provided[k])
            elif hasattr(cls, k):
                data[k] = getattr(cls, k)  # use default value
            else:
                default_supplier = Utils.get_builtins_type_factory(v)
                if default_supplier is None:
                    data[k] = None
                    warnings.warn(f"{cls.__name__} has no default value for {k}")
                else:
                    data[k] = default_supplier()
        return cls(**data)

    def to_dict(self):
        try:
            return json.loads(json.dumps(self, cls=BaseModelJsonEncoder))
        except:
            traceback.print_exc()
