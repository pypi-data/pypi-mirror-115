# -*- coding: utf-8 -*-
"""SSH YAML Configuration

NAME - SSH YAML Configuration
AUTHOR - Patryk Adamczyk <patrykadamczyk@paipweb.com>
LICENSE - MIT
"""
# Imports

from sshyc import __version__
import os
import yaml
from typing import Dict

# Underscore Variables

"""Author of the module"""
__author__ = 'Patryk Adamczyk'
"""Module License"""
__license__ = 'MIT'
"""Documentation format"""
__docformat__ = 'restructuredtext en'

# Variables


debug = True

# Lib Functions


def log(level: str = None, *args) -> None:
    if level is None:
        print('SSHYC:', *args)
    elif level == "DEBUG":
        if debug:
            print('SSHYC [{0}]:'.format(level), *args)
    else:
        print('SSHYC [{0}]:'.format(level), *args)


def read_yaml(filename: str) -> dict:
    """Function to read data from yaml file
    Args:
        filename (object): File Name

    Returns:
        :obj:`str`: Returning Data from YAML file
    """
    dane = {}
    if os.path.isfile(filename):
        with open(filename, "r") as plik:
            dane = yaml.full_load(plik)
    return dane


def special_yaml_config_tags(key, value) -> Dict[str, str]:
    generic_key = str(key).lower()
    if generic_key in ('$proxy'):
        value_split = value.split(':')
        if len(value_split) >= 1:
            host = value_split[0]
            if len(value_split) >= 2:
                port = value_split[1]
            else:
                port = "22"
        else:
            log('SYNTAX_WARNING', 'Invalid $Proxy value')
            return {}
        return {
            "ProxyCommand": "ssh -q -p {0} -W %h:%p {1}".format(port, host),
        }
    return {key: value}

# Main App Function


def main() -> None:
    print("SSH YAML Configuration v.{0}".format(__version__))

    # Variables
    config_path = os.path.expanduser('~/.ssh/config')

    # Check if config files exist
    file_paths = [
        os.path.expanduser('~/.ssh/config.yaml'),
        os.path.expanduser('~/.ssh/config.yml'),
    ]
    found_path = None

    for file_path in file_paths:
        log('DEBUG', 'Checking configuration file path:', file_path)
        if os.path.isfile(file_path):
            found_path = file_path
            log('DEBUG', 'Configuration File found in:', found_path)
            break
    log('DEBUG', 'Configuration checked')
    if found_path is None:
        log('ERROR', 'Make configuration file in any of these locations:')
        for file_path in file_paths:
            log('ERROR', '   -', file_path)
        log('ERROR', 'and run tool again')
        return

    configuration = read_yaml(found_path)

    if configuration is None:
        log('ERROR', 'Configuration file in', found_path, 'is empty. Create configuration and run tool again')
        return

    generated_file = ""
    generated_yaml = {}

    for root_key, root_value in configuration.items():
        # all key
        if str(root_key).lower() in ('all', '*'):
            generated_yaml['*'] = {}
            if root_value is not None and isinstance(root_value, dict):
                for key, value in root_value.items():
                    generated_yaml['*'].update(special_yaml_config_tags(key, value))
            else:
                log('SYNTAX_WARNING', 'Invalid {0} value'.format(root_key))
        # hosts key
        if str(root_key).lower() in ('hosts'):
            if root_value is not None and isinstance(root_value, dict):
                for host_key, host_value in root_value.items():
                    generated_yaml[host_key] = {}
                    if root_value is not None and isinstance(host_value, dict):
                        for key, value in host_value.items():
                            generated_yaml[host_key].update(special_yaml_config_tags(key, value))
                    else:
                        log('SYNTAX_WARNING', 'Invalid {0}.{1} value'.format(root_key, host_key))
            else:
                log('SYNTAX_WARNING', 'Invalid {0} value'.format(root_key))
        # groups key
        if str(root_key).lower() in ('groups'):
            if root_value is not None and isinstance(root_value, dict):
                for group_key, group_value in root_value.items():
                    if root_value is not None and isinstance(group_value, dict):
                        for host_key, host_value in group_value.items():
                            generated_yaml[host_key] = {}
                            if root_value is not None and isinstance(host_value, dict):
                                for key, value in host_value.items():
                                    generated_yaml[host_key].update(special_yaml_config_tags(key, value))
                            else:
                                log('SYNTAX_WARNING', 'Invalid {0}.{1}.{2} value'.format(root_key, group_key, host_key))
                    else:
                        log('SYNTAX_WARNING', 'Invalid {0}.{1} value'.format(root_key, group_key))
            else:
                log('SYNTAX_WARNING', 'Invalid {0} value'.format(root_key))
        # projects key
        if str(root_key).lower() in ('projects'):
            if root_value is not None and isinstance(root_value, dict):
                for project_key, project_value in root_value.items():
                    if root_value is not None and isinstance(project_value, dict):
                        for host_key, host_value in project_value.items():
                            generated_yaml[host_key] = {}
                            if root_value is not None and isinstance(host_value, dict):
                                for key, value in host_value.items():
                                    generated_yaml[host_key].update(special_yaml_config_tags(key, value))
                            else:
                                log('SYNTAX_WARNING', 'Invalid {0}.{1}.{2} value'.format(root_key, project_key, host_key))
                    else:
                        log('SYNTAX_WARNING', 'Invalid {0}.{1} value'.format(root_key, project_key))
            else:
                log('SYNTAX_WARNING', 'Invalid {0} value'.format(root_key))
        # hosts groups key
        if str(root_key).lower() in ('host_groups', 'hosts_groups'):
            if root_value is not None and isinstance(root_value, dict):
                for group_key, group_value in root_value.items():
                    if root_value is not None and isinstance(group_value, dict):
                        for host_key, host_value in group_value.items():
                            host = "{0}.{1}".format(host_key, group_key)
                            generated_yaml[host] = {}
                            if root_value is not None and isinstance(host_value, dict):
                                for key, value in host_value.items():
                                    generated_yaml[host].update(special_yaml_config_tags(key, value))
                            else:
                                log('SYNTAX_WARNING', 'Invalid {0}.{1}.{2} value'.format(root_key, group_key, host_key))
                    else:
                        log('SYNTAX_WARNING', 'Invalid {0}.{1} value'.format(root_key, group_key))
            else:
                log('SYNTAX_WARNING', 'Invalid {0} value'.format(root_key))
    # print(yaml.dump(generated_yaml))
    # print(generated_yaml)

    padding = "     "
    eol = "\n"
    for host_name, host_config in generated_yaml.items():
        if host_config is not None and isinstance(host_config, dict):
            generated_conf = "Host {0}{1}".format(host_name, eol)
            for config_key, config_value in host_config.items():
                generated_conf += "{0}{1} {2}{3}".format(padding, config_key, config_value, eol)
            generated_file += generated_conf
        else:
            log('WARNING', 'Host {0} has empty or invalid configuration'.format(host_name))
    # print(generated_file)

    log(None, 'Generating SSH Config File')
    with open(config_path, "w") as plik:
        plik.write(generated_file)
    # f = open(file_path, 'r', encoding='utf-8')
    # log
