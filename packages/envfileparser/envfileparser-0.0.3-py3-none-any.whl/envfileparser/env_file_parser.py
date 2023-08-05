import os
import sys
from .type_checker import is_int

__all__ = ['get_env']


def get_env(const_name, file_path=".env"):
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), file_path))
        with open(file_path, 'r') as env_file:
            env_file_lines = env_file.readlines()
    except FileNotFoundError:
        print(f"dotenv: The {file_path} not found.")
        sys.exit(1)

    env_consts = {}

    for line in env_file_lines:
        equal_index = line.index('=')
        value = line[equal_index + 1::].strip()
        if is_int(value):
            value = int(value)
        elif value[0] == value[-1] and value[0] in ('''"''', """'"""):
            value = value[1:len(value) - 1]
        key = line[0:equal_index].strip()
        env_consts[key] = value
    try:
        config_var = env_consts[const_name]
    except KeyError:
        print(f"dotenv: The constant you specified is not contained in the {file_path}.")
        sys.exit(1)
    return config_var


if __name__ == "__main__":
    print("This is python config file parser by Kirill Lapushinskiy.")
