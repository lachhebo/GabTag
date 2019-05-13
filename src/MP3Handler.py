from .audiobasics import AudioBasics
from mutagen.mp3 import EasyMP3, MP3
from mutagen.id3 import ID3, APIC, TRCK, USLT
from PIL import Image
import io

class MP3Handler(AudioBasics):

    def __init__(self,adress):
        self.adress = adress
        self.audio = EasyMP3(adress)
        self.id3 = ID3(adress)
        self.tags = self.audio.tags


    def getTag(self,tag_key):
        if tag_key != "cover" :
            if tag_key in self.tags:
                #print("GETTAG : ", self.tags[tag_key][0])
                return self.tags[tag_key][0]
            else :
                return ""
        else :
            #id3 = ID3(self.adress)
            cover_tag = self.id3.getall('APIC')

            if len(cover_tag)>0 :
                return cover_tag[0].data
            else:
                return None


    def get_extension_mime(self, filename):

         namelist = filename.split('/')
         return namelist[-1]



    def check_tag_existence(self,key):
        if key != "cover":
            return key in self.tags
        else :
            #id3 = ID3(self.adress)
            cover_tag = self.id3.getall('APIC')
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
        else :
            self.tags[tag_key] = tag_value


    def get_extension_image(self, filename):

         namelist = filename.split('.')
         return "/image/" + namelist[-1]


    def savemodif(self):
        self.tags.save(self.adress)
        self.id3.save(self.adress)


    
