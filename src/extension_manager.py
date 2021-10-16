from .constant import HANDLED_EXTENSIONS


def get_file_extension(filename):
    """
    return the file extension.
    """
    namelist = filename.split(".")
    return namelist[-1]


def is_extension_managed(filename):
    """
    Check if the file extension is handled by Gabtag
    input : a filename (string)
    output : a bool
    """

    extension = get_file_extension(filename)

    if extension in HANDLED_EXTENSIONS:
        return True
    else:
        return False
