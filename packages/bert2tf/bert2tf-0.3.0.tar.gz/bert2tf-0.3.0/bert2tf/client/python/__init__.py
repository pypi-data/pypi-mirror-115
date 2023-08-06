from typing import Union, List, Dict, Callable

from .grpc import GrpcClient
from .. import request
from ...proto import bert2tf_pb2


class PyClient(GrpcClient):
    def call(self, inputs: Union[List, Dict], tname: str, callback: Callable = None, **kwargs):
        req = getattr(request, tname)(inputs, **kwargs)
        req = self._stub.CallUnary(req)

        if callback:
            callback(req)

    def predict(self, inputs: Union[List, Dict], **kwargs) -> bert2tf_pb2.Request:
        self.start(inputs, tname='predict', **kwargs)
