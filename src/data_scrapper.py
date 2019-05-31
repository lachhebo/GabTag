import musicbrainzngs as mb
from os import walk
from .moteur import Moteur


class Data_Scrapper :


    class __Data_Scrapper :


        def __init__(self):
            mb.set_useragent("GabTag", version = "1.0.5", contact = "ismael.lachheb@protonmail.com")
            self.tag_finder = {}


        def scrap_tags(self,directory,improving):
            filelist = []
            for (dirpath, dirnames, filenames) in walk(directory):
                filelist.extend(filenames)
                break

            for namefile in filelist:
                if Moteur().check_extension(namefile) :
                    mzquery = self.remove_extension(namefile)
                    if improving == 1:
                        mzquery = mzquery[0].split("-")
                    self.tag_finder[namefile] = self.reorder_data(mb.search_recordings(query = mzquery,limit=1))

        def get_tags(self,model,listiter, multiline_selected):

            namefile = model[listiter][0]
            if namefile in self.tag_finder :
                alpha =  self.tag_finder[namefile]
            else :
                return { "title":"", "artist":"", "album":"", "track":"", "year":"", "genre":"", "cover":""}


            if multiline_selected == 1 :
                 for i in range(1,len(listiter)):
                    beta = model[listiter[i]][0]
                    if beta in self.tag_finder :
                        for tagi in ["artist","album","year","genre","cover"] :
                            if alpha[tagi] != self.tag_finder[beta][tagi] :
                                alpha[tagi] = ""


            return alpha

        def reorder_data(self,mzdata):
            '''
            take a bunch of data from mz and make it in the form { title = , ...}
            '''

            dictionnary = {}

            dictionnary["title"]    = mzdata['recording-list'][0]['title']
            dictionnary["artist"]   = mzdata['recording-list'][0]['artist-credit'][0]["artist"]["name"]

            if 'disambiguation' in mzdata['recording-list'][0]['artist-credit'][0]["artist"]:
                dictionnary["genre"] = mzdata['recording-list'][0]['artist-credit'][0]["artist"]["disambiguation"]
            else :
                dictionnary["genre"] = ""


            if 'release-list' in mzdata['recording-list'][0] :
                try :
                    dictionnary["cover"]    = mb.get_image(mbid = mzdata['recording-list'][0]["release-list"][0]["id"],coverid = "front", size = 250)
                except :
                    dictionnary["cover"] = ""

                dictionnary["album"]    = mzdata['recording-list'][0]['release-list'][0]["release-group"]["title"] #album
                dictionnary["track"]    = mzdata['recording-list'][0]['release-list'][0]["medium-list"][0]['track-list'][0]["number"]
                if 'date' in mzdata['recording-list'][0]['release-list'][0] :
                    dictionnary["year"] = mzdata['recording-list'][0]['release-list'][0]["date"].split("-")[0]
                else :
                    dictionnary["year"] = ""
            else :
                dictionnary["album"]    = ""
                dictionnary["track"]    = ""
                dictionnary["year"]     = ""

            return dictionnary




        def remove_extension(self, filename):
            '''
            return the filename without the extension
            '''
            namelist = filename.split('.')
            print(namelist)
            return namelist[0:-1]



    
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
