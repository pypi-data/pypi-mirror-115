from . import BaseDriver
from ..excepts import NoExplicitMessage, UnknownRequestError
from ..proto import is_data_request, bert2tf_pb2
from .control import ControlReqDriver


class ForwardDriver(BaseDriver):
    """Forward the message to next pod"""

    def __call__(self, *args, **kwargs):
        pass


class RouteDriver(ControlReqDriver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idle_dealers = set()
        self.is_pollin_paused = False

    def __call__(self, *args, **kwargs):
        if is_data_request(self.req):
            self.logger.debug(self.idle_dealers)
            if self.idle_dealers:
                dealer_id = self.idle_dealers.pop()
                self.envelope.receiver_id = dealer_id
                if not self.idle_dealers:
                    self.pea.zmqlet.pause_pollin()
                    self.is_pollin_paused = True

            else:
                raise RuntimeError('if this router connects more than one dealer, '
                                   'then this error should never be raised. often when it '
                                   'is raised, some Pods must fail to start, so please go '
                                   'up and check the first error message in the log')

        elif self.req.command == bert2tf_pb2.Request.ControlRequest.IDLE:
            self.idle_dealers.add(self.envelope.client_id)
            self.logger.debug(f'{self.envelope.client_id} is idle')
            if self.is_pollin_paused:
                self.pea.zmqlet.resume_pollin()
                self.is_pollin_paused = False
            raise NoExplicitMessage
        else:
            raise UnknownRequestError(f'unknown request type {type(self.req)}')
