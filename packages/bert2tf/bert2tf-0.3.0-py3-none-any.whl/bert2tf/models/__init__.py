import re
from typing import Dict, List, TypeVar

import ruamel.yaml.constructor
import tensorflow as tf
from ruamel.yaml import StringIO
from tensorflow.python.keras import backend as K

from ..excepts import YAMLEmptyError, UnattachedDriver, NoDriverForRequest
from ..helper import get_local_config_source, yaml
from ..logging.base import get_logger

__all__ = ['BaseModel', 'AnyModel', 'ModelType']

AnyModel = TypeVar('AnyModel', bound='BaseModel')


class ModelType(type):
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


class BaseModel(tf.keras.Model, metaclass=ModelType):
    """Base models"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._drivers = {}  # type: Dict[str, List['BaseDriver']]

        self.logger = get_logger(self.__class__.__name__)

    def get_dummy_inputs(self):
        """
        get models inputs
        note:
        if the models need init from pre trained models, it must implement this function
        :return: multi input tensor
        """

    @classmethod
    def build_model(cls, pretrained_model_path=None, *args, **kwargs):
        """
        Build models
        :param pretrained_model_path: pre trained models save path
        :return: keras models
        """
        model = cls(*args, **kwargs)

        if pretrained_model_path:
            inputs = model.get_dummy_inputs()  # dumpy inputs
            if inputs is None:
                raise NotImplementedError(
                    'if you want to weights from pre trained models, you must implement `get_dummy_inputs`')
            model(inputs)  # do pre build
            weight_value_tuples = model.mapping(pretrained_model_path)
            if weight_value_tuples is None:
                raise NotImplementedError('if you want to restore weights from pre trained model, '
                                          'you must implement `mapping`, '
                                          'and return a tuple like this ([resource_var, value]) from mapping')
            K.batch_set_value(weight_value_tuples)
            model.logger.success(f'successfully restored {cls.__name__} weights from pre trained model')

        return model

    @classmethod
    def load_config(cls, source):
        source = get_local_config_source(source)
        with open(source, 'r', encoding='utf-8') as fp:
            # ignore all lines start with ! because they could trigger the deserialization of that class
            safe_yml = '\n'.join(v if not re.match(r'^[\s-]*?!\b', v) else v.replace('!', '__tag: ') for v in fp)
            tmp = yaml.load(safe_yml)
            if tmp:
                stream = StringIO()
                yaml.dump(tmp, stream)
                tmp_s = stream.getvalue().strip().replace('__tag: ', '!')
                return yaml.load(tmp_s)
            else:
                raise YAMLEmptyError(f'{source} is empty? nothing to read from there')

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls._get_instance_from_yaml(constructor, node)[0]

    @classmethod
    def _get_instance_from_yaml(cls, constructor, node):
        data = ruamel.yaml.constructor.SafeConstructor.construct_mapping(
            constructor, node, deep=True)
        obj = cls.build_model(**data.get('with', {}))
        obj._fill_requests(data.get('requests', {}))
        obj.logger.success(f'successfully built {cls.__name__} from a yaml config')

        return obj, data

    def attach(self, *args, **kwargs):
        for v in self._drivers.values():
            for driver in v:
                driver.attach(model=self, *args, **kwargs)

    def _fill_requests(self, _requests):
        if _requests and 'on' in _requests and isinstance(_requests['on'], dict):
            # if control request is forget in YAML, then fill it
            if 'ControlRequest' not in _requests['on']:
                from ..drivers.control import ControlReqDriver
                _requests['on']['ControlRequest'] = [ControlReqDriver()]

            for req_type, drivers in _requests['on'].items():
                if isinstance(req_type, str):
                    req_type = [req_type]
                for r in req_type:
                    if r not in self._drivers:
                        self._drivers[r] = list()
                    if self._drivers[r] != drivers:
                        self._drivers[r].extend(drivers)

    def get_name_to_variable(self):
        """
        get trainable variables dict, key is variable name, value is resources variable
        """
        import collections
        name_to_variable = collections.OrderedDict()
        for var in self.trainable_variables:
            name = var.name
            m = re.match('^(.*):\\d+$', name)
            if m is not None:
                name = m.group(1)
            name_to_variable[name] = var

        return name_to_variable

    def mapping(self, pretrained_model_path: str):
        """Return a dict which key is trainable resources, value is pre trained value.
           the tuple like this [(resource_var, value)]
        """

    def work(self, request_type, *args, **kwargs):
        if request_type in self._drivers:
            for driver in self._drivers[request_type]:
                if driver.attached:
                    driver()
                else:
                    raise UnattachedDriver(driver)

        else:
            raise NoDriverForRequest(request_type)


class Model(BaseModel):
    """Model for not pretrained models"""


class PreTrainModel(Model):
    """Model for pretrained models"""

    def get_dummy_inputs(self):
        raise NotImplementedError
