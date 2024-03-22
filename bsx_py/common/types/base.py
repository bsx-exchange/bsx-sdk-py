import inspect


class DataClassMeta(type):
    # def __call__(cls, *args, **kwargs):
    #     return cls(**{
    #         k: v for k, v in kwargs.items()
    #         if k in inspect.signature(cls).parameters
    #     })
    pass