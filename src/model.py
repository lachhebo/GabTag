from os import walk
from .moteur import Moteur
from .view import View
from .data_scrapper import Data_Scrapper
#import asyncio
import threading
import time
import os

class Model:

    class __Model:

        def __init__(self):
            '''
            Initilisaion of the model class
            '''
            self.directory = ""
            self.modification = {}
            self.view = View.getInstance()
            self.moteur = Moteur()
            self.tagdico = { #TODO add that in a separate json file.
                        "title" :{ "value": ""},
                        "album" :{ "value": ""},
                        "artist":{ "value": ""},
                        "genre" :{ "value": ""},
                        "cover" :{ "value": ""},
                        "year"  :{ "value": ""},
                        "track" :{ "value": ""},
                        "length":{ "value": ""},
                        "size"  :{ "value": ""}
                        }

            self.data_scrapper = Data_Scrapper.getInstance()

        def update_directory(self,directory):
            '''
            we the user open a new directory, we remove all waiting modifications
            '''
            self.directory = directory
            self.modification = {}
            thread_mbz = threading.Thread(target = self.data_scrapper.scrap_tags, args=(directory,)) #Writing data
            thread_mbz.start()

        def reset_all(self,selection):
            '''
            Reset modification and reupdate the view,it supose that something is selectionned (True)
            '''
            self.modification = {}
            self.view.erase()
            self.update_view(selection)

        def reset_one(self, selection):
            '''
            Find the selected rows and delete the related dictionnary
            nested in modifications. Then update view
            '''
            model, listiter = selection.get_selected_rows()

            for i in range(0,len(listiter)):
                namefile = model[listiter[i]][0]
                if namefile in self.modification:
                    del self.modification[namefile]

            self.update_view(selection)

        def save_one(self, selection):
            '''
            Find the selected rows, set tags for each row and then save modification.
            We don't need to update the view after saving one file.
            '''
            model, listiter = selection.get_selected_rows()

            for i in range(len(listiter)):
                namefile = model[listiter[i]][0]
                audio = self.moteur.getFile(namefile, self.directory)
                if namefile in self.modification :
                    filemodifs = self.modification[namefile]

                    for key in self.tagdico :
                        if key in filemodifs:
                            audio.setTag(key,filemodifs[key])

                    audio.savemodif()

                thread_mbz = threading.Thread(target = self.data_scrapper.scrap_one_tag, args=(namefile,self.directory)) #Writing data
                thread_mbz.start()
                self.modification[namefile] = {}


        def update_list(self,store):
            '''
            Erase the list in the tree view and then update it with filename with extension
            handled by GabTag
            '''

            store.clear()

            filelist = []
            for (dirpath, dirnames, filenames) in walk(self.directory):
                filelist.extend(filenames)
                break

            for namefile in filelist:
                if self.moteur.check_extension(namefile) :
                    store.append([namefile])

        def update_view(self,selection):
            '''
            Erase the view and the current tag value then get tags for selected row (or rows)
            and show them.
            '''

            model, listiter = selection.get_selected_rows()

            self.view.erase()
            self.erasetag()


            multiple_line_selected = self.getTags(model,listiter) # return a bool

            data_scrapped = self.data_scrapper.get_tags(model, listiter, multiple_line_selected)

            self.view.show(self.tagdico, multiple_line_selected)
            self.view.show_mbz(data_scrapped)


        def rename_files(self):


            filelist = []
            for (dirpath, dirnames, filenames) in walk(self.directory):
                filelist.extend(filenames)
                break

            for namefile in filelist:
                if self.moteur.check_extension(namefile) :
                    audio = self.moteur.getFile(namefile,self.directory)
                    new_name = {}
                    for key in self.tagdico :
                        new_name[key] = audio.getTag(key)
                    os.rename(os.path.join(self.directory,namefile),os.path.join(self.directory,new_name["title"]+"-"+new_name["album"]+"-"+new_name["artist"]+audio.getextensiontype()))
                    ## TODO remove this useless function and use a correct one)
                    #print(" renaming done ! ",os.path.join(self.directory,namefile), ", ",os.path.join(self.directory,new_name["title"]+"-"+new_name["album"]+"-"+new_name["artist"]))


        def update_modifications(self,selection, tag_changed, new_value):
            '''
            If the namefile is already a key in the directory, add or update the modified tags
            else create a new key in modification
            '''
            
            model, listiter = selection.get_selected_rows()

            if len(listiter) == 1: #TODO try to merge the case ==1 and >1
                if model[listiter][0] in self.modification :
                    alpha = self.modification[model[listiter][0]]
                    alpha[tag_changed] = new_value
                else :
                    self.modification[model[listiter][0]] = {}
                    alpha = self.modification[model[listiter][0]]
                    alpha[tag_changed] = new_value

            elif len(listiter) > 1:
                for i in range(0,len(listiter)):
                    if model[listiter[i]][0] in self.modification :
                        alpha = self.modification[model[listiter[i]][0]]
                        alpha[tag_changed] = new_value

                    else :
                        self.modification[model[listiter[i]][0]] = {}
                        alpha = self.modification[model[listiter[i]][0]]
                        alpha[tag_changed] = new_value

        def set_data_scrapped(self,selection):

            model, listiter = selection.get_selected_rows()

            if len(listiter)> 1 :
                multiple_line_selected = 1
            else :
                multiple_line_selected = 0

            data_scrapped = self.data_scrapper.get_tags(model, listiter, multiple_line_selected)

            if len(listiter) == 1:
                if model[listiter][0] in self.modification :
                    alpha = self.modification[model[listiter][0]]
                    for key in data_scrapped :
                        alpha[key] = data_scrapped[key]
                else :
                    self.modification[model[listiter][0]] = {}
                    alpha = self.modification[model[listiter][0]]
                    for key in data_scrapped :
                        alpha[key] = data_scrapped[key]

            elif len(listiter) > 1:
                for i in range(0,len(listiter)):
                    if model[listiter[i]][0] in self.modification :
                        alpha = self.modification[model[listiter[i]][0]]
                        for key in data_scrapped :
                            alpha[key] = data_scrapped[key]

                    else :
                        self.modification[model[listiter[i]][0]] = {}
                        alpha = self.modification[model[listiter[i]][0]]
                        for key in data_scrapped :
                            alpha[key] = data_scrapped[key]



        def erasetag(self):
            '''
            erase current tags value
            '''
            for key in self.tagdico:
                self.tagdico[key]["value"] = ""

        def save_modifications(self):
            '''
            For each key file in modification, we get the tags inside the nested dictionnary and
            integer them on the audio tag file. Eventually we save the audio tag file.
            '''

            for filename in self.modification:
                audio = self.moteur.getFile(filename, self.directory)
                filemodifs = self.modification[filename]

                for key in self.tagdico:
                    if key in filemodifs:
                        audio.setTag(key,filemodifs[key])

                audio.savemodif()


            thread_mbz = threading.Thread(target = self.data_scrapper.update_tag_finder, args=(self.modification,self.directory)) #Writing data
            thread_mbz.start()

            self.modification = {}

        def getTags(self, model, listiter):
            '''
            First we get the selected rows, we get the tag value of the first row, if there are several
            rows, we check the tag value inside them are the same as in the first row. If yes, those tags
            value are shown.
            '''

            namefile = model[listiter][0]
            audio = self.moteur.getFile(namefile,self.directory)

            for key in self.tagdico :
                self.tagdico[key]["value"] = audio.getTag(key)

            self.check_dictionnary(namefile)   # Look in Mofification

            if len(listiter) > 1:

                contkey_dico = self.tagdico.copy()

                for key in self.tagdico:
                    contkey_dico[key] = 1

                for i in range(1,len(listiter)):
                    namefile = model[listiter[i]][0]
                    audio =  self.moteur.getFile(namefile,self.directory)
                    for key in contkey_dico :
                        if contkey_dico[key] == 1:
                            contkey_dico[key] = self.check_tag_equal_key_value(audio.check_tag_existence(key),audio.getTag(key),namefile,key,self.tagdico[key]["value"])

                for key in contkey_dico :
                    if contkey_dico[key] == 0 :
                        self.tagdico[key]["value"] = ""

                return 1 # we return 1 if multiple rows
            else:
                return 0 # O otherwise

        def check_dictionnary(self,namefile):
            '''
            Check in the filename modification dictionnary the existence of tags and
            update the current list of tags with found values.
            '''

            dict_tag_changed = {}
            if namefile in self.modification :
                dict_tag_changed = self.modification[namefile]

            for key in self.tagdico :
                if key in dict_tag_changed :
                    self.tagdico[key]["value"] = dict_tag_changed[key]

        def check_tag_equal_key_value(self,audio_key_exist,audio_tag_value, namefile,key,key_value):
            '''
            We check that the tag 'key' is egal to key_value for namefile else we return 0.
            We first look in modification then in the tag audio file.
            '''

            if namefile in self.modification:
                dict_tag_changed = self.modification[namefile]
                if key in dict_tag_changed:
                    if key_value != dict_tag_changed[key]:
                        return 0
                    else :
                        return 1

            if not(audio_key_exist) or key_value != audio_tag_value:
                return 0
            else :
                return 1


    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if Model.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Model.__instance = Model.__Model()


    @staticmethod
    def getInstance():
        """ Static access method. """
        if Model.__instance == None:
            Model()
        return Model.__instance
