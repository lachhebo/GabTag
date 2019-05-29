import musicbrainzngs as mb
from os import walk
from .moteur import Moteur


class Data_Scrapper :


    class __Data_Scrapper :


        def __init__(self):
            mb.set_useragent("GabTag", version = "1.0.5", contact = "ismael.lachheb@protonmail.com")
            self.tag_finder = {}


        def getTags(self,directory):
            filelist = []
            for (dirpath, dirnames, filenames) in walk(directory):
                filelist.extend(filenames)
                break

            for namefile in filelist:
                if Moteur().check_extension(namefile) :
                    mzquery = self.remove_extension(namefile)
                    self.tag_finder[namefile] = mb.search_recordings(query = mzquery,limit=1)

        def get_one_tag(self,namefile):
            if namefile in self.tag_finder :
                return self.tag_finder[namefile]
            else :
                return None


        def remove_extension(self, filename):
            '''
            return the filename without the extension
            '''
            namelist = filename.split('.')
            return namelist[0]



    
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if Data_Scrapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Data_Scrapper.__instance = Data_Scrapper.__Data_Scrapper()


    @staticmethod
    def getInstance():
        """ Static access method. """
        if Data_Scrapper.__instance == None:
            Data_Scrapper()
        return Data_Scrapper.__instance
