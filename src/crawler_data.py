import musicbrainzngs as mb
from os import walk
from .audio_getter import is_extension_managed, get_file_manager
from .tools import remove_extension, reorder_data
from .treeview import TREE_VIEW
from .version import __version__
from .view import VIEW


class DataCrawler:
    def __init__(self):
        mb.set_useragent(
            "GabTag", version=__version__, contact="ismael.lachheb@protonmail.com"
        )
        self.tag_founds = {}
        self.view = VIEW
        self.tree_view = TREE_VIEW
        self.directory = ""

    def crawl_one_file(self, name_file, directory):
        audio = get_file_manager(name_file, directory)

        tags = audio.get_tag_research()  # title, artist, album

        if tags[0] == "" and tags[1] == "":
            self.search_by_filename(name_file)
        elif tags[0] != "" and tags[1] != "":
            self.search_by_title_and_artist(name_file, tags)
        elif tags[1] == "":
            self.search_by_title_and_album(name_file, tags)
        elif tags[0] == "":
            self.search_by_artist_and_name_file(name_file, tags)

        self.tree_view.manage_crawled([name_file])

    def search_by_artist_and_name_file(self, name_file, tags):
        try:
            gathered_data = mb.search_recordings(
                query=remove_extension(name_file),
                artistname=tags[1],
                limit=1,
            )
            reordered_data = reorder_data(gathered_data)
            self.tag_founds[name_file] = reordered_data
        except mb.NetworkError:
            pass

    def search_by_title_and_album(self, name_file, tags):
        try:
            records = mb.search_recordings(recording=tags[0], release=tags[2], limit=1)
            records = reorder_data(records)
            self.tag_founds[name_file] = records
        except mb.NetworkError:
            pass

    def search_by_title_and_artist(self, name_file, tags):
        # Using tags title artist and album if they are present
        try:
            gathered_data = mb.search_recordings(
                recording=tags[0], artistname=tags[1], limit=1
            )
            self.tag_founds[name_file] = reorder_data(gathered_data)
        except mb.NetworkError:
            pass

    def search_by_filename(self, name_file):
        mz_query = remove_extension(name_file)
        self.tag_founds[name_file] = reorder_data(
            mb.search_recordings(query=mz_query, limit=1)
        )

    def update_data_crawled(self, modifications, directory):
        for name_file in modifications:
            self.tree_view.manage_crawled([name_file], False)
            if self.stop(directory):
                break
            self.crawl_one_file(name_file, directory)
            if self.stop(directory):
                break

    def erase_data(self):
        self.tag_founds = {}

    def get_file_list(self, directory):
        self.directory = directory

        file_list = []
        for (_, _, file_names) in walk(directory):
            file_list.extend(file_names)
            break

        return file_list

    def get_data_from_online(self, file_list, directory):
        for name_file in file_list:
            if is_extension_managed(name_file):
                if not self.stop(directory):
                    self.crawl_one_file(name_file, directory)

    def stop(self, directory):
        return not self.directory == directory

    def get_tags(self, model, list_iterator):

        tags_output = None

        name_file = model[list_iterator[0]][0]
        if name_file in self.tag_founds:
            tags_output = self.tag_founds[name_file].copy()

        if len(list_iterator) > 1:
            for i in range(1, len(list_iterator)):
                name_file = model[list_iterator[i]][0]
                if name_file not in self.tag_founds:
                    return None
                _tags = ["artist", "album", "year", "genre", "cover"]
                for tag_iterator in _tags:
                    tag_test = self.tag_founds[name_file][tag_iterator]
                    if tags_output[tag_iterator] != tag_test:
                        tags_output[tag_iterator] = ""
                tags_output["title"] = ""
                tags_output["track"] = ""

        return tags_output


DATA_CRAWLER = DataCrawler()
