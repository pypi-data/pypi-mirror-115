from .parse_env import parse_env
from .read_env import read_env


def get_env(var_name: str, file_path=".env") -> str:
    """A function that returns value of the specified variables as a string.

    The var name is passed to the function as a string.
    and a named parameter - the path to the file with a default value.
    String value of found variable is returned - otherwise an exception is thrown.

    :param var_name: name of extracted variable
    :param file_path: the string is the path to the file, it has a default value
    :return: value of extracted var as a string
    """
    env_file_lines = read_env(file_path)
    env_vars = parse_env(env_file_lines)

    try:
        var = env_vars[var_name]
    except KeyError:
        raise KeyError(f"{var_name} is not found in {file_path}.")

    return var
