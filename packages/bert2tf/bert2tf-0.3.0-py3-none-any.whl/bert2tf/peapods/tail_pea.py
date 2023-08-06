import argparse
from typing import Dict, Union

from .pea import BasePea
from ..logging.base import get_logger


class TailPea(BasePea):
    """the tail pea of the pod"""

    def __init__(self, args: Union['argparse.Namespace', Dict]):
        super().__init__(args)

        if args.name and args.name != self.__class__.__name__.lower():
            self.name = f'{args.name}-tail'
            self.logger = get_logger(self.name)
            args.name = self.name

        self.is_tail_router = True
