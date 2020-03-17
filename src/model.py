import os
from os import walk
from threading import Thread

from .audio_getter import is_extension_managed, get_file_manager
from .crawler_data import DataCrawler
from .tools import is_selection_equal
from .treeview import TreeView
from .view import View


class Model:
    class __Model:

        def __init__(self):
            """
            Initialisation of the model class
            """
            self.directory = ''
            self.modification = {}
            self.audio_tags = {}
            self.view = View.get_instance()
            self.selection = None
            self.file_name = []
            self.tags_dictionary = {
                'title': {'value': ''},
                'album': {'value': ''},
                'artist': {'value': ''},
                'genre': {'value': ''},
                'cover': {'value': ''},
                'year': {'value': ''},
                'track': {'value': ''},
                'length': {'value': ''},
                'size': {'value': ''},
                'lyrics': {'value': ''}
            }

            self.data_crawler = DataCrawler.get_instance()

        def update_directory(self, directory, store):
            """
            we the user open a new directory, we remove all waiting modifications
            """
            self.directory = directory
            self.update_list(store)
            self.selection = None
            self.modification = {}

        def reset_all(self, selection):
            """
            Reset modification and reupdate the view,it suppose that something is selectioned (True)
            """
            self.modification = {}
            self.view.erase()
            self.update_view(selection)

            tree_handler = TreeView.get_instance()
            tree_handler.remove_bold_font(self.file_name)

        def reset_one(self, selection):
            """
            Find the selected rows and delete the related dictionnary
            nested in modifications. Then update view
            """
            model, list_iter = selection.get_selected_rows()

            for i in range(0, len(list_iter)):
                name_file = model[list_iter[i]][0]
                if name_file in self.modification:
                    self.modification[name_file] = {}

                tree_handler = TreeView.get_instance()
                tree_handler.remove_bold_font([name_file])

            self.update_view(selection)

        def save_one(self, selection):
            """
            Find the selected rows, set tags for each row and then save modification.
            We don't need to update the view after saving one file.
            """
            model, list_iter = selection.get_selected_rows()
            tree_handler = TreeView.get_instance()

            for i in range(len(list_iter)):
                name_file = model[list_iter[i]][0]
                audio = get_file_manager(name_file, self.directory)
                if name_file in self.modification:
                    file_modification = self.modification[name_file]

                    for key in self.tags_dictionary:
                        if key in file_modification:
                            audio.set_tag(key, file_modification[key])

                    tree_handler.remove_bold_font([name_file])
                    audio.save_modifications()

                self.modification[name_file] = {}

        def update_list(self, store):
            """
            Erase the list in the tree view and then update it with filename with extension
            handled by GabTag
            """

            self.file_name = []
            store.clear()

            file_list = []
            for (directory_path, directory_name, files_name) in walk(self.directory):
                file_list.extend(files_name)
                break

            for name_file in file_list:
                if is_extension_managed(name_file):
                    self.file_name.append(name_file)
                    store.append([name_file, 'No', 400])

        def update_view(self, selection):
            """
            Erase the view and the current tag value then get tags for selected row (or rows)
            and show them.
            """

            self.selection = selection

            model, list_iteration = selection.get_selected_rows()

            self.view.erase()
            self.erase_tag()

            multiple_line_selected = self.get_tags(
                model, list_iteration)  # return a bool

            data_scrapped = self.data_crawler.get_tags(
                model, list_iteration, multiple_line_selected)
            lyrics_scrapped = self.data_crawler.get_lyrics(
                model, list_iteration, multiple_line_selected)

            self.view.show_tags(self.tags_dictionary, multiple_line_selected)

            if data_scrapped is None:
                self.view.show_mbz({'title': '', 'artist': '', 'album': '',
                                    'track': '', 'year': '', 'genre': '', 'cover': ''})

                length_selection = len(list_iteration)
                file_selection = []

                for i in range(len(list_iteration)):
                    name_file = model[list_iteration[i]][0]
                    file_selection.append(name_file)

                thread_waiting_mbz = Thread(target=self.wait_for_mbz, args=(
                    model, list_iteration, length_selection, file_selection, multiple_line_selected))
                thread_waiting_mbz.start()
            else:
                self.view.show_mbz(data_scrapped)

            if lyrics_scrapped is None:
                self.view.show_lyrics('File not crawled yet on lyrics.wikia')
            else:
                self.view.show_lyrics(lyrics_scrapped)

        def wait_for_mbz(self, model, list_iteration, len_selection, file_selection, multiple_line_selected):
            is_waiting_mbz = 1

            while is_selection_equal(self.selection, len_selection, file_selection) and is_waiting_mbz == 1:
                data_scrapped = self.data_crawler.get_tags(
                    model, list_iteration, multiple_line_selected)
                if data_scrapped is not None and is_selection_equal(self.selection, len_selection, file_selection):
                    is_waiting_mbz = 0
                    self.view.show_mbz(data_scrapped)

        def wait_for_lyrics(self, model, list_iteration, len_selection, file_selection, multiple_line_selected):
            is_waiting_lyrics = 1

            while is_selection_equal(self.selection, len_selection, file_selection) and is_waiting_lyrics == 1:
                lyrics_scrapped = self.data_crawler.get_lyrics(
                    model, list_iteration, multiple_line_selected)
                if lyrics_scrapped is not None and is_selection_equal(self.selection, len_selection, file_selection):
                    is_waiting_lyrics = 0
                    self.view.show_lyrics(lyrics_scrapped)

        def rename_files(self):

            file_list = []
            for (_, _, file_names) in walk(self.directory):
                file_list.extend(file_names)
                break

            for name_file in file_list:
                if is_extension_managed(name_file):
                    audio = get_file_manager(name_file, self.directory)
                    new_name = {}
                    for key in self.tags_dictionary:
                        new_name[key] = audio.get_tag(key)
                    os.rename(os.path.join(self.directory, name_file), os.path.join(
                        self.directory,
                        new_name['title'] + '-' + new_name['album'] + '-' + new_name['artist'] + audio.get_extension()))
                    # TODO remove this useless function and use a correct one)

        def update_modifications(self, selection, tag_changed, new_value):
            """
            If the file name is already a key in the directory, add or update the modified tags
            else create a new key in modification
            """
            model, list_iter = selection.get_selected_rows()

            name_file = model[list_iter][0]

            if len(list_iter) == 1:  # TODO try to merge the case ==1 and >1
                if name_file in self.modification:
                    alpha = self.modification[name_file]
                    alpha[tag_changed] = new_value
                else:
                    self.modification[name_file] = {}
                    alpha = self.modification[name_file]
                    alpha[tag_changed] = new_value

                tree_handler = TreeView.get_instance()
                if self.file_modified(name_file):
                    tree_handler.add_bold_font([name_file])
                else:
                    tree_handler.remove_bold_font([name_file])

            elif len(list_iter) > 1:
                for i in range(0, len(list_iter)):
                    if model[list_iter[i]][0] in self.modification:
                        alpha = self.modification[model[list_iter[i]][0]]
                        alpha[tag_changed] = new_value

                    else:
                        self.modification[model[list_iter[i]][0]] = {}
                        alpha = self.modification[model[list_iter[i]][0]]
                        alpha[tag_changed] = new_value
                    tree_handler = TreeView.get_instance()
                    if self.file_modified(name_file):
                        tree_handler.add_bold_font([model[list_iter[i]][0]])
                    else:
                        tree_handler.remove_bold_font([model[list_iter[i]][0]])

        def file_modified(self, name_file):

            audio = get_file_manager(name_file, self.directory)

            audio_tag = {}
            tag_modified = {}
            for key in self.tags_dictionary:
                audio_tag[key] = audio.get_tag(key)

            if name_file in self.modification:
                tag_modified = self.modification[name_file]
            else:
                pass

            for key_tag in tag_modified:
                if tag_modified[key_tag] != audio_tag[key_tag]:
                    return True

            return False

        def set_data_lyrics(self, selection):

            model, list_iterator = selection.get_selected_rows()

            if len(list_iterator) > 1:
                multiple_line_selected = 1
            else:
                multiple_line_selected = 0

            if len(list_iterator) == 1:
                lyrics = self.data_crawler.get_lyrics(
                    model, list_iterator, multiple_line_selected)
                self.update_modifications(selection, 'lyrics', lyrics)

        def set_data_crawled(self, selection):

            model, list_iterator = selection.get_selected_rows()

            if len(list_iterator) > 1:
                multiple_line_selected = 1
            else:
                multiple_line_selected = 0

            data_scrapped = self.data_crawler.get_tags(
                model, list_iterator, multiple_line_selected)

            new_data_scrapped = {}

            for key in data_scrapped:
                if data_scrapped[key] != "":
                    new_data_scrapped[key] = data_scrapped[key]

            for key in new_data_scrapped:
                self.update_modifications(
                    selection, key, new_data_scrapped[key])

        def update_modification_name_file(self, name_file, key, new_value):
            self.modification[name_file][key] = new_value

            tree_handler = TreeView.get_instance()
            if self.file_modified(name_file):
                tree_handler.add_bold_font([name_file])
            else:
                tree_handler.remove_bold_font([name_file])

        def set_online_tags(self):
            tag_founds = self.data_crawler.tag_finder

            for name_file in tag_founds:
                if name_file in self.modification:
                    for key in tag_founds[name_file]:
                        self.update_modification_name_file(
                            name_file, key, tag_founds[name_file][key])

                else:
                    self.modification[name_file] = {}
                    for key in tag_founds[name_file]:
                        self.update_modification_name_file(
                            name_file, key, tag_founds[name_file][key])

        def erase_tag(self):
            """
            erase current tags value
            """
            for key in self.tags_dictionary:
                self.tags_dictionary[key]['value'] = ''

        def save_modifications(self, selection):
            """
            For each key file in modification, we get the tags inside the nested dictionary and
            integer them on the audio tag file. Eventually we save the audio tag file.
            """
            tree_handler = TreeView.get_instance()

            for filename in self.modification:
                audio = get_file_manager(filename, self.directory)
                file_modifications = self.modification[filename]

                for key in self.tags_dictionary:
                    if key in file_modifications:
                        audio.set_tag(key, file_modifications[key])

                tree_handler.remove_bold_font([filename])

                audio.save_modifications()

            self.modification = {}

        def get_tags(self, model, list_iterator):
            """
            First we get the selected rows, we get the tag value of the first row, if there are several
            rows, we check the tag value inside them are the same as in the first row. If yes, those tags
            value are shown.
            """

            name_file = model[list_iterator][0]
            audio = get_file_manager(name_file, self.directory)

            for key in self.tags_dictionary:
                self.tags_dictionary[key]["value"] = audio.get_tag(key)

            self.audio_tags = self.tags_dictionary.copy()
            self.check_dictionary(name_file)  # Look in Modification

            if len(list_iterator) > 1:

                contkey_dico = self.tags_dictionary.copy()

                for key in self.tags_dictionary:
                    contkey_dico[key] = 1

                for i in range(1, len(list_iterator)):
                    name_file = model[list_iterator[i]][0]
                    audio = get_file_manager(name_file, self.directory)
                    for key in contkey_dico:
                        if contkey_dico[key] == 1:
                            contkey_dico[key] = self.check_tag_equal_key_value(audio.check_tag_existence(
                                key), audio.get_tag(key), name_file, key, self.tags_dictionary[key]["value"])
                for key in contkey_dico:
                    if contkey_dico[key] == 0:
                        self.tags_dictionary[key]["value"] = ""

                return 1  # we return 1 if multiple rows
            else:
                return 0  # O otherwise

        def check_dictionary(self, name_file):
            """
            Check in the filename modification dictionary the existence of tags and
            update the current list of tags with found values.
            """

            dict_tag_changed = {}
            if name_file in self.modification:
                dict_tag_changed = self.modification[name_file]

            for key in self.tags_dictionary:
                if key in dict_tag_changed:
                    self.tags_dictionary[key]["value"] = dict_tag_changed[key]

        def check_tag_equal_key_value(self, audio_key_exist, audio_tag_value, name_file, key, key_value):
            """
            We check that the tag 'key' is equal to key_value for name_file else we return 0.
            We first look in modification then in the tag audio file.
            """

            if name_file in self.modification:
                dict_tag_changed = self.modification[name_file]
                if key in dict_tag_changed:
                    if key_value != dict_tag_changed[key]:
                        return 0
                    else:
                        return 1

            if not audio_key_exist or key_value != audio_tag_value:
                return 0
            else:
                return 1

    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if Model.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Model.__instance = Model.__Model()

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Model.__instance is None:
            Model()
        return Model.__instance
