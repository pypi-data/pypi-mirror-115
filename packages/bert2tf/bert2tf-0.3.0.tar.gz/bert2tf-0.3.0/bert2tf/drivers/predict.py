from . import BaseExecutableDriver
from ..client.request import fill_data
from ..helper import pb2array


class PredictDriver(BaseExecutableDriver):
    """Driver for all of predict request"""

    def __call__(self, *args, **kwargs):
        inputs = [pb2array(item) for item in self.req.data.blob]
        results = self.model_fn(inputs)
        self.req.data.ClearField('blob')
        fill_data(self.req.data, results)