from typing import List, Any

from .audio_getter import get_file_manager
from .crawler_data import DATA_CRAWLER


class Model:
    def __init__(self):
        """
        Initialisation of the model class
        """
        self.modification = {}
        self.tags_dictionary = {
            "title": "",
            "album": "",
            "artist": "",
            "genre": "",
            "cover": "",
            "year": "",
            "track": "",
            "length": "",
            "size": "",
        }
        self.audio_data = {}

    def reset_all(self) -> None:
        self.modification = {}
        self.audio_data = {}

    def erase_tag(self) -> None:
        for key in self.tags_dictionary:
            self.tags_dictionary[key] = ""

    def reset(self, file_names: List) -> None:
        for file_name in file_names:
            self.modification[file_name] = {}

    def get_modification(self, name_file: str) -> Any:
        """
        Find the selected rows, set tags for each row and then save
        modification.
        We don't need to update the view after saving one file.
        """
        if name_file in self.modification:
            return self.modification[name_file]

    def update_modification(
        self, tag_changed: str, new_value: str, name_file: str, directory: str
    ) -> bool:
        if name_file not in self.modification:
            self.modification[name_file] = {}

        self.modification[name_file][tag_changed] = new_value

        return self.is_file_modified(name_file, directory)

    def update_modifications(
        self, file_names: List, tag_changed: str, new_value: str, directory: str
    ) -> None:
        """
        If the file name is already a key in the directory, add or update
        the modified tags else create a new key in modification
        """

        for name_file in file_names:
            self.update_modification(tag_changed, new_value, name_file, directory)

    def is_file_modified(self, name_file: str, directory: str) -> bool:
        if name_file not in self.modification:
            return False

        #audio = get_file_manager(name_file, directory)
        if name_file in self.audio_data:
            audio = self.audio_data[name_file]
        else:
            audio = get_file_manager(name_file, directory)
            self.audio_data[name_file]=audio

        audio_tag = audio.get_tags()
        tag_modified = self.modification[name_file]

        for key_tag in tag_modified:
            if tag_modified[key_tag] != audio_tag[key_tag]:
                return True

        return False

    def set_online_tags(self, directory) -> None:
        for name_file in DATA_CRAWLER.tag_founds:
            if name_file not in self.modification:
                self.modification[name_file] = {}

            for key in DATA_CRAWLER.tag_founds[name_file]:
                self.update_modification(
                    key, DATA_CRAWLER.tag_founds[name_file][key], name_file, directory
                )

    def save_modifications(self, tree_handler, directory: str, name_files: List =None) -> None:
        """
        For each key file in modification, we get the tags inside
        the nested dictionary and integer them on the audio tag file.
        Eventually we save the audio tag file.
        """

        if name_files is None:
            modifications = self.modification
        else:
            modifications = {}
            for name in name_files:
                modifications[name] = self.modification.get(name)

        for filename in modifications:
            if modifications[filename] is not None:
                if filename in self.audio_data:
                    audio = self.audio_data[filename]
                else:
                    audio = get_file_manager(filename, directory)
                    self.audio_data[filename]=audio

                # audio = get_file_manager(filename, directory=directory)
                file_modifications = modifications[filename]

                for key in self.tags_dictionary:
                    if key in file_modifications:
                        audio.set_tag(key, file_modifications[key])
                        self.tags_dictionary[key] = file_modifications[key]

                tree_handler.manage_bold_font([filename], add=False)

                audio.save_modifications()
                self.modification[filename] = {}

            self.update_tags_dictionary_with_modification(filename)

        # print("tags: ", self.tags_dictionary)
        # print("modif: " , self.modification)

    def set_tags_dictionary(self, names_file: List, directory: str) -> int:
        """
        First we get the selected rows, we get the tag value of the
        first row, if there are several rows, we check the tag value
        inside them are the same as in the first row. If yes, those tags
        value are shown.
        """

        name_file = names_file[0]

        if name_file in self.audio_data:
            audio = self.audio_data[name_file]
        else:
            audio = get_file_manager(name_file, directory)
            self.audio_data[name_file]=audio

        for key in self.tags_dictionary:
            self.tags_dictionary[key] = audio.get_tag(key)


        if name_file in self.modification:
            self.update_tags_dictionary_with_modification(name_file)

        if len(names_file) > 1:

            same_tags = {key: True for key in self.tags_dictionary.keys()}

            for name_file in names_file:
                if name_file in self.audio_data:
                    audio = self.audio_data[name_file]
                else:
                    audio = get_file_manager(name_file, directory)
                    self.audio_data[name_file]=audio
                for key in same_tags:
                    if same_tags[key] is True:
                        if key not in ["length", "size"]:
                            value = self.check_tag_equal_key_value(
                                audio.check_tag_existence(key),
                                audio.get_tag(key),
                                name_file,
                                key,
                                self.tags_dictionary[key],
                            )
                            same_tags[key] = value
                        else:
                            same_tags[key] = False
            for key in same_tags:
                if same_tags[key] is False:
                    self.tags_dictionary[key] = ""

            return 1
        else:
            return 0

    def update_tags_dictionary_with_modification(self, name_file: str) -> None:
        """
        Check in the filename modification dictionary the existence of
        tags and update the current list of tags with found values.
        """

        dict_tag_changed = {}
        if name_file in self.modification:
            dict_tag_changed = self.modification[name_file]

        for key in self.tags_dictionary:
            if key in dict_tag_changed:
                self.tags_dictionary[key] = dict_tag_changed[key]

    def check_tag_equal_key_value(
        self,
        audio_key_exist: bool,
        audio_tag_value: Any,
        name_file: str,
        key: str,
        key_value: Any,
    ) -> bool:
        """
        We check that the tag 'key' is equal to key_value
        for name_file and return 1 else we return 0.We first
        look in modification then in the
        tag audio file.
        """

        if name_file in self.modification:
            modified_tags = self.modification[name_file]
            if key in modified_tags:
                if key_value != modified_tags[key]:
                    return False
                else:
                    return True

        if not audio_key_exist or key_value != audio_tag_value:
            return False

        return True

    def set_data_crawled(self, names_files: List):
        data_scrapped = DATA_CRAWLER.get_tags(names_files)
        new_data = {}

        for key in data_scrapped:
            if data_scrapped[key] != "":
                new_data[key] = data_scrapped[key]

        for key in new_data:
            self.update_modifications(names_files, key, new_data[key])


MODEL = Model()
