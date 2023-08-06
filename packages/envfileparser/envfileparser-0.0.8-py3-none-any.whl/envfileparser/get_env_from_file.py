from .get_env import get_env
from .get_envs import get_envs
from .parse_env import parse_env
from .read_env import read_env


def get_env_from_file(*var_names: str, file_path=".env"):
    """Unifying function.

    This function allows you to return both the value of a single
    variable as a string, and a list of values for several
    variables. In addition, if the parameter with variable names
    is left empty, the function returns a dictionary with all the
    variables from the file. If the file is empty,
    an empty dictionary is returned.

    :param var_names: tuple of names of extracted variables
    :param file_path: the string is the path to the file, it has a default value
    :return:
        for one var name - string value of var
        for zero var names - dict of all variables in file
        for for multiple var names - list of values
    """
    var_names_count = len(var_names)
    if var_names_count == 1:
        return get_env(var_names[0], file_path=file_path)
    elif var_names_count > 1:
        return get_envs(*var_names, file_path=file_path)
    else:
        env_file_lines = read_env(file_path)
        env_vars = parse_env(env_file_lines)
        return env_vars
