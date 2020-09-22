import os

import yaml

from dbfaker.common.logger import log
from dbfaker.common.tools import check_path

__all__ = ['get_yaml', 'check_valid', 'update_settings']


def check_valid(key, value):
    if not value:
        log.e('[%s] Not Configured.Please Config in settings.yaml.' % key)
        raise ValueError
    return value


def get_yaml(yaml_file=None):
    yaml_file = check_path(yaml_file)
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f.read())


def update_settings(setting_data):
    register_setting = setting_data.get("Register")
    _global_setting = setting_data.get("global")
    for register_module in register_setting:
        for g in _global_setting:
            if g not in register_setting[register_module]:
                register_setting[register_module][g] = _global_setting[g]

    return setting_data
