import argparse
import os

import grpc

from ... import __stop_msg__
from ...excepts import GRPCServerError, BadClient
from ...logging.base import get_logger
from ...proto import bert2tf_pb2_grpc


class GrpcClient:
    """
    A Base gRPC client which the other python client application can build from.

    """

    def __init__(self, args: 'argparse.Namespace'):
        self.args = args
        if not args.proxy and os.name != 'nt':
            os.unsetenv('http_proxy')
            os.unsetenv('https_proxy')
        self.logger = get_logger(self.__class__.__name__)
        self.logger.debug('setting up grpc insecure channel...')

        self._channel = grpc.insecure_channel(
            '%s:%d' % (args.host, args.grpc_port),
            options={
                'grpc.max_send_message_length': -1,
                'grpc.max_receive_message_length': -1,
            }.items(),
        )

        self.logger.debug('waiting channel to be ready...')
        try:
            grpc.channel_ready_future(self._channel).result(
                timeout=(args.timeout_ready / 1000) if args.timeout_ready > 0 else None)
        except grpc.FutureTimeoutError:
            self.logger.critical('can not connect to the server at %s:%d after %d ms, please double check the '
                                 'ip and grpc port number of the server'
                                 % (args.host, args.grpc_port, args.timeout_ready))
            raise GRPCServerError('can not connect to the server at %s:%d' % (args.host, args.grpc_port))

        self.logger.debug('create new stub...')
        self._stub = bert2tf_pb2_grpc.Bert2tfRPCStub(self._channel)

        # attache response handler
        self.logger.success('connected to the gateway at %s:%d!' % (self.args.host, self.args.grpc_port))
        self.is_closed = False

    def call(self, *args, **kwargs):
        """Calling the gRPC server """
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self, *args, **kwargs):
        """Wrapping :meth:`call` and provide exception captures
        """

        try:
            self.call(*args, **kwargs)
        except KeyboardInterrupt:
            self.logger.warning('user cancel the process')
        # Since this object is guaranteed to be a grpc.Call,
        # might as well include that in its name.
        except grpc.RpcError as rpc_error_call:
            my_code = rpc_error_call.code()
            my_details = rpc_error_call.details()
            if my_code == grpc.StatusCode.UNAVAILABLE:
                self.logger.error('the ongoing request is terminated as the server is not available or closed already')
            elif my_code == grpc.StatusCode.INTERNAL:
                self.logger.error('internal error on the server side')
            else:
                raise BadClient('%s error in grpc: %s '
                                'often the case is that you define/send a bad request to bert2tf, '
                                'please double check your request' % (my_code, my_details))
        finally:
            self.close()

        return self

    def close(self):
        """Gracefully shutdown the client and release all gRPC-related resources """
        if not self.is_closed:
            self._channel.close()
            self.logger.success(__stop_msg__)
            self.is_closed = True
