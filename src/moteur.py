from .MP3Handler import MP3Handler
from os import path


class Moteur:

    def __init__(self):
        '''
        the list of extensions handled by Gabtag
        '''
        self.extensions = ["mp3"]

    def check_extension(self, filename):
        '''
        Check if the file extension is handled by Gabtag
        input : a filename (string)
        output : a bool
        '''

        extension = self.get_extension(filename)

        if extension in self.extensions:
            return True
        else:
            return False

    def getFile(self, filename, directory):
        '''
        return the correct handler for the file
        input : a file (string), a directory (string)
        ouput : an Handler or None
        '''

        if self.get_extension(filename) == "mp3":
            return MP3Handler(path.join(directory, filename))
        else:
            return None

    def get_extension(self, filename):
        '''
        return the file extension.
        '''
        namelist = filename.split('.')
        return namelist[-1]
