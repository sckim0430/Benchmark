"""The check file implementation.
"""
def check_cfg(model_cfg, data_cfg, env_cfg, mode=True):
    """The operation for check the config.

    Args:
        model_cfg (dict): The model config.
        data_cfg (dict): The data config.
        env_cfg (dict): The environment config.
        mode (bool, optional): The check mode option. if mode = true then train else test.

    Raises:
        ValueError: If the key doesn't exist.
    """
    #model_cfg check
    print('Check the model config file.')
    exist_check(["model", "params", "optimizer"], model_cfg)
    exist_check(["type"], model_cfg['model'])
    exist_check(["type"], model_cfg['optimizer'])
    exist_check(["evaluation", "loss"], model_cfg['params'])
    exist_check(["train", "validation", "test"],
                model_cfg['params']['evaluation'])

    for k in model_cfg['model'].keys():
        if k == "type":
            continue

        exist_check("type", model_cfg['model'][k])

    print('done.')

    #data_cfg check
    print('Check the data config file.')

    if mode:
        #train check mode
        exist_check(["dummy", "batch_size", "epochs", "resume", "weight_dir"], data_cfg)

        if data_cfg['resume'] is not None and "start_epoch" not in data_cfg:
            raise ValueError('The start_epoch option must be in data config when resume is not None.')

        if not data_cfg['dummy'] and "train_dir" not in data_cfg:
            raise ValueError('The train directory must be in the config file when dummy is false.')

    else:
        #test check mode
        exist_check(["weight_load"], data_cfg)

        if not data_cfg['dummy'] and "test_dir" not in data_cfg:
            raise ValueError(
                'The test directory must be in the config file, and the directory must exist.')

    print('done.')

    #env_cfg check
    print('Check the environment config file.')

    exist_check(["seed", "workers", "multiprocessing_distributed", "distributed",
                "gpu_id", "ngpus_per_node", "world_size", "rank", "dist_url", "dist_backend"], env_cfg)

    print('done.')

def exist_check(*keys, cfg):
    """The operation for check the exist.

    Args:
        *keys (list[str]): The keys.
        cfg (dict): The config.

    Raises:
        ValueError: If the key doesn't exist.
    """
    for k in keys:
        if k not in cfg:
            raise ValueError('The {} must be in config.'.format(k))

def check_cls(cls_scores, labels, num_class, multi_label=False):
    """The operation for check the classification scores and labels format.

    Args:
        cls_scores (torch.Tensor): The classification scores.
        labels (torch.Tensor): The labels.
        num_class (int): The number of class.
        multi_label (bool, optional): The multi label option. Defaults to False.

    Raises:
        ValueError: If the dimension of labels and classification scores miss match.
    """
    cls_dim = cls_scores.dim()
    labels_dim = labels.dim()

    if num_class == 2:
        if cls_dim != 1 or labels_dim != 1:
            raise ValueError(
                "The binary classification task must have 1-dimension classification scores and labels.")
    else:
        if cls_dim != 2:
            raise ValueError(
                "The multi class and label classification task must have 2-dimension classification scores.")

        if multi_label:
            if labels_dim != 2:
                raise ValueError(
                    "The multi label classification task must have 2-dimension labels.")
        else:
            if labels_dim not in (1, 2):
                raise ValueError(
                    "The multi class classification task must have 1 or 2-dimension labels.")