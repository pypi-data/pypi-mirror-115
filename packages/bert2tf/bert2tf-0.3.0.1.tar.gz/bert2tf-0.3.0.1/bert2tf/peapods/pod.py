import copy
from argparse import Namespace
from contextlib import ExitStack
from typing import Dict, Optional, Union, List, Callable

from .head_pea import HeadPea
from .pea import BasePea
from .tail_pea import TailPea
from ..enums import SocketType, PeaRoleType
from ..helper import random_port, get_random_identity, get_parsed_args
from ..parser import set_pod_parser, set_gateway_parser


class BasePod(ExitStack):
    def __init__(self, args: Namespace):
        super().__init__()
        self.peas = []
        self._args = args
        self.peas_args = self._parse_args(args)

    def _parse_args(self, args: Namespace) -> Dict[str, Optional[Union[List[Namespace], Namespace]]]:
        peas_args = {
            'head': None,
            'tail': None,
            'peas': []
        }

        if getattr(args, 'parallel', 1) > 1:
            peas_args['head'] = _copy_to_head_args(args)
            peas_args['tail'] = _copy_to_tail_args(args)
            peas_args['peas'] = _set_pea_args(args, peas_args['head'], peas_args['tail'])

        else:
            args.role = PeaRoleType.SINGLETON
            args.socket_out = SocketType.PUB_BIND
            peas_args['peas'] = [args]

        return peas_args

    @property
    def head_args(self) -> Namespace:
        if self.peas_args['head']:
            return self.peas_args['head']
        else:
            return self.peas_args['peas'][0]

    @property
    def tail_args(self) -> Namespace:
        if self.peas_args['tail']:
            return self.peas_args['tail']
        else:
            return self.peas_args['peas'][0]

    @property
    def all_args(self) -> List[Namespace]:
        return self.peas_args['peas']

    def start(self) -> 'FLowPod':
        if self.peas_args['head']:
            pea = HeadPea(self.peas_args['head'])
            self.peas.append(pea)
            self.enter_context(pea)

        if self.peas_args['tail']:
            pea = TailPea(self.peas_args['tail'])
            self.peas.append(pea)
            self.enter_context(pea)

        for idx, args in enumerate(self.peas_args['peas']):
            args.replicas_id = idx
            pea = BasePea(args)
            self.peas.append(pea)
            self.enter_context(pea)

        return self

    def __enter__(self):
        return self.start()


class FLowPod(BasePod):
    def __init__(self, kwargs: Dict, parser: Callable = set_pod_parser):
        _parser = parser()
        self.cli_args, self._args, self.unk_args = get_parsed_args(kwargs, _parser, 'FlowPod')
        super().__init__(self._args)


class GatewayPod(BasePod):
    def start(self):
        from .gateway import RESTGatewayPea, GatewayPea
        gateway_pea_args = self.all_args[0]

        gateway_pea_args.socket_in = SocketType.SUB_CONNECT
        gateway_pea_args.socket_out = SocketType.PUSH_CONNECT

        gateway_pea_args.name = 'gateway'
        gateway = GatewayPea(gateway_pea_args)
        self.peas.append(gateway)
        self.enter_context(gateway)

        if gateway_pea_args.rest_api:
            rest_gateway_pea_args = copy.deepcopy(gateway_pea_args)
            rest_gateway_pea_args.name = 'RESTGateway'
            rest_gateway = RESTGatewayPea(rest_gateway_pea_args)
            self.peas.append(rest_gateway)
            self.enter_context(rest_gateway)

        return self


class GatewayFlowPod(GatewayPod, FLowPod):
    def __init__(self, kwargs: Dict):
        FLowPod.__init__(self, kwargs, parser=set_gateway_parser)


def _copy_to_head_args(args: Namespace) -> Namespace:
    _args = copy.deepcopy(args)
    _args.port_out = random_port()
    _args.port_ctrl = random_port()
    _args.socket_out = SocketType.ROUTER_BIND
    _args.role = PeaRoleType.HEAD
    _args.yaml_path = '_route'

    return _args


def _copy_to_tail_args(args: Namespace) -> Namespace:
    _args = copy.deepcopy(args)
    _args.port_in = random_port()
    _args.port_ctrl = random_port()
    _args.role = PeaRoleType.TAIL
    _args.socket_out = SocketType.PUB_BIND
    _args.yaml_path = '_forward'

    return _args


def _set_pea_args(args: Namespace, head_args: Namespace, tail_args: Namespace) -> List[Namespace]:
    pea_args = []
    for idx in range(args.parallel):
        _args = copy.deepcopy(args)
        _args.identity = get_random_identity()
        _args.port_in = head_args.port_out
        _args.port_out = tail_args.port_in
        _args.port_ctrl = random_port()
        _args.socket_in = SocketType.DEALER_CONNECT
        _args.socket_out = SocketType.PUSH_CONNECT
        _args.role = PeaRoleType.REPLICA
        _args.replicas_id = idx
        pea_args.append(_args)

    return pea_args
