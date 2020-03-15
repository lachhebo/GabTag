from os import path

from .audio_mp3_file_handler import Mp3FileHandler
from .tools import get_file_extension

EXTENSIONS = ['mp3']


def check_extension(filename):
    """
    Check if the file extension is handled by Gabtag
    input : a filename (string)
    output : a bool
    """

    extension = get_file_extension(filename)

    if extension in EXTENSIONS:
        return True
    else:
        return False


def get_file(filename, directory):
    """
    return the correct handler for the file
    input : a file (string), a directory (string)
    output : an Handler or None
    """

    if get_file_extension(filename) == "mp3":
        return Mp3FileHandler(path.join(directory, filename))
    else:
        return None
