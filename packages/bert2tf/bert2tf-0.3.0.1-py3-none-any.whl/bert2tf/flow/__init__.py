import argparse
from contextlib import ExitStack
from typing import Dict

import ruamel

from ..helper import get_local_config_source, yaml, get_parsed_args
from ..logging.base import get_logger
from ..parser import set_flow_parser
from ..peapods.pod import FLowPod, GatewayFlowPod

from .. import __stop_msg__


class Flow(ExitStack):
    """Flow for models serving"""

    def __init__(self, args: 'argparse.Namespace' = None, **kwargs):
        super().__init__()
        self.logger = get_logger(self.__class__.__name__)
        self._update_args(args, **kwargs)
        self.gateway = None
        self.pod = None

        self.built = False

    @classmethod
    def load_config(cls, source: str):
        yaml.register_class(Flow)
        source = get_local_config_source(source)
        with open(source, 'r', encoding='utf-8') as fp:
            return yaml.load(fp)

    @classmethod
    def from_yaml(cls, constructor, node):
        """Required by :mod:`ruamel.yaml.constructor` """
        return cls._get_instance_from_yaml(constructor, node)[0]

    @classmethod
    def _get_instance_from_yaml(cls, constructor, node):
        data = ruamel.yaml.constructor.SafeConstructor.construct_mapping(
            constructor, node, deep=True)
        p = data.get('with', {}) # todo
        obj = cls(**p)

        obj.add_gateway(data.get('gateway', {}))
        obj.add_pod(data.get('pod', {}))
        return obj, data

    def add_gateway(self, args: Dict):
        self.gateway = GatewayFlowPod(args)

    def add_pod(self, args: Dict):
        self.pod = FLowPod(args)

    def _update_args(self, args: 'argparse.Namespace', **kwargs):
        _flow_parser = set_flow_parser()
        if args is None:
            _, args, _ = get_parsed_args(kwargs, _flow_parser, 'Flow')

        self.args = args
        self.gateway_args = kwargs

    def build(self):
        self.gateway.all_args[0].port_out = self.pod.head_args.port_in
        self.gateway.all_args[0].port_in = self.pod.tail_args.port_out
        self.enter_context(self.pod)
        self.enter_context(self.gateway)

        self.built = True
        self.logger.success('flow is ready for use...')

        return self

    def serving(self):
        if not self.built:
            self.build()

        try:
            while self.gateway is not None and self.pod is not None:
                continue
        except KeyboardInterrupt:
            self.close()

    def __enter__(self):
        return self.build()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.logger.success(__stop_msg__)
