from mutagen.id3 import ID3, TIT2, APIC, TALB, TPE1  # noqa:F401
from mutagen.id3 import TCON, TRCK, TDRC, USLT  # noqa:F401
from mutagen.mp3 import MP3

from .audio_extension_handler import AudioExtensionHandler
from .tools import get_extension_image, music_length_to_string
from .tools import file_size_to_string

TAG_PARAMS = {
    "title": "TIT2",
    "cover": "APIC",
    "album": "TALB",
    "artist": "TPE1",
    "genre": "TCON",
    "track": "TRCK",
    "year": "TDRC",
}


class Mp3FileHandler(AudioExtensionHandler):
    """
    This function treat MP3 tags, There is no reference of MP3 in the
    code elsewhere, to handle a new file type, implement a similar class
    who is the children of AudioBasics.
    """

    @staticmethod
    def get_extension():
        return ".mp3"

    def __init__(self, path_file):
        """
        We initialise the path of the file and the tagging tool we use
        """
        self.path_file = path_file
        self.audio = MP3(path_file)
        self.id3 = self.audio.tags

        if self.id3 is None:
            self.audio.tags = ID3()
            self.id3 = self.audio.tags

    def get_one_tag(self, id3_name_tag, data_type):
        """
        A function to return the first tag of an id3 label
        """
        if self.id3 is not None:
            tag_needed = self.id3.getall(id3_name_tag)
            if len(tag_needed) > 0:
                if data_type == "text":
                    return tag_needed[0].text[0]
                elif data_type == "data":
                    return tag_needed[0].data
            else:
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
            return self.get_one_tag("APIC", "data")
        elif tag_key == "year":
            return str(self.get_one_tag("TDRC", "text"))
        elif tag_key == "size":
            return file_size_to_string(self.path_file)
        elif tag_key == "length":
            return music_length_to_string(self.audio.info.length)
        else:
            return self.get_one_tag(TAG_PARAMS[tag_key], "text")

    def get_tags(self):
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
        """Every thing is in the title"""
        return len(self.id3.getall(TAG_PARAMS[key])) > 0

    def set_tag(self, tag_key, tag_value):

        if tag_key == "cover":

            self.id3.delall("APIC")

            if tag_value == "":
                pass
            elif type(tag_value) == bytes:
                self.id3.add(
                    APIC(
                        encoding=3,  # UTF-8
                        mime="/image/png",  # '/image/png'
                        type=3,  # 3 is for album art
                        desc="Cover",
                        data=tag_value,
                    )
                )
            else:
                extension_image = get_extension_image(tag_value)
                self.id3.add(
                    APIC(
                        encoding=3,  # UTF-8
                        mime=extension_image,  # '/image/png'
                        type=3,  # 3 is for album art
                        desc="Cover",
                        data=open(tag_value, "rb").read(),
                    )
                )
        else:
            self.id3.delall(TAG_PARAMS[tag_key])
            self.id3.add(globals()[TAG_PARAMS[tag_key]](encoding=3, text=tag_value))

    def save_modifications(self):
        """
        Save definitively the modification we have made.
        """
        self.id3.save(self.path_file)
