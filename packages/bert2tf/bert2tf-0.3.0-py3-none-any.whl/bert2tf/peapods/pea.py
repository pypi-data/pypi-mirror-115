import argparse
import multiprocessing
import threading
import traceback
from multiprocessing import Process
from multiprocessing.synchronize import Event
from typing import Union, Dict

import zmq

from .zmq import Zmqlet, send_ctrl_message, ZmqStreamlet
from ..enums import PeaRoleType
from ..excepts import PeaFailToStart, NoExplicitMessage
from ..helper import routes2str
from ..logging.base import get_logger
from ..models import BaseModel
from ..proto import bert2tf_pb2, add_route


def _get_event(obj: 'BasePea') -> Event:
    if isinstance(obj, threading.Thread):
        return threading.Event()
    elif isinstance(obj, multiprocessing.Process):
        return multiprocessing.Event()
    else:
        raise NotImplementedError


def _make_or_event(obj: 'BasePea', *events) -> Event:
    or_event = _get_event(obj)

    def or_set(self):
        self._set()
        self.changed()

    def or_clear(self):
        self._clear()
        self.changed()

    def orify(e, changed_callback):
        e._set = e.set
        e._clear = e.clear
        e.changed = changed_callback
        e.set = lambda: or_set(e)
        e.clear = lambda: or_clear(e)

    def changed():
        bools = [e.is_set() for e in events]
        if any(bools):
            or_event.set()
        else:
            or_event.clear()

    for e in events:
        orify(e, changed)
    changed()
    return or_event


class BasePea(Process):
    """The basic unit in Pod"""

    def __init__(self, args: Union['argparse.Namespace', Dict]):
        super().__init__()

        self.name = self.__class__.__name__.lower()

        self.is_ready = _get_event(self)
        self.is_shutdown = _get_event(self)
        self.ready_or_shutdown = _make_or_event(self, self.is_ready, self.is_shutdown)
        self.is_shutdown.clear()

        self.is_head_router = False
        self.is_tail_router = False

        self.args = args

        if args.name:
            self.name = args.name
        if args.role == PeaRoleType.REPLICA:
            self.name = f'{self.name}-{args.replicas_id}'

        args.name = self.name
        self.logger = get_logger(self.name)

        self._message = None
        self._request = None
        self.ctrl_addr = Zmqlet.get_ctrl_address(self.args)

    def run(self):
        try:
            self.post_init()
            self.loop_body()
        except KeyboardInterrupt:
            pass
        except zmq.error.ZMQError:
            self.logger.critical('zmqlet can not be initiated')
        except Exception as ex:
            self.logger.critical(f'met unknown exception {repr(ex)}', exc_info=True)
        finally:
            self.loop_teardown()
            self.unset_ready()
            self.is_shutdown.set()

    def start(self):
        super().start()

        _timeout = getattr(self.args, 'timeout_ready', -1)
        if _timeout <= 0:
            _timeout = None
        else:
            _timeout /= 1e3

        if self.ready_or_shutdown.wait(_timeout):
            if self.is_shutdown.is_set():
                # return too early and the shutdown is set, means something fails!!
                self.logger.critical(f'fail to start {self.__class__} with name {self.name}, '
                                     f'this often means the model used in the pod is not valid')
                raise PeaFailToStart
            return self
        else:
            raise TimeoutError(
                f'{self.__class__} with name {self.name} can not be initialized after {_timeout * 1e3}ms')

    def loop_body(self):
        self.load_model()
        self.zmqlet = ZmqStreamlet(self.args)
        self.set_ready()
        self.zmqlet.start(self.msg_callback)

    def pre_hook(self, msg: bert2tf_pb2.Message) -> 'BasePea':
        msg_type = msg.request.WhichOneof('body')
        self.logger.info(
            f'received "{msg_type}" from {routes2str(msg, flag_current=True)} client {msg.envelope.client_id}')

        self._message = msg
        self._request = getattr(msg.request, msg_type)
        add_route(self.message.envelope, self.name, self.args.identity)

        return self

    def handle(self, msg: bert2tf_pb2.Message) -> 'BasePea':
        if msg.envelope.status.code != bert2tf_pb2.Status.ERROR:
            self.model.work(self.request_type)
        return self

    def post_hook(self, msg: bert2tf_pb2.Message) -> 'BasePea':
        msg.envelope.routes[-1].end_time.GetCurrentTime()
        return self

    def _callback(self, msg: bert2tf_pb2.Message) -> bert2tf_pb2.Message:
        if msg.envelope.status.code != bert2tf_pb2.Status.ERROR:
            self.pre_hook(msg).handle(msg).post_hook(msg)

        return msg

    def msg_callback(self, msg: bert2tf_pb2.Message) -> bert2tf_pb2.Message:
        try:
            self.zmqlet.send_message(self._callback(msg))
        except (SystemError, zmq.error.ZMQError, KeyboardInterrupt) as ex:
            self.logger.info(f'{repr(ex)} causes the breaking from the event loop')
            # serious error happen in callback, we need to break the event loop
            self.zmqlet.send_message(msg)
            # note, the logger can only be put on the second last line before `close`, as when
            # `close` is called, the callback is unregistered and everything after `close` can not be reached
            # some black magic in eventloop i guess?
            self.loop_teardown()
        except NoExplicitMessage:
            # silent and do not propagate message anymore
            # 1. wait partial message to be finished
            # 2. dealer send a control message and no need to go on
            pass
        except (RuntimeError, Exception) as ex:
            msg.envelope.status.code = bert2tf_pb2.Status.ERROR
            if not msg.envelope.status.description:
                msg.envelope.status.description = f'{self} throws {repr(ex)}'
            d = msg.envelope.status.details.add()
            d.pod = self.name
            d.pod_id = self.args.identity
            d.exception = repr(ex)
            d.traceback = traceback.format_exc()
            d.time.GetCurrentTime()
            self.logger.error(ex, exc_info=True)

            self.zmqlet.send_message(msg)

    def load_model(self):
        self.model = BaseModel.load_config(self.args.yaml_path)
        self.model.attach(pea=self)

    def post_init(self):
        self.to_device()

    def set_ready(self, *args, **kwargs):
        """Set the status of the pea to ready """
        from .. import __ready_msg__
        if not self.is_ready.is_set():
            self.is_ready.set()
            self.logger.info(__ready_msg__)

    def unset_ready(self, *args, **kwargs):
        """Set the status of the pea to shutdown """
        if self.is_ready.is_set():
            from .. import __stop_msg__
            self.is_ready.clear()
            self.logger.success(__stop_msg__)

    def loop_teardown(self):
        """Stop the request loop """
        if hasattr(self, 'zmqlet'):
            self.zmqlet.close()

    def to_device(self):
        import tensorflow as tf
        tf.config.experimental.set_visible_devices(devices=self.device)

    def close(self):
        send_ctrl_message(self.ctrl_addr, bert2tf_pb2.Request.ControlRequest.TERMINATE, self.args.timeout_ctrl)

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.join()

    @property
    def message(self):
        return self._message

    @property
    def device(self):
        import tensorflow as tf
        if self.args.device_id >= 0:
            gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
            if len(gpus) > 0:
                return gpus[self.args.device_id]
            else:
                self.logger.warning('in your machine, it does not have GPU(s), back to CPU')

        return tf.config.experimental.list_physical_devices(device_type='CPU')

    @property
    def request(self) -> bert2tf_pb2.Request:
        return self._request

    @property
    def request_type(self) -> str:
        return self._request.__class__.__name__
