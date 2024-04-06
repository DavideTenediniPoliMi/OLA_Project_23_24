import os.path as osp

import yaml

CONFIG_PATH = osp.join(osp.dirname(osp.abspath(__file__)))


def load_config():
    """
    Load config yaml file
    """
    return load_yaml(osp.join(CONFIG_PATH, "config.yaml"))


def load_yaml(path):
    """
    Load yaml file

    Args:
        path (str): path to yaml file
    """

    with open(path, "r") as stream:
        try:
            yaml_dict: dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return yaml_dict
