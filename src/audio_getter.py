from os import path

from .audio_mp3_file_handler import Mp3FileHandler
from .audio_ogg_file_handler import OggFileHandler
from .dir_manager import DIR_MANAGER
from .extension_manager import get_file_extension


def get_file_manager(filename):
    """
    return the correct handler for the file
    input : a file (string), a directory (string)
    output : an Handler or None
    """

    ext = get_file_extension(filename)
    if ext == "mp3":
        return Mp3FileHandler(path.join(DIR_MANAGER.directory, filename))
    elif ext == "ogg":
        return OggFileHandler(path.join(DIR_MANAGER.directory, filename))
    else:
        return None
