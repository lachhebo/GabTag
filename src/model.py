from os import walk
from .moteur import Moteur
from .view import View


class Model:

    class __Model:

        def __init__(self):
            self.directory = ""
            self.modification = {}
            self.view = View.getInstance()
            self.moteur = Moteur()
            self.tagdico = { #TODO add that in a separate json file.
                        "title" :{ "groupability": 0, "value": None},
                        "album" :{ "groupability": 1, "value": None},
                        "artist":{ "groupability": 1, "value": None},
                        "genre" :{ "groupability": 1, "value": None},
                        "cover" :{ "groupability": 1, "value": None},
                        "year"  :{ "groupability": 1, "value": None},
                        "track" :{ "groupability": 1, "value": None}
                        }

        def update_directory(self,directory):
            self.directory = directory
            self.modification = {}

        def update_list(self,store):

            # Erase the list

            store.clear()

            # Update the list

            filelist = []
            for (dirpath, dirnames, filenames) in walk(self.directory):
                filelist.extend(filenames)
                break

            for namefile in filelist:
                if self.moteur.check_extension(namefile) :
                    store.append([namefile])

        def update_view(self,selection):
            '''
            Update the view when the user change his file selection
            '''

            self.view.erase()
            self.erasetag()

            model, listiter = selection.get_selected_rows()

            multiline = self.getTags(model,listiter)

            # afficher les modifs :
            self.view.show(self.tagdico, multiline)

        def update_modifications(self,selection, tag_changed, new_value):
            '''
            Update the dictionnary of modification to the user input.
            '''
            
            model, listiter = selection.get_selected_rows()

            if len(listiter) == 1:
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

        def erasetag(self):
            '''
            erase tag value
            '''
            for key in self.tagdico:
                self.tagdico[key]["value"] = None

        def save_modifications(self):
            '''
            We check th dictionnary of modification and set or update tags depending and the modification
            made by the user.
            '''


            for filename in self.modification:
                audio = self.moteur.getFile(filename, self.directory)
                filemodifs = self.modification[filename]

                for key in self.tagdico :
                    if key in filemodifs:
                        audio.setTag(key,filemodifs[key])

                audio.savemodif()

            self.modification = {}

        def getTags(self, model, listiter):
            '''
            update the tag_dico
            '''

            namefile = model[listiter][0]
            audio = self.moteur.getFile(namefile,self.directory)

            ## Look in tag

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
                            contkey_dico[key] = self.check_tag_in_file(audio,namefile,key,self.tagdico[key]["value"])

                for key in contkey_dico :
                    if contkey_dico[key] == 0 :
                        self.tagdico[key]["value"] = ""

                return 1
            else:
                return 0

        def check_dictionnary(self,namefile):
            '''
                Check in the dictionnary if a tag has been modified and return the updated
                list of tags
            '''

            dict_tag_changed = {}
            if namefile in self.modification :
                dict_tag_changed = self.modification[namefile]

            for key in self.tagdico :
                if key in dict_tag_changed :
                    self.tagdico[key]["value"] = dict_tag_changed[key]

        def check_tag_in_file(self,audio, namefile,key,key_value):

            if namefile in self.modification:
                dict_tag_changed = self.modification[namefile]
                if key in dict_tag_changed:
                    if key_value != dict_tag_changed[key]:
                        return 0
            elif not(audio.check_tag_existence(key)) or key_value != audio.getTag(key):
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
