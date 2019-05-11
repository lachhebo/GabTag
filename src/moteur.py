from .MP3Handler import MP3Handler
from os import path

class Moteur:

    def __init__(self):
        self.extensions =  ["mp3"]


    def check_extension(self,filename):

        extension = self.get_extension(filename)

        if extension in self.extensions :
            return True
        else:
            return False


    def getFile(self,filename, directory):

        if self.get_extension(filename) == "mp3":
            return MP3Handler(path.join(directory,filename))
        else:
            return None

    def get_extension(self, filename):
         namelist = filename.split('.')

         return namelist[-1]



