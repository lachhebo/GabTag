from .audiobasics import AudioBasics
from mutagen.mp3 import EasyMP3, MP3
from mutagen.id3 import ID3, APIC, TRCK, USLT, TIT2, TALB, TPE1, TCON, TYER
from PIL import Image
import io

class MP3Handler(AudioBasics):

    def __init__(self,path_file):
        '''
        We initialise :
         the path of the file
         the tagging tool we use
        '''
        self.path_file = path_file
        self.audio = MP3(path_file)
        self.id3 = self.audio.tags


    def getTag(self,tag_key):
        if tag_key == "title" :
            title_tag = self.id3.getall('TIT2')
            if len(title_tag)>0:
                return title_tag[0].text[0]
            else:
                return ""

        elif tag_key == "cover":
            cover_tag = self.id3.getall('APIC')

            if len(cover_tag)>0 :
                return cover_tag[0].data
            else:
                return ""

        elif tag_key == "album":
            album_tag = self.id3.getall('TALB')
            if len(album_tag)>0:
                return album_tag[0].text[0]
            else:
                return ""

        elif tag_key == "artist":

            artist_tag = self.id3.getall('TPE1')
            if len(artist_tag)>0:
                return artist_tag[0].text[0]
            else:
                return ""

        elif tag_key == "genre":

            genre_tag = self.id3.getall('TCON')
            if len(genre_tag)>0:
                return genre_tag[0].text[0]
            else:
                return ""


        elif tag_key == "track":

            track_tag = self.id3.getall('TRCK')
            if len(track_tag)>0:
                print("TRACK :",track_tag)
                return track_tag[0].text[0] #text 6/16
            else:
                return ""

        elif tag_key == "year":
            year_tag = self.id3.getall('TYER')
            if len(year_tag)>0:
                print("YEAR :", year_tag)
                return year_tag[0].text[0]
            else:
                return ""




    def get_extension_mime(self, filename):
         namelist = filename.split('/')
         return namelist[-1]



    def check_tag_existence(self,key):
        if key != "title":
            tag = self.id3.getall('TIT2')
            return len(tag)>0
        elif key == "cover" :
            tag = self.id3.getall('APIC')
            return len(cover_tag)>0
        elif key == "album":
            tag = self.id3.getall('TALB')
            return len(cover_tag)>0
        elif key == "artist":
            tag = self.id3.getall('TPE1')
            return len(cover_tag)>0
        elif key == "genre":
            tag = self.id3.getall('TCON')
            return len(cover_tag)>0
        elif key == "track_number":
            tag = self.id3.getall('TRCK')
            return len(cover_tag)>0
        elif key == "year":
            tag = self.id3.getall('TYER')
            return len(cover_tag)>0



    def setTag(self,tag_key,tag_value): #TODO

        if tag_key == "cover":
            extension_image  = self.get_extension_image(tag_value)

            self.id3.delall('APIC')

            self.id3.add(
                APIC(
                    encoding = 3,  # UTF-8
                    mime= extension_image,   # '/image/png'
                    type= 3,  # 3 is for album art
                    desc='Cover',
                    data= open(tag_value, 'rb').read()      #img.read()  # Reads and adds album art
                )
            )
        elif tag_key == "title":
            self.id3.delall("TIT2")
            self.id3.add(TIT2(encoding=3, text=tag_value))
        elif tag_key == "album":
            self.id3.delall('TALB')
            self.id3.add(TALB(encoding=3, text=tag_value))
        elif tag_key == "artist":
            self.id3.delall('TPE1')
            self.id3.add(TPE1(encoding=3, text=tag_value))
        elif tag_key == "genre":
            self.id3.delall('TCON')
            self.id3.add(TCON(encoding=3, text=tag_value))
        elif tag_key == "track_number":
            self.id3.delall('TRCK')
            self.id3.add(TRCK(encoding=3, text=tag_value))
        elif tag_key == "year":
            self.id3.delall('TRCK')
            self.id3.add(TYER(encoding=3, text=tag_value))


    def get_extension_image(self, filename):

         namelist = filename.split('.')
         return "/image/" + namelist[-1]


    def savemodif(self):
        self.id3.save(self.path_file)


    
