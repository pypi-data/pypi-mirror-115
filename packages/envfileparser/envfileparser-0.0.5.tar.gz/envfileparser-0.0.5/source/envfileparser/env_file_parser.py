import os
import sys

from .type_checker import is_int

__all__ = ['get_env', 'get_envs']


def read_env(file_path):
    try:
        if not os.path.isabs(file_path):
            if sys.platform == "win32":
                file_path = os.path.abspath(os.getcwd() + '/' + file_path)
            else:
                file_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), file_path))
        with open(file_path, 'r') as env_file:
            env_file_lines = env_file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"The {file_path} not found!")
    return env_file_lines


def parse_env(env_file_lines):
    env_vars = {}
    for line in env_file_lines:
        equal_index = line.index('=')
        value = line[equal_index + 1::].strip()
        if is_int(value):
            value = int(value)
        elif value[0] == value[-1] and value[0] in ('''"''', """'"""):
            value = value[1:len(value) - 1]
        key = line[0:equal_index].strip()
        env_vars[key] = value
    return env_vars


def get_env(var_name: str, file_path=".env"):
    env_file_lines = read_env(file_path)
    env_vars = parse_env(env_file_lines)
    try:
        var = env_vars[var_name]
    except KeyError:
        raise KeyError(f"{var_name} is not found in {file_path}.")
    return var


def get_envs(*var_names: str, file_path=".env"):
    var_list = []
    env_file_lines = read_env(file_path)
    env_vars = parse_env(env_file_lines)
    try:
        var = None
        for name in var_names:
            var = env_vars[name]
            var_list.append(var)
    except KeyError:
        raise KeyError(f"{var} is not found in {file_path}.")
    return var_list


if __name__ == "__main__":
    pass
