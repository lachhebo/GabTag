from os import path

from .audio_mp3_file_handler import Mp3FileHandler
from .tools import get_file_extension

HANDLED_EXTENSIONS = ["mp3"]


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


def get_file_manager(filename, directory):
    """
    return the correct handler for the file
    input : a file (string), a directory (string)
    output : an Handler or None
    """

    if get_file_extension(filename) == "mp3":
        return Mp3FileHandler(path.join(directory, filename))
    else:
        return None
