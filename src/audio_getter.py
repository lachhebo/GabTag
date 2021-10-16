from os import path

from .audio_mp3_file_handler import Mp3FileHandler
from .dir_manager import DIR_MANAGER
from .extension_manager import get_file_extension


def get_file_manager(filename):
    """
    return the correct handler for the file
    input : a file (string), a directory (string)
    output : an Handler or None
    """

    if get_file_extension(filename) == "mp3":
        return Mp3FileHandler(path.join(DIR_MANAGER.directory, filename))
    else:
        return None
