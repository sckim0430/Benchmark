"""The build implementation.
"""
from torch.optim import *
from torchvision.transforms import *
from torchvision.datasets import *
from torch.optim.lr_scheduler import *

from models.type import *
from models.module import *
from utils.parse import parse_type


def build(cfg, logger=None):
    """The operation for build.

    Args:
        cfg (dict): The input config.
        logger (logging.RootLogger|logging.Logger): The logger. Defaults to None.

    Returns:
        nn.Module: The sub model object.
    """
    # parse type from config
    type, params = parse_type(cfg)

    if logger is not None:
        params.update({'logger': logger})

    return eval(type)(**params if params is not None else {})


def build_model(cfg, logger=None):
    """The operation for build model.

    Args:
        cfg (dict): The input config.
        logger (logging.RootLogger|logging.Logger): The logger. Defaults to None.
    Returns:
        nn.Module: The model object.
    """
    # parse model config
    type, params = parse_type(cfg)

    # build sub modules
    for k in params:
        params.update({k: build(params[k], logger)})

    if logger is not None:
        params.update({'logger': logger})

    return eval(type)(**params if params is not None else {})


def build_optimizer(model_parameters, cfg):
    """The operation for build optimizer.

    Args:
        model_parameters (generator): The model parameters.
        cfg (dict): The input config.

    Returns:
        torch.optim: The optimizer object.
    """
    # parse optimizer config
    type, params = parse_type(cfg)
    params.update({'params': model_parameters})

    # build optimizer
    return eval(type)(**params)


def build_scheduler(optimizer, cfg):
    """The operation for build scheduler.

    Args:
        optimizer (torch.optim): The optimizer object.
        cfg (dict): The input config.

    Returns:
        torch.optim.lr_scheduler: The scheduler object.
    """
    type, params = parse_type(cfg)
    params.update({'optimizer': optimizer})

    return eval(type)(**params)


def build_param(cfg, mode='train'):
    """The operation for build parameter.

    Args:
        cfg (dict): The input config.
        mode (str, optional): The parameter about mode. Defaults to 'train'.

    Raises:
        ValueError: The mode should be in train/validation/test.

    Returns:
        dict: The output config.
    """
    if mode not in cfg['evaluation']:
        raise ValueError("The '{}' should be in config file.".format(mode))

    cfg_param = cfg.copy()
    cfg_param.update({'evaluation': cfg_param['evaluation'][mode]})

    return cfg_param


def build_pipeline(cfg, mode='train'):
    """The operation for build pipeline.

    Args:
        cfg (dict): The input config.
        mode (str, optional): The parameter about mode. Defaults to 'train'.

    Raises:
        ValueError: The mode should be in train/validation/test.

    Returns:
        torchvision.transforms.Compose: The pipeline.
    """
    if mode not in cfg:
        raise ValueError("The '{}' should be in config file.".format(mode))

    tf_list = []
    for k in cfg[mode]:
        tf_list.append(
            eval(k)(**cfg[mode][k] if cfg[mode][k] is not None else {}))

    return Compose(tf_list)


def build_dataset(dataset='ImageNet', **kwargs):
    """The operation for build dataset.

    Args:
        dataset (str, optional): The dataset name. Defaults to 'ImageNet'.

    Returns:
        torchvision.datasets: The dataset.
    """
    return eval(dataset)(**kwargs if kwargs is not None else {})
