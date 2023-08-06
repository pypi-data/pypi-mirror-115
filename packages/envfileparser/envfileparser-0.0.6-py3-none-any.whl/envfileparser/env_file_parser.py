import os
import sys

__all__ = ['get_env', 'get_envs']


def read_env(file_path: str) -> list:
    """A function that reads a file with variables.

    This function is intended for use inside the package.
    As a parameter, it takes a string - the path to the file
    that will be opened in the future in a way that
    depends on the platform used. After opening the file,
    the data is read line by line and saved as a spike.
    At the end of this, the list returns to the outside.

    :param file_path: file path
    :type file_path: str
    :return: list of file lines
    """
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


def parse_env(env_file_lines: list) -> dict:
    """A function that extracts a variable from a list of strings.

    Each line from the list is divided by the first equal sign.
    The left part is taken for the variable name,
    and the right part is taken for the value.
    Empty lines, lines starting with " # " and
    lines without '=' are skipped. Comments to the
    right of the code are deleted.
    The value will always be stored as a string.

    :param env_file_lines: list of lines
    :type env_file_lines: list
    :return: dict var name - var value
    """
    env_vars = {}
    for line in env_file_lines:
        line = line.strip()
        if len(line) == 0 or line[0] == '#' or '=' not in line:
            continue

        equal_index = line.index('=')
        value = line[equal_index + 1::].strip()

        if '#' in value:
            if value[0] in ("'", '''"'''):
                if value[::-1].index(value[0]) > value.index('#'):
                    value = value[0:value.index('#')]
            else:
                value = value[0:value.index('#')]

        # Remove the quotation marks, if there are any.
        if value[0] == value[-1] and value[0] in ('''"''', """'"""):
            value = value[1:len(value) - 1]
        key = line[0:equal_index].strip()
        env_vars[key] = value

    return env_vars


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


if __name__ == "__main__":
    pass
