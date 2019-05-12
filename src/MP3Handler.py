from .audiobasics import AudioBasics
from mutagen.mp3 import EasyMP3, MP3
from mutagen.id3 import ID3, APIC, TRCK, USLT
from PIL import Image
import io

class MP3Handler(AudioBasics):

    def __init__(self,adress):
        self.adress = adress
        self.audio_easy = EasyMP3(adress)
        self.audio_cover = MP3(adress,ID3=ID3)
        self.tags = self.audio_easy.tags


    def getTag(self,tag_key): #TODO
        if tag_key != "cover" :
            if tag_key in self.tags:
                #print("GETTAG : ", self.tags[tag_key][0])
                return self.tags[tag_key][0]
            else :
                return ""
        else :
            id3 = ID3(self.adress)
            cover_tag = id3.getall('APIC')

            #print("COVERTAG :",cover_tag)

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
            id3 = ID3(self.adress)
            cover_tag = id3.getall('APIC')
            return len(cover_tag)>0


    def setTag(self,tag_key,tag_value): #TODO

        if tag_key == "cover":
            extension_image  = self.get_extension_image(tag_value)

           # img = Image.open(tag_value)

            #glibbytes = GLib.Bytes.new(img.tobytes())


            #imagedata = open(tag_value, 'rb').read()
            self.audio_cover.tags

            # id3 = ID3(tag_value)

            # if id3.getall('APIC'):
            #     id3.delall('APIC')

            self.audio_cover.tags.add(
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
        self.audio_cover.tags.save(self.adress)


    
