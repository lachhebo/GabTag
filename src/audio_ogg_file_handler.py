import base64
import mutagen.flac
from typing import Dict
from mutagen.flac import Picture
from mutagen.id3 import ID3, TIT2, APIC, TALB, TPE1  # noqa:F401
from mutagen.id3 import TCON, TRCK, TDRC, USLT  # noqa:F401
from mutagen.oggvorbis import OggVorbis, OggVCommentDict

from .audio_extension_handler import AudioExtensionHandler
from .tools import file_size_to_string
from .tools import music_length_to_string

TAG_PARAMS = {
    "title": "TITLE",
    "cover": "METADATA_BLOCK_PICTURE",
    "album": "ALBUM",
    "artist": "ARTIST",
    "genre": "GENRE",
    "track": "TRACKNUMBER",
    "year": "DATE",
}


class OggFileHandler(AudioExtensionHandler):

    @staticmethod
    def get_extension():
        return ".ogg"

    def __init__(self, path_file):
        """
        We initialise the path of the file and the tagging tool we use
        """
        self.path_file = path_file
        self.audio = OggVorbis(path_file)
        self.id3 = self.audio.tags

        if self.id3 is None:
            self.audio.add_tags()
            self.id3 = self.audio.tags

    def get_one_tag(self, id3_name_tag: str, data_type: str):
        """
        A function to return the first tag of an id3 label
        """
        if self.id3 is None:
            return ""

        if self.id3 is OggVCommentDict:
            return self.id3.get(id3_name_tag)

        tag_needed = self.id3.get(id3_name_tag, "")

        if len(tag_needed) == 0:
            return ""

        if data_type == "text":
            return tag_needed[0]
        elif data_type == "data":
            try:
                return base64.b64decode(tag_needed[0])
            except (TypeError, ValueError):
                return ""
        else:
            return ""

    def get_tag_research(self):
        return [
            self.get_one_tag(TAG_PARAMS["title"], "text"),
            self.get_one_tag(TAG_PARAMS["artist"], "text"),
            self.get_one_tag(TAG_PARAMS["album"], "text"),
        ]

    def get_tag(self, tag_key):
        """
        We handle tag using a switch, it is working well because it
        is basically the structure.
        """

        if tag_key == "cover":
            cover_bytes = self.get_one_tag("METADATA_BLOCK_PICTURE", "data")
            if cover_bytes == "":
                return ""
            try:
                picture = Picture(cover_bytes)
                return picture.data
            except mutagen.flac.error:
                return ""
        elif tag_key == "size":
            return file_size_to_string(self.path_file)
        elif tag_key == "length":
            return music_length_to_string(self.audio.info.length)
        else:
            return self.get_one_tag(TAG_PARAMS[tag_key], "text")

    def get_tags(self) -> Dict:
        tags = [
            "title",
            "album",
            "artist",
            "genre",
            "cover",
            "year",
            "track",
            "length",
            "size",
        ]
        result = {}
        for tag in tags:
            result[tag] = self.get_tag(tag)
        return result

    def check_tag_existence(self, key):
        return len(self.id3.get(TAG_PARAMS[key])) > 0

    def set_tag(self, tag_key, tag_value):

        if tag_key != "cover":
            self.id3[TAG_PARAMS[tag_key]] = [tag_value]
            return 1

        if tag_value == "":
            return 0

        if isinstance(tag_value, str):
            tag_value = open(tag_value, "rb").read()
        picture = Picture()
        picture.data = tag_value
        binary_data = picture.write()
        self.id3[TAG_PARAMS[tag_key]] = [base64.b64encode(binary_data).decode("ascii")]

    def save_modifications(self):
        """
        Save definitively the modification we have made.
        """
        self.audio.save()
