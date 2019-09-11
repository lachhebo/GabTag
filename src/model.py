from os import walk
#from time import sleep
from threading import Thread
from .moteur import Moteur
from .view import View
from .data_crawler import Data_Crawler
from .treeview import TreeView

#from gi.repository import Pango

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
            self.selection = None
            self.moteur = Moteur()
            self.tagdico = {  # TODO add that in a separate json file.
                "title": {"value": ""},
                "album": {"value": ""},
                "artist": {"value": ""},
                "genre": {"value": ""},
                "cover": {"value": ""},
                "year": {"value": ""},
                "track": {"value": ""},
                "length": {"value": ""},
                "size": {"value": ""},
                "lyrics": {"value": ""}
            }

            self.data_crawler = Data_Crawler.getInstance()

        def update_directory(self, directory, store):
            '''
            we the user open a new directory, we remove all waiting modifications
            '''
            self.directory = directory
            self.update_list(store)
            self.selection = None
            self.modification = {}

        def reset_all(self, selection):
            '''
            Reset modification and reupdate the view,it supose that something is selectionned (True)
            '''
            self.modification = {}
            self.view.erase()
            self.update_view(selection)

            treehandler = TreeView.getInstance()
            treehandler.remove_bold_font(self.filenames)

        def title2filename(self, title):
            for registeredfile in  self.filenames :
                if registeredfile[0] == title :
                    namefile = registeredfile[1] #TODO : handle case were 2 files have the same title

            return namefile

        def filename2title(self, filename):
            for registeredfile in self.filenames :
                if registeredfile[1] == filename :
                    title = registeredfile[0] #TODO : handle case were 2 files have the same title

            return title

        def reset_one(self, selection):
            '''
            Find the selected rows and delete the related dictionnary
            nested in modifications. Then update view
            '''
            model, listiter = selection.get_selected_rows()

            for i in range(0, len(listiter)):
                namefile = self.title2filename(model[listiter[i]][0])
                if namefile in self.modification:
                    self.modification[namefile] = {}

                treehandler = TreeView.getInstance()
                treehandler.remove_bold_font([model[listiter[i]][0]])

            self.update_view(selection)

        def save_one(self, selection):
            '''
            Find the selected rows, set tags for each row and then save modification.
            We don't need to update the view after saving one file.
            '''

            model, listiter = selection.get_selected_rows()
            treehandler = TreeView.getInstance()

            for i in range(len(listiter)):  # TODO
                namefile = self.title2filename(model[listiter[i]][0])
                audio = self.moteur.getFile(namefile, self.directory)
                if namefile in self.modification:
                    filemodifs = self.modification[namefile]

                    for key in self.tagdico:
                        if key in filemodifs:
                            audio.setTag(key, filemodifs[key])

                    treehandler.remove_bold_font([model[listiter[i]][0]])
                    audio.savemodif()

                    '''
                    thread_mbz = threading.Thread(target = self.data_crawler.update_data_crawled, args=([namefile],self.directory)) #Writing data
                    thread_mbz.start()
                    '''

                self.modification[namefile] = {}

        def update_list(self, store):
            '''
            Erase the list in the tree view and then update it with filename with extension
            handled by GabTag
            '''

            store.clear()

            filelist = []
            for (dirpath, dirnames, filenames) in walk(self.directory):
                filelist.extend(filenames)
                break

            self.filenames = []

            for namefile in filelist:
                if self.moteur.check_extension(namefile):
                    audiofile_name = self.moteur.getFile(namefile, self.directory).getFileName()

                    self.filenames.append((audiofile_name, namefile)) # we register both the title and the file associated to it.
                    store.append([audiofile_name, "No", 400])

        def update_view(self, selection):
            '''
            Erase the view and the current tag value then get tags for selected row (or rows)
            and show them.
            '''

            self.selection = selection

            model, listiter = selection.get_selected_rows()

            self.view.erase()
            self.erasetag()

            multiple_line_selected = self.getTags(
                model, listiter)  # return a bool

            data_scrapped = self.data_crawler.get_tags(
                model, listiter, multiple_line_selected, self.filenames)
            lyrics_scrapped = self.data_crawler.get_lyrics(
                model, listiter, multiple_line_selected, self.filenames)

            self.view.show_tags(self.tagdico, multiple_line_selected)

            if data_scrapped == None:
                self.view.show_mbz({"title": "", "artist": "", "album": "",
                                    "track": "", "year": "", "genre": "", "cover": ""})

                lenselec = len(listiter)
                fileselec = []


                for i in range(len(listiter)):
                    namefile = self.title2filename(model[listiter][0])
                    fileselec.append(namefile)

                thread_waiting_mbz = Thread(target=self.wait_for_mbz, args=(
                    model, listiter, lenselec, fileselec, multiple_line_selected))
                thread_waiting_mbz.start()
            else:
                self.view.show_mbz(data_scrapped)

            if lyrics_scrapped == None:
                self.view.show_lyrics("File not crawled yet on lyrics.wikia")
            else:
                self.view.show_lyrics(lyrics_scrapped)

        def wait_for_mbz(self, model, listiter, lenselec, fileselec, multiple_line_selected):
            is_waiting_mbz = 1

            while self.is_selectionequal(self.selection, lenselec, fileselec) and is_waiting_mbz == 1:
                data_scrapped = self.data_crawler.get_tags(
                    model, listiter, multiple_line_selected, self.filenames)
                if data_scrapped != None and self.is_selectionequal(self.selection, lenselec, fileselec):
                    is_waiting_mbz = 0
                    self.view.show_mbz(data_scrapped)

        def wait_for_lyrics(self, model, listiter, lenselec, fileselec, multiple_line_selected):
            is_waiting_lyrics = 1

            while self.is_selectionequal(self.selection, lenselec, fileselec) and is_waiting_lyrics == 1:
                lyrics_scrapped = self.data_crawler.get_lyrics(
                    model, listiter, multiple_line_selected, self.filenames)
                if lyrics_scrapped != None and self.is_selectionequal(self.selection, lenselec, fileselec):
                    is_waiting_lyrics = 0
                    self.view.show_lyrics(lyrics_scrapped)

        def is_selectionequal(self, selec, lenselec2, filelistselec2):
            model, listiter = selec.get_selected_rows()

            if len(listiter) == lenselec2:
                for i in range(len(listiter)):
                    namefile = self.title2filename(model[listiter[i]][0])
                    if namefile not in filelistselec2:
                        return False
            else:
                return False

            return True

        def rename_files(self):

            filelist = []
            for (_, _, filenames) in walk(self.directory):
                filelist.extend(filenames)
                break

            for namefile in filelist:
                if self.moteur.check_extension(namefile):
                    audio = self.moteur.getFile(namefile, self.directory)
                    new_name = {}
                    for key in self.tagdico:
                        new_name[key] = audio.getTag(key)
                    os.rename(os.path.join(self.directory, namefile), os.path.join(
                        self.directory, new_name["title"]+"-"+new_name["album"]+"-"+new_name["artist"]+audio.getextensiontype()))
                    # TODO remove this useless function and use a correct one)

        def update_modifications(self, selection, tag_changed, new_value):
            '''
            If the namefile is already a key in the directory, add or update the modified tags
            else create a new key in modification
            '''
            model, listiter = selection.get_selected_rows()

            namefile = self.title2filename(model[listiter][0])

            if len(listiter) == 1:  # TODO try to merge the case ==1 and >1
                if namefile in self.modification:
                    alpha = self.modification[namefile]
                    alpha[tag_changed] = new_value
                else:
                    self.modification[namefile] = {}
                    alpha = self.modification[namefile]
                    alpha[tag_changed] = new_value

                treehandler = TreeView.getInstance()
                if self.file_modified(namefile):
                    treehandler.add_bold_font([model[listiter][0]])
                else:
                    treehandler.remove_bold_font([model[listiter][0]])

            elif len(listiter) > 1:
                for i in range(0, len(listiter)):
                    if self.title2filename(model[listiter[i]][0]) in self.modification:
                        alpha = self.modification[self.title2filename(model[listiter[i]][0])]
                        alpha[tag_changed] = new_value

                    else:
                        self.modification[self.title2filename(model[listiter[i]][0])] = {}
                        alpha = self.modification[self.title2filename(model[listiter[i]][0])]
                        alpha[tag_changed] = new_value
                    treehandler = TreeView.getInstance()
                    if self.file_modified(namefile):
                        treehandler.add_bold_font([model[listiter[i]][0]])
                    else:
                        treehandler.remove_bold_font([model[listiter[i]][0]])

        def file_modified(self, namefile):

            audio = self.moteur.getFile(namefile, self.directory)

            audio_tag = {}
            for key in self.tagdico:
                audio_tag[key] = audio.getTag(key)

            if namefile in self.modification:
                tag_modified = self.modification[namefile]
            else:
                print("ERROR Debug !")

            for key_tag in tag_modified:
                if tag_modified[key_tag] != audio_tag[key_tag]:
                    return True

            return False

        def set_data_lyrics(self, selection):

            model, listiter = selection.get_selected_rows()

            if len(listiter) > 1:
                multiple_line_selected = 1
            else:
                multiple_line_selected = 0

            if len(listiter) == 1:
                lyrics = self.data_crawler.get_lyrics(
                    model, listiter, multiple_line_selected, self.filenames)
                self.update_modifications(selection, "lyrics", lyrics)

        def set_data_crawled(self, selection):

            model, listiter = selection.get_selected_rows()

            if len(listiter) > 1:
                multiple_line_selected = 1
            else:
                multiple_line_selected = 0

            data_scrapped = self.data_crawler.get_tags(
                model, listiter, multiple_line_selected, self.filenames)

            new_data_scrapped = {}

            for key in data_scrapped:
                if data_scrapped[key] != "":
                    new_data_scrapped[key] = data_scrapped[key]

            for key in new_data_scrapped:
                self.update_modifications(
                    selection, key, new_data_scrapped[key])

        def update_modification_namefile(self, namefile, key, new_value):

            self.modification[namefile][key] = new_value

            treehandler = TreeView.getInstance()
            if self.file_modified(namefile):
                treehandler.add_bold_font([self.filename2title(namefile)])
            else:
                treehandler.remove_bold_font([self.filename2title(namefile)])

        def set_online_tags(self):
            tag_finded = self.data_crawler.tag_finder

            for namefile in tag_finded:
                if namefile in self.modification:
                    for key in tag_finded[namefile]:
                        self.update_modification_namefile(
                            namefile, key, tag_finded[namefile][key])

                else:
                    self.modification[namefile] = {}
                    for key in tag_finded[namefile]:
                        self.update_modification_namefile(
                            namefile, key, tag_finded[namefile][key])

        def set_online_lyrics(self):  # TODO
            pass

        def erasetag(self):
            '''
            erase current tags value
            '''
            for key in self.tagdico:
                self.tagdico[key]["value"] = ""

        def save_modifications(self, selection):
            '''
            For each key file in modification, we get the tags inside the nested dictionnary and
            integer them on the audio tag file. Eventually we save the audio tag file.
            '''
            treehandler = TreeView.getInstance()

            for filename in self.modification:
                audio = self.moteur.getFile(filename, self.directory)
                filemodifs = self.modification[filename]

                for key in self.tagdico:
                    if key in filemodifs:
                        audio.setTag(key, filemodifs[key])

                treehandler.remove_bold_font([self.filename2title(filename)])

                audio.savemodif()

            self.modification = {}

        def getTags(self, model, listiter):
            '''
            First we get the selected rows, we get the tag value of the first row, if there are several
            rows, we check the tag value inside them are the same as in the first row. If yes, those tags
            value are shown.
            '''

            namefile = self.title2filename(model[listiter][0])
            print(namefile)
            audio = self.moteur.getFile(namefile, self.directory)


            for key in self.tagdico:
                self.tagdico[key]["value"] = audio.getTag(key)

            self.audio_tag = self.tagdico.copy()
            self.check_dictionnary(namefile)   # Look in Mofification

            if len(listiter) > 1:

                contkey_dico = self.tagdico.copy()

                for key in self.tagdico:
                    contkey_dico[key] = 1

                for i in range(1, len(listiter)):
                    namefile = self.title2filename(model[listiter[i]][0])
                    audio = self.moteur.getFile(namefile, self.directory)
                    for key in contkey_dico:
                        if contkey_dico[key] == 1:
                            contkey_dico[key] = self.check_tag_equal_key_value(audio.check_tag_existence(
                                key), audio.getTag(key), namefile, key, self.tagdico[key]["value"])
                    '''
                    for key in contkey :
                        if self.audio_tag[key]["value"] != audio.getTag(key):
                            self.audio_tag
                    '''
                for key in contkey_dico:
                    if contkey_dico[key] == 0:
                        self.tagdico[key]["value"] = ""

                return 1  # we return 1 if multiple rows
            else:
                return 0  # O otherwise

        def check_dictionnary(self, namefile):
            '''
            Check in the filename modification dictionnary the existence of tags and
            update the current list of tags with found values.
            '''

            dict_tag_changed = {}
            if namefile in self.modification:
                dict_tag_changed = self.modification[namefile]

            for key in self.tagdico:
                if key in dict_tag_changed:
                    self.tagdico[key]["value"] = dict_tag_changed[key]

        def check_tag_equal_key_value(self, audio_key_exist, audio_tag_value, namefile, key, key_value):
            '''
            We check that the tag 'key' is egal to key_value for namefile else we return 0.
            We first look in modification then in the tag audio file.
            '''

            if namefile in self.modification:
                dict_tag_changed = self.modification[namefile]
                if key in dict_tag_changed:
                    if key_value != dict_tag_changed[key]:
                        return 0
                    else:
                        return 1

            if not(audio_key_exist) or key_value != audio_tag_value:
                return 0
            else:
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
