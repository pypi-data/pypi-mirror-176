from __future__ import annotations

import atexit
import json
import logging
import logging.config
import os
import random
import shutil
from collections import OrderedDict
from collections.abc import MutableMapping
from os import PathLike as _PathLike
from typing import IO, Any, Callable, Dict, List, Optional, Tuple, Union

import accelerate
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.nn as nn
from chanfig import NestedDict

from danling.utils import catch, is_json_serializable

from .base_runner import BaseRunner
from .utils import ensure_dir, on_local_main_process, on_main_process

PathLike = Union[str, _PathLike]
File = Union[PathLike, IO]


class EpochRunner(BaseRunner):
    """
    Set up everything for running a job
    """

    epoch_begin: int
    epoch_end: int

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if "epoch_begin" not in self:
            self.epoch_begin = 0
        if "epoch_end" not in self:
            raise ValueError('"epoch_end" must be specified for EpochRunner')
