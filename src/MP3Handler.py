from .audiobasics import AudioBasics
from mutagen.mp3 import EasyMP3, MP3

class MP3Handler(AudioBasics):

    def __init__(self,adress):
        self.adress = adress
        self.audio = EasyMP3(adress)
        self.tags = self.audio.tags


    def getTag(self,tag_key):
        if tag_key in self.tags:
            return self.tags[tag_key][0]
        else :
            return ""

    def check_tag_existence(self,key):
        return key in self.tags

    def setTag(self,tag_key,tag_value):
        self.tags[tag_key] = tag_value


    def savemodif(self):
        self.tags.save(self.adress)


    
