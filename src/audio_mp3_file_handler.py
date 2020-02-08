import os

from mutagen.id3 import ID3, APIC, TRCK, USLT, TIT2, TALB, TPE1, TCON, TDRC
from mutagen.mp3 import MP3

from .audio_extension_handler import AudioExtensionHandler
from .tools import get_extension_image


class Mp3FileHandler(AudioExtensionHandler):
    """
    This function treat MP3 tags, There is no reference of MP3 in the code elsewhere,
    to handle a new file type, implement a similar class who is the children of AudioBasics
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
                if data_type == 'text':
                    return tag_needed[0].text[0]
                elif data_type == 'data':
                    return tag_needed[0].data
            else:
                return ""
        else:
            return ""

    def get_tag_research(self):
        return [
            self.get_one_tag('TIT2', 'text'),
            self.get_one_tag('TPE1', 'text'),
            self.get_one_tag('TALB', 'text')
        ]

    def get_tag(self, tag_key):
        """
        We handle tag using a switch, it is working well because it is basically the structure.
        """
        if tag_key == 'title':
            return self.get_one_tag('TIT2', 'text')
        elif tag_key == 'cover':
            return self.get_one_tag('APIC', 'data')
        elif tag_key == 'album':
            return self.get_one_tag('TALB', 'text')
        elif tag_key == 'artist':
            return self.get_one_tag('TPE1', 'text')
        elif tag_key == 'genre':
            return self.get_one_tag('TCON', 'text')
        elif tag_key == 'track':
            return self.get_one_tag('TRCK', 'text')
        elif tag_key == 'lyrics':
            if self.id3 is not None:
                tag_needed = self.id3.getall('USLT')
                if len(tag_needed) > 0:
                    return tag_needed[0].text
                else:
                    return ''
            else:
                return ''

        elif tag_key == 'year':
            return str(self.get_one_tag('TDRC', 'text'))

        # NOT tags but file information
        elif tag_key == 'size':
            return str(round(os.path.getsize(self.path_file) / 1000000, 1)) + ' Mb'
        elif tag_key == 'length':
            return str(int(self.audio.info.length / 60)) + ' minutes ' + str(
                int(self.audio.info.length % 60)) + ' seconds'

    def check_tag_existence(self, key):
        """ Every thing is in the title"""
        if key != 'title':
            tag_title = self.id3.getall('TIT2')
            return len(tag_title) > 0
        elif key == 'cover':
            tag_cover = self.id3.getall('APIC')
            return len(tag_cover) > 0
        elif key == 'album':
            tag_album = self.id3.getall('TALB')
            return len(tag_album) > 0
        elif key == 'artist':
            tag_artist = self.id3.getall('TPE1')
            return len(tag_artist) > 0
        elif key == 'genre':
            tag_genre = self.id3.getall('TCON')
            return len(tag_genre) > 0
        elif key == 'track':
            tag_track = self.id3.getall('TRCK')
            return len(tag_track) > 0
        elif key == 'year':
            tag_year = self.id3.getall('TDRC')
            return len(tag_year) > 0
        elif key == 'lyrics':
            tag_lyrics = self.id3.getall('USLT')
            return len(tag_lyrics) > 0

    def set_tag(self, tag_key, tag_value):

        if tag_key == 'cover':

            self.id3.delall('APIC')

            if tag_value == '':
                pass
            elif type(tag_value) == bytes:
                self.id3.add(
                    APIC(
                        encoding=3,  # UTF-8
                        mime='/image/png',  # '/image/png'
                        type=3,  # 3 is for album art
                        desc='Cover',
                        data=tag_value
                    )
                )
            else:
                extension_image = get_extension_image(tag_value)
                self.id3.add(
                    APIC(
                        encoding=3,  # UTF-8
                        mime=extension_image,  # '/image/png'
                        type=3,  # 3 is for album art
                        desc='Cover',
                        data=open(tag_value, 'rb').read()
                    )
                )

        elif tag_key == 'title':
            self.id3.delall('TIT2')
            self.id3.add(TIT2(encoding=3, text=tag_value))
        elif tag_key == 'album':
            self.id3.delall('TALB')
            self.id3.add(TALB(encoding=3, text=tag_value))
        elif tag_key == 'artist':
            self.id3.delall('TPE1')
            self.id3.add(TPE1(encoding=3, text=tag_value))
        elif tag_key == 'genre':
            self.id3.delall('TCON')
            self.id3.add(TCON(encoding=3, text=tag_value))
        elif tag_key == 'track':
            self.id3.delall('TRCK')
            self.id3.add(TRCK(encoding=3, text=tag_value))
        elif tag_key == 'year':
            self.id3.delall('TDRC')
            self.id3.add(TDRC(encoding=3, text=tag_value))
        elif tag_key == 'lyrics':
            self.id3.delall('USLT')
            self.id3.add(USLT(encoding=3, text=tag_value))
        else:
            # print('NO_TAG', tag_key)
            pass

    def save_modifications(self):
        """
        Save definitively the modification we have made.
        """
        self.id3.save(self.path_file)
