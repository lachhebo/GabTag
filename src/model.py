from os import walk
from threading import Thread

from .audio_getter import is_extension_managed, get_file_manager
from .crawler_data import DATA_CRAWLER
from .tools import is_selection_equal
from .treeview import TREE_VIEW
from .view import VIEW


class Model:
    def __init__(self):
        """
        Initialisation of the model class
        """
        self.directory = ""
        self.modification = {}
        self.audio_tags = {}
        self.view = VIEW
        self.selection = None
        self.file_name = []
        self.tags_dictionary = {
            "title": {"value": ""},
            "album": {"value": ""},
            "artist": {"value": ""},
            "genre": {"value": ""},
            "cover": {"value": ""},
            "year": {"value": ""},
            "track": {"value": ""},
            "length": {"value": ""},
            "size": {"value": ""},
        }

        self.data_crawler = DATA_CRAWLER

    def update_directory(self, directory, store):
        """
        we the user open a new directory, we remove all waiting
        modifications
        """
        self.directory = directory
        self.update_list(store)
        self.selection = None
        self.modification = {}

    def reset_all(self, selection):
        """
        Cancel modification before it being saved
        and reupdate the view,it supposes that something
        is selectioned (True)
        """
        self.modification = {}
        self.view.erase()
        self.update_view(selection)

        tree_handler = TREE_VIEW
        tree_handler.remove_bold_font(self.file_name)

    def reset_one(self, selection):
        """
        Find the selected rows and delete the related dictionnary
        nested in modifications. Then update view
        """
        model, list_iter = selection.get_selected_rows()

        for i in range(0, len(list_iter)):
            name_file = model[list_iter[i]][0]
            self.modification[name_file] = {}

            tree_handler = TREE_VIEW
            tree_handler.remove_bold_font([name_file])

        self.update_view(selection)

    def save_one(self, selection):
        """
        Find the selected rows, set tags for each row and then save
        modification.
        We don't need to update the view after saving one file.
        """
        model, list_iter = selection.get_selected_rows()
        tree_handler = TREE_VIEW

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
        Erase the list in the tree view and then update it with filename
        with extension handled by GabTag
        """

        self.file_name = []
        store.clear()

        file_list = []
        for (_, _, files_name) in walk(self.directory):
            file_list.extend(files_name)
            break

        for name_file in file_list:
            if is_extension_managed(name_file):
                self.file_name.append(name_file)
                store.append([name_file, "No", 400])

    def update_view(self, selection):
        """
        Erase the view and the current tag value then get tags for
        selected row (or rows) and show them.
        """

        self.selection = selection

        model, list_iteration = selection.get_selected_rows()

        self.view.erase()
        self.erase_tag()

        multiple_line_selected = self.get_tags(model, list_iteration)  # return a bool

        data_scrapped = self.data_crawler.get_tags(
            model, list_iteration, multiple_line_selected
        )

        self.view.show_tags(self.tags_dictionary, multiple_line_selected)

        if data_scrapped is None:
            self.view.show_mbz(
                {
                    "title": "",
                    "artist": "",
                    "album": "",
                    "track": "",
                    "year": "",
                    "genre": "",
                    "cover": "",
                }
            )

            length_selection = len(list_iteration)
            file_selection = []

            for i in range(len(list_iteration)):
                name_file = model[list_iteration[i]][0]
                file_selection.append(name_file)

            thread_waiting_mbz = Thread(
                target=self.wait_for_mbz,
                args=(
                    model,
                    list_iteration,
                    length_selection,
                    file_selection,
                    multiple_line_selected,
                ),
            )
            thread_waiting_mbz.start()
        else:
            self.view.show_mbz(data_scrapped)

    def wait_for_mbz(
        self,
        model,
        list_iteration,
        len_selection,
        file_selection,
        multiple_line_selected,
    ):

        is_waiting_mbz = 1
        selection_are_equal = is_selection_equal(
            self.selection, len_selection, file_selection
        )

        while selection_are_equal and is_waiting_mbz == 1:

            data_gat = self.data_crawler.get_tags(
                model, list_iteration, multiple_line_selected
            )

            selection_are_equal2 = is_selection_equal(
                self.selection, len_selection, file_selection
            )

            if data_gat is not None and selection_are_equal2:
                is_waiting_mbz = 0
                self.view.show_mbz(data_gat)

    def update_modifications(self, selection, tag_changed, new_value):
        """
        If the file name is already a key in the directory, add or update
        the modified tags else create a new key in modification
        """

        model, list_iter = selection.get_selected_rows()

        for i in range(0, len(list_iter)):
            name_file = model[list_iter[i]][0]
            self._update_modif_for_one_file(tag_changed, new_value, name_file)

    def file_modified(self, name_file: str) -> bool:
        if name_file not in self.modification:
            return False

        audio = get_file_manager(name_file, self.directory)
        audio_tag = audio.get_tags()
        tag_modified = self.modification[name_file]

        for key_tag in tag_modified:
            if tag_modified[key_tag] != audio_tag[key_tag]:
                return True

        return False

    def update_modification_name_file(
        self, name_file: str, key: str, new_value: str
    ) -> None:
        self.modification[name_file][key] = new_value

        tree_handler = TREE_VIEW
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
                        name_file, key, tag_founds[name_file][key]
                    )

            else:
                self.modification[name_file] = {}
                for key in tag_founds[name_file]:
                    self.update_modification_name_file(
                        name_file, key, tag_founds[name_file][key]
                    )

    def erase_tag(self):
        """
        erase current tags value
        """
        for key in self.tags_dictionary:
            self.tags_dictionary[key]["value"] = ""

    def save_modifications(self):
        """
        For each key file in modification, we get the tags inside
        the nested dictionary and integer them on the audio tag file.
        Eventually we save the audio tag file.
        """
        tree_handler = TREE_VIEW

        for filename in self.modification:
            audio = get_file_manager(filename, self.directory)
            file_modifications = self.modification[filename]

            for key in self.tags_dictionary:
                if key in file_modifications:
                    audio.set_tag(key, file_modifications[key])

            tree_handler.remove_bold_font([filename])

            audio.save_modifications()

        self.modification = {}

    def get_tags(self, model, list_iterator) -> int:
        """
        First we get the selected rows, we get the tag value of the
        first row, if there are several rows, we check the tag value
        inside them are the same as in the first row. If yes, those tags
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
                        if key not in ["length", "size"]:
                            value = self.check_tag_equal_key_value(
                                audio.check_tag_existence(key),
                                audio.get_tag(key),
                                name_file,
                                key,
                                self.tags_dictionary[key]["value"],
                            )
                            contkey_dico[key] = value
            for key in contkey_dico:
                if contkey_dico[key] == 0:
                    self.tags_dictionary[key]["value"] = ""

            return 1  # we return 1 if multiple rows
        else:
            return 0  # O otherwise

    def check_dictionary(self, name_file):
        """
        Check in the filename modification dictionary the existence of
        tags and update the current list of tags with found values.
        """

        dict_tag_changed = {}
        if name_file in self.modification:
            dict_tag_changed = self.modification[name_file]

        for key in self.tags_dictionary:
            if key in dict_tag_changed:
                self.tags_dictionary[key]["value"] = dict_tag_changed[key]

    def check_tag_equal_key_value(
        self, audio_key_exist, audio_tag_value, name_file, key, key_value
    ):
        """
        We check that the tag 'key' is equal to key_value
        for name_file and return 1 else we return 0.We first
        look in modification then in the
        tag audio file.
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

    def set_data_crawled(self, selection):

        data_scrapped, new_data = self._preprocess_data_scrapped(selection)

        for key in data_scrapped:
            if data_scrapped[key] != "":
                new_data[key] = data_scrapped[key]

        for key in new_data:
            self.update_modifications(selection, key, new_data[key])

    def _preprocess_data_scrapped(self, selection):
        model, list_iterator = selection.get_selected_rows()
        if len(list_iterator) > 1:
            multiple_line_selected = 1
        else:
            multiple_line_selected = 0
        data_scrapped = self.data_crawler.get_tags(
            model, list_iterator, multiple_line_selected
        )
        new_data_scrapped = {}
        return data_scrapped, new_data_scrapped

    def _update_modif_for_one_file(self, tag_changed, new_value, name_file):
        if name_file not in self.modification:
            self.modification[name_file] = {}

        self.modification[name_file][tag_changed] = new_value

        if self.file_modified(name_file):
            TREE_VIEW.add_bold_font([name_file])
        else:
            TREE_VIEW.remove_bold_font([name_file])


MODEL = Model()
