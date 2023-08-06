import logging

import ruamel

from ..helper import yaml
from ..models import AnyModel
from ..peapods.pea import BasePea
from ..proto import bert2tf_pb2


class DriverType(type):

    def __new__(cls, *args, **kwargs):
        _cls = super().__new__(cls, *args, **kwargs)
        return cls.register_class(_cls)

    @staticmethod
    def register_class(cls):
        reg_cls_set = getattr(cls, '_registered_class', set())
        if cls.__name__ not in reg_cls_set:
            reg_cls_set.add(cls.__name__)
            setattr(cls, '_registered_class', reg_cls_set)
        yaml.register_class(cls)
        return cls


class BaseDriver(metaclass=DriverType):
    """A :class:`BaseDriver` is a logic unit above the :class:`bert2tf.peapods.pea.BasePea`.
    It reads the protobuf message, extracts/modifies the required information and then return
    the message back to :class:`bert2f.peapods.pea.BasePea`.

    A :class:`BaseDriver` needs to be :attr:`attached` to a :class:`bert2tf.peapods.pea.BasePea` before using. This is done by
    :func:`attach`. Note that a deserialized :class:`BaseDriver` from file is always unattached.

    """
    store_args_kwargs = False

    def __init__(self, *args, **kwargs):
        self.attached = False
        self.pea = None  # type: 'BasePea'

    def attach(self, pea: 'BasePea', *args, **kwargs) -> None:
        """Attach this driver to a :class:`bert2tf.peapods.pea.BasePea`

        :param pea: the pea to be attached.
        """
        self.pea = pea
        self.attached = True

    @classmethod
    def _get_instance_from_yaml(cls, constructor, node):
        data = ruamel.yaml.constructor.SafeConstructor.construct_mapping(
            constructor, node, deep=True)

        obj = cls(**data.get('with', {}))
        return obj

    @classmethod
    def from_yaml(cls, constructor, node):
        """Required by :mod:`ruamel.yaml.constructor` """
        return cls._get_instance_from_yaml(constructor, node)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def req(self) -> 'bert2tf_pb2.Request':
        """Get the current (typed) request, shortcut to ``self.pea.request``"""
        return self.pea.request

    @property
    def msg(self) -> 'bert2tf_pb2.Message':
        """Get the current request, shortcut to ``self.pea.message``"""
        return self.pea.message

    @property
    def envelope(self) -> 'bert2tf_pb2.Envelope':
        """Get the current request, shortcut to ``self.pea.message``"""
        return self.msg.envelope

    @property
    def logger(self) -> 'logging.Logger':
        """Shortcut to ``self.pea.logger``"""
        return self.pea.logger


class BaseExecutableDriver(BaseDriver):
    def __init__(self, method: str = None, *args, **kwargs):
        """ Initialize a :class:`BaseExecutableDriver`

        :param method: the function name of the executor that the driver feeds to
        """
        super().__init__(*args, **kwargs)
        self._method_name = method
        self._model = None
        self._model_fn = None

    def attach(self, model: 'AnyModel', *args, **kwargs):
        super().attach(*args, **kwargs)
        self._model = model

        if self._method_name:
            self._model_fn = getattr(self.model, self._method_name)
        else:
            self._model_fn = getattr(self.model, 'call')

    @property
    def model(self) -> 'AnyModel':
        """the model that attached """
        return self._model

    @property
    def model_fn(self):
        """the model main function, can be customized, default `call`"""
        return self._model_fn
