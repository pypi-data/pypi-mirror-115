import os
import sys


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
