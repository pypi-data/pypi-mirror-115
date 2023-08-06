from typing import Union, Iterator, Dict

import numpy as np
import tensorflow as tf

from ..excepts import BadInputs
from ..helper import array2pb
from ..proto import bert2tf_pb2


def _generate(inputs: Union[Iterator[int], Dict, Iterator[np.ndarray]], request_id: int = 0,
              mode: str = 'predict') -> bert2tf_pb2.Request:
    """Generate a request"""
    request = bert2tf_pb2.Request()

    request.request_id = request_id
    data = getattr(request, mode).data

    fill_data(data, inputs)

    return request


def fill_data(data: bert2tf_pb2.Data, inputs: Union[Iterator[int], Iterator[tf.Tensor], np.ndarray, tf.Tensor]) -> None:
    """Add data into protobuf message"""
    if isinstance(inputs, (list, tuple)):
        if not isinstance(inputs[0], tf.Tensor):
            if len(np.array(inputs).shape) == 3:
                for item in inputs:
                    data.blob.add().CopyFrom(array2pb(np.array(item)))
            elif len(np.array(inputs).shape) == 2:
                data.blob.add().CopyFrom(array2pb(np.array(inputs)))
            else:
                raise BadInputs(f'except 2 or 3 axis, got {len(np.array(inputs).shape)}')
        else:
            for item in inputs:
                data.blob.add().CopyFrom(array2pb(item.numpy()))

    elif isinstance(inputs, tf.Tensor):
        data.blob.add().CopyFrom(array2pb(inputs.numpy()))
    elif isinstance(inputs, np.ndarray):
        data.blob.add().CopyFrom(array2pb(inputs))
    else:
        raise ValueError(f'the data type: {type(inputs)} is not support')


def predict(*args, **kwargs):
    """Generate predict request"""
    return _generate(*args, **kwargs)
