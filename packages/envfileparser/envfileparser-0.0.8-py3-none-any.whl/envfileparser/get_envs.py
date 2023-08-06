from .parse_env import parse_env
from .read_env import read_env


def get_envs(*var_names: str, file_path=".env") -> list:
    """A function that returns a list of the values of the specified variables.

    The var names are passed to the function as a sequence
    and a named parameter - the path to the file with a default value.
    A list of values of all the specified variables is
    returned - otherwise an exception is thrown.

    :param var_names: list of names of extracted variables
    :param file_path: the string is the path to the file, it has a default value
    :return: list of values of extracted variables
    """
    var_list = []
    env_file_lines = read_env(file_path)
    env_vars = parse_env(env_file_lines)
    var_from_line = None

    try:
        for name in var_names:
            var_from_line = env_vars[name]
            var_list.append(var_from_line)
    except KeyError:
        raise KeyError(f"{var_from_line} is not found in {file_path}.")

    return var_list
