from os import path

from .audio_mp3_file_handler import Mp3FileHandler
from .audio_ogg_file_handler import OggFileHandler
from .extension_manager import get_file_extension


def get_file_manager(filename, directory):
    """
    return the correct handler for the file
    input : a file (string), a directory (string)
    output : an Handler or None
    """

    ext = get_file_extension(filename)
    if ext == "mp3":
        # print("read mp3: ",filename)
        return Mp3FileHandler(path.join(directory, filename))
    elif ext == "ogg":
        return OggFileHandler(path.join(directory, filename))
    else:
        return None
