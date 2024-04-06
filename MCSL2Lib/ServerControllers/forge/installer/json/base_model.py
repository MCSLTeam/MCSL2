import typing
from dataclasses import dataclass, fields, MISSING


@dataclass
class BaseModel:
    @classmethod
    def from_dict(cls, data: dict):
        # cls_fields = {field.name for field in fields(cls)}
        # return cls(**{k:data.get(k, None)  for k in cls_fields})
        cls_fields = {field.name: field for field in fields(cls)}
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

        factories = cls.get_factories(cls_fields.keys())
        for field in factories:
            if filtered_dict[field] is None: continue
            filtered_dict[field] = factories[field](filtered_dict[field])

        return cls(**filtered_dict)

    @classmethod
    def get_factories(cls, fields_: typing.Iterable[str]):
        factories = {}
        for field in fields_:
            factory = getattr(cls, field + "_factory", None)
            if factory is not None:
                factories[field] = factory

        return factories
